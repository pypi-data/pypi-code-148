from meili_sdk.websockets.client import MeiliWebsocketClient
from sentry_sdk import capture_exception, capture_message
from meili_lib.agent import agent_sentry
from meili_lib.parse_data import parse_waypoints, parse_topic, parse_docking_routine


from std_msgs.msg import Bool


class Handlers:

    def __init__(self, agent):
        self.agent = agent
        self.client = []  # docking routine

        for i in range(0, self.agent.number_of_vehicles):
            self.client.append(0)  # docking routine

        self.rate = None

    def sdk_setup(self):
        """sdk_setup"""
        try:
            self.agent.client = MeiliWebsocketClient(
                self.agent.token,
                override_host=self.agent.server_instance.replace("https", "wss"),
                fleet=self.agent.fleet,
                open_handler=self.open_handler,
                close_handler=self.close_handler,
                error_handler=self.error_handler,
                task_handler=self.task_handler,
                task_cancellation_handler=self.task_cancellation_handler,
                move_action_handler=self.move_action_handler,
                slow_down_handler=self.slow_down_handler,
                topic_list_initializer_handler=self.topic_handler,
                # path_rerouting_handler=self.path_rerouting_handler,
                # docking_routine_request_handler=self.docking_routine_request_handler,
                # docking_routine_finalize_handler=self.docking_routine_finalize_handler,
                # collision_clearance_handler=self.collision_clearance_handler,
            )
        except KeyError as error:
            self.agent.log_info(f"[ROSHandler] No handler named {error}")
            capture_exception(error)
        return self.agent.client

    def __check_fleet_get_vehicle_position(self, vehicle):
        if self.agent.fleet:
            return self.agent.return_vehicle_position(vehicle)
        return 0

    def move_action_handler(self, _, data: dict, vehicle: str):
        """When a task is received, goal is generated and sent to the specific robot"""
        try:
            vehicle_position = self.__check_fleet_get_vehicle_position(vehicle)
            self.send_goal(data, vehicle_position)
            self.rate.sleep()

            # If the robot is moving the task will be automatically cancelled to go to the
            # charging station.
            self.agent.log_info(
                f"[ROSHandler] Sending vehicle {self.agent.vehicle_list[vehicle_position]} to CHARGING STATION"
            )

        except Exception as error:
            self.agent.log_error(
                "[ROSHandler] Error move_action_handler: %s" % (error,)
            )
            self.agent.agent_sentry(error, "[ROSHandler] Error move_action_handler")

    def task_handler(self, _, data: dict, vehicle: str):
        """When a task is received, goal is generated and sent to the specific robot"""
        try:
            vehicle_position = self.__check_fleet_get_vehicle_position(vehicle)
            current_task_uuid = data["uuid"]

            self.agent.number_of_tasks = self.agent.number_of_tasks + 1

            self.agent.log_info(
                f"[ROSHandler] Number of received task is: {self.agent.number_of_tasks}"
            )
            self.agent.log_info(
                f"[ROSHandler] Received task assigned to vehicle: {self.agent.vehicle_list[vehicle_position]}"
            )
            if not data["metric_waypoints"]:
                # Case when only one task is sent
                self.send_goal(data, vehicle_position)
            else:
                # This is batch-task vehicle
                if self.agent.node.path_planning:
                    pose = parse_waypoints(data)
                    self.waypoints_handler(
                        vehicle_position=vehicle_position,
                        pose=pose,
                        current_task_uuid=current_task_uuid,
                    )
                else:
                    self.send_goal(data, vehicle_position)

            self.rate.sleep()

        except KeyError as error:
            self.agent.log_error(
                f"[ROSHandler] Error task_handler: {error}"
            )
            agent_sentry(error, "[ROSHandler] Error task_handler")

    def task_cancellation_handler(self, goal_id, vehicle):
        """Handles task cancellation info to specific robot"""
        self.agent.log_info(f"[ROSHandler] Cancelling task with goal id: {goal_id}")
        self.agent.log_info(f"[ROSHandler] Cancelling task of vehicle: {vehicle}")

        # if cancellation is received cancel goal
        vehicle_position = self.__check_fleet_get_vehicle_position(vehicle)

        self.cancel_goal(goal_id, vehicle_position)

        # Refresh variables
        self.agent.waypoints[vehicle_position] = False
        self.agent.task_started[vehicle_position] = 0

    def waypoints_handler(
            self, vehicle_position, pose, current_task_uuid
    ):
        """Handles offline waypoints and sends to specific robot"""
        # ROS2
        try:
            self.agent.waypoints[vehicle_position] = True
            self.agent.current_task_uuid = current_task_uuid

            self.send_waypoints(pose, vehicle_position)
        except KeyError as error:
            self.agent.log_error(
                f"[ROSHandler] Error waypoints_handler:{error}"
            )

            self.agent.agent_sentry(error, "[ROSHandler] Error waypoints_handler")

    #def get_list_of_topic():
    #    """Getting the list of topics available with specified namespace"""
    #    # getting  topics available
    #    topic_list = rospy.get_published_topics(namespace="/robot1")
    #    return topic_list

    def topic_request_handler(self, _):
        """logging information"""
        self.agent.log_info("[ROSHandler] Received topic request")
        # get_list_of_topic()

    def close_handler(self, *_):
        """Close the websocket"""
        self.agent.log_info("[ROSHandler] WS close for Agent")
        capture_message("[ROSHandler] WS close for Agent")

    def error_handler(self, _, err):
        """verifies websocket connection"""
        if not self.agent.offline.offline:
            self.agent.log_error(f"[ROSHandler] WS error {err}")
            capture_message("[ROSHandler] WS error")

    def open_handler(self, *_, **__):
        """Opens the websocket connection"""
        self.agent.log_info("[ROSHandler] WS open")
        self.agent.ws_open = True

    def topic_handler(self, _, topics, vehicle):
        """find vehicle token to passed to the topic streaming node"""

        if topics and vehicle:

            # initialise custom msg to send topic info

            for index in topics["data"]:
                self.agent.total_topics += 1
                index["vehicle_uuid"] = vehicle

                msg = parse_topic(index, self.agent)

                self.agent.topic_streaming_talker(msg)
                self.agent.log_info(
                    f"[ROSHandler] Topic to stream {index['topic']}, for vehicle {vehicle}"
                )
        else:
            self.agent.log_info("[ROSHandler] No topics to stream")

    def path_rerouting_handler(self, _, data: dict, vehicle: str):
        vehicle_position = self.__check_fleet_get_vehicle_position(vehicle)

        self.agent.goal_id_rerouted[vehicle_position] = self.agent.goal_id[vehicle_position]
        self.task_cancellation_handler(goal_id=self.agent.goal_id_rerouted[vehicle_position], vehicle=vehicle)

        data_new_path = {"rotation_angles": data["rotation_angles"], "metric_waypoints": data["path"]}
        current_task_uuid = "Rerouted_task"
        pose = parse_waypoints(data_new_path)
        self.waypoints_handler(
            vehicle_position=vehicle_position,
            pose=pose,
            current_task_uuid=current_task_uuid,
        )

    def docking_routine_finalize_handler(self, data: dict, vehicle: str):
        self.agent.log_info("[ROSHandler] Docking Routine FINALIZING request")
        vehicle_position = self.__check_fleet_get_vehicle_position(vehicle)

        rate = self.agent.node.create_rate(10)

        try:
            vehicle = self.agent.vehicles[vehicle_position]
            vehicle_prefix = str(vehicle["prefix"])
            if vehicle_prefix == "None":
                vehicle_prefix = ""

            pub = self.end_recording_publisher(vehicle_prefix)

            for i in range(10):
                variable = Bool()
                variable.data = False
                pub.publish(variable)
                rate.sleep()
            self.agent.log_info("[ROSHandler] Published end of recording")

            self.client[vehicle_position].wait_for_result()
            result = self.client[vehicle_position].get_result()

            if result is not None:
                # rospy.loginfo(f"[ROSHandler] Result {result}")
                path, rotation_angles = parse_docking_routine(result.plan)
                self.agent.ping_docking_routine(vehicle["uuid"], path, rotation_angles)
            else:
                self.agent.log_error(f"[ROSHandler] Docking output is None. Try again.")
        except Exception as e:
            self.agent.log_error(f"[ROSHandler] Error on Docking Routine Finalize: {e}")



