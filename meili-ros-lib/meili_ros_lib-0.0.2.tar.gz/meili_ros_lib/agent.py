import sys
import datetime

from meili_sdk.websockets.models.message import Message
from meili_sdk.websockets import constants

from geometry_msgs.msg import PoseWithCovarianceStamped, Pose
from sensor_msgs.msg import NavSatFix

from meili_lib.config_agent import ConfigAgent
from meili_lib.maths import euler_to_quaternion, quaternion_to_euler
from meili_lib.parse_data import parse_battery_data
from meili_lib.sentry import initialize_sentry, agent_sentry

from sentry_sdk import capture_exception, capture_message

initialize_sentry()


def update_capacity_lipo(voltage):
    # Calculate current capacity of lipo batteries taking into account voltage/capacity estimation using regression
    # capacity = 47.6 *voltage - 500
    capacity = 47.6 * voltage - 500
    return capacity


class Agent:
    def __init__(self, node):
        # Logging functions
        self.log_info = node.log_info
        self.log_error = node.log_error

        # Initial instances
        self.node = node
        self.token = None
        self.fleet = None
        self.mqtt_id = None

        self.vehicle_list = []
        self.vehicle_tokens = []
        self.vehicles = {}
        self.number_of_vehicles = None

        # Other classes
        self.offline = None
        self.client = None

        # Messages
        self.msg_pose = []
        self.msg_battery = []
        self.msg_gps = []

        self.msg_plan = []
        self.arr_plan = []
        self.buffer = []

        # Internet
        self.ws_open = False

        # Task
        self.task_started = []
        self.number_of_tasks = 0
        self.start_time = None

        # Waypoints
        self.waypoints = []
        self.waypoints_goal_id = []

        # Traffic control
        self.goal_id = []
        self.goal_id_rerouted = []
        self.max_vel_x = []
        self.max_vel_theta = []
        self.path_length = 200

        # Miscellaneous
        self.total_topics = 0
        self.vehicles = self.__agent_setup()

    def __agent_setup(self):
        config = ConfigAgent(self.log_info, self.log_error)
        self.log_info("[ROSAgent] The configuration is started...")

        try:
            config.open_files()

            (
                setup_token,
                self.server_instance,
                self.token,
                self.mqtt_id,
                self.fleet,
            ) = config.config_var()

            self.log_info(f"[ROSAgent] Server instance:{self.server_instance}")
            (
                self.vehicle_list,
                vehicles,
                self.vehicle_tokens,
            ) = config.config_vehicles()

            self.number_of_vehicles = len(self.vehicle_list)
            self.initialisation()

        except Exception as error:
            self.log_error(
                "[ROSAgent] Agent Setup Error: %s %s" % (type(error).__name__, error)
            )
            agent_sentry(error, "[ROSAgent] Agent Setup Error")
            sys.exit()

        for vehicle in vehicles:
            uuid = vehicle["uuid"]
            self.log_info(f"[ROSAgent] Vehicle {uuid} is on the fleet")
        self.log_info("[ROSAgent] Agent has been configured")

        return vehicles

    def initialisation(self):
        for i in range(0, self.number_of_vehicles):
            self.msg_pose.append(i)
            self.msg_battery.append(i)
            self.msg_gps.append(i)

            self.msg_plan.append(i)
            self.arr_plan.append([])
            self.buffer.append(i)

            self.task_started.append(0)
            self.waypoints.append(False)
            self.waypoints_goal_id.append(None)
            self.goal_id_rerouted.append(None)

            self.max_vel_x.append(0)
            self.max_vel_theta.append(0)
            self.goal_id.append(0)

    ################################################
    def check_topic_streaming_mode(self):
        """Check Topic Streaming"""
        if self.node.topic_streaming_mode == "FILTERING":
            self.node.get_logger().info("[ROSAgent] Mode for topic streaming is FILTERING")
        else:
            self.node.get_logger().info("[ROSAgent] Mode for topic streaming is REALTIME")

    def check_internet(self):
        """Check if there is internet if not connect the offline agent"""
        try:
            self.ws_open = self.offline.check_internet_connection(self.ws_open)
        except Exception as error:
            self.node.get_logger().info(f"[ROSAgent] Error Checking internet:{error}")

    ################################################

    # PING FUNCTIONS
    def send_message_client(self, event, value, vehicle):
        """Sends message via Websocket"""
        message = Message(event=event, value=value, vehicle=vehicle)
        message.validate()
        self.client.send(message)

    def ping_filtering_mode(self, pub_rate):
        pub_rate.sleep()

        if self.node.outdoor:
            self.ping_gps()
        else:
            self.ping_location()

        if self.node.battery_present:
            self.ping_battery()

        if self.node.traffic_control:
            self.ping_trajectory()

    def ping_location(self):
        """Ping Location """
        try:
            for index, msg in enumerate(self.msg_pose):
                if isinstance(msg, PoseWithCovarianceStamped):
                    x = round(msg.pose.pose.position.x, 3)
                    y = round(msg.pose.pose.position.y, 3)
                    orientation = msg.pose.pose.orientation
                elif isinstance(msg, Pose):
                    x = round(msg.position.x, 3)
                    y = round(msg.position.y, 3)
                    orientation = msg.orientation
                else:
                    self.log_info(
                        f"[ROSAgent] Robot {self.vehicle_list[index]} pose is not available"
                    )
                    capture_message("[ROSAgent] Robot pose is not available")
                    continue

                yaw = round(quaternion_to_euler(
                    orientation.x, orientation.y, orientation.z, orientation.w
                ),
                    3)
                self.send_message_client(
                    constants.EVENT_LOCATION,
                    {"xm": x, "ym": y, "rotation": yaw},
                    self.vehicle_list[index],
                )

        except Exception as error:
            self.log_info(f"[ROSAgent] Ping location error: {error}")
            capture_exception(error)

    def ping_battery(self):
        """Sending Battery message via websocket"""
        try:
            for index, msg in enumerate(self.msg_battery):
                if self.node.lipo_battery:
                    msg.capacity = update_capacity_lipo(msg.voltage)

                    battery_data = parse_battery_data(msg)
                    self.send_message_client(
                        constants.EVENT_BATTERY,
                        {**battery_data},
                        self.vehicle_list[index],
                    )
        except Exception as error:
            capture_exception(error)
            self.log_info("[ROSAgent] Ping Battery Error: %s" % (error,))

    def ping_trajectory(self):
        """Send the trajectory as an array of poses"""

        if self.number_of_tasks > 0:
            try:
                for index, plan in enumerate(self.arr_plan):
                    # Not sending the same path
                    if plan not in (0, self.buffer[index]):
                        self.buffer[index] = plan
                        self.send_message_client(
                            constants.EVENT_PATH_DATA,
                            {"path": self.buffer[index]},
                            self.vehicle_list[index],
                        )
            except Exception as error:
                self.log_info(
                    f"[ROSAgent] Ping Trajectory Error: {error} "
                )
                capture_exception(error)

    def ping_gps(self):
        try:
            for index, msg in enumerate(self.msg_gps):
                if isinstance(msg, NavSatFix):
                    lat = msg.latitude
                    lon = msg.longitude
                    rotation = 0
                    self.send_message_client(
                        constants.EVENT_LOCATION,
                        {"lat": lat, "lon": lon, "rotation": rotation},
                        self.vehicle_list[index],
                    )
        except Exception as e:
            self.log_info(
                "[ROSAgent] Ping GPS Error: %s ", e)
            capture_exception(e)

    def ping_docking_routine(self, vehicle, path, rotation_angles):
        # send the trajectory as an array of poses
        try:
            message = Message(
                event=constants.EVENT_DOCKING_ROUTINE,
                value={"path": path, "rotation_angles": rotation_angles},
                vehicle=vehicle,
            )
            self.log_info(path)
            message.validate()
            self.client.send(message)
            self.log_info("[ROSAgent] Docking Routine Sent")
        except Exception as e:
            self.log_info("[ROSAgent] Ping Docking Routine Error: %s ", e)
            capture_exception(e)

    ################################################
    def return_vehicle_position(self, vehicle_token):
        """Returns: Vehicle Position"""
        return self.vehicle_list.index(vehicle_token)

    ################################################
    # CALLBACKS
    def callback_pose(self, msg, vehicle_uuid):
        """Parse current robot pose and sent to FMS task_msg_server"""
        vehicle_position = self.return_vehicle_position(vehicle_uuid)
        self.msg_pose[vehicle_position] = msg

        if self.node.topic_streaming_mode == "REALTIME " and self.ws_open:
            self.ping_location()

    def callback_battery(self, msg, vehicle_uuid):
        """When battery topic is available, is parsed and sent to FMS agent"""
        if self.node.battery_present:
            vehicle_position = self.return_vehicle_position(vehicle_uuid)
            self.msg_battery[vehicle_position] = msg

            if self.node.topic_streaming_mode == "REALTIME" and self.ws_open:
                self.ping_battery()

    def callback_rosoutagg(self, msg, type_msg, time_stamp):
        rosout_message = msg.msg

        count = 0
        # Find the vehicle uuid that corresponds to the message.
        if rosout_message.find('vehicle') != -1:
            for vehicle in self.vehicle_list:
                if (rosout_message.find(vehicle)) != -1:
                    vehicle = vehicle
        elif msg.name.find('robot') != -1:
            name = '/robot' + msg.name[msg.name.find('robot') + 5]
            for vehicle in self.vehicles:
                if (vehicle['prefix']) == name:
                    vehicle = self.vehicle_list[count]
                count += 1
        else:
            vehicle = self.vehicle_list[0]

        # if self.ws_open & (type_msg == "error" or type_msg == "warning"):
        #     message = Message(
        #         event=constants.EVENT_NOTIFICATION,
        #         value={"vehicle":vehicle,
        #                "message": rosout_message, "level": type_msg,
        #                "meta": {"file": msg.file, "function": msg.function, "line": msg.line}},
        #
        #         vehicle=vehicle,
        #     )
        #     message.validate()
        #     self.client.send(message)

    def task_in_progress(self, goal_id, status_id, vehicle_uuid):
        if self.ws_open:
            vehicle_position = self.return_vehicle_position(vehicle_uuid)
            if self.waypoints_goal_id[vehicle_position] is not None:
                goal_id = self.waypoints_goal_id[vehicle_position]
                if self.goal_id_rerouted[vehicle_position] is not None:
                    goal_id = self.goal_id_rerouted[vehicle_position]

            self.goal_id[vehicle_position] = goal_id
            self.send_message_client(
                constants.EVENT_GOAL_STATUS,
                {"goal_id": goal_id, "status_id": status_id},
                vehicle_uuid,
            )
            self.log_info(
                f"[ROSAgent] Sending {goal_id} in progress<<{status_id}>> of vehicle {vehicle_position} ")

        else:
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            self.start_time = dt_string
        return 1

    def callback_status(self, msg, goal_id, status_id, vehicle_uuid):

        # Status of navigation task is parsed and send to FMS task_msg_server
        if msg.status_list and len(msg.status_list) != 0:
            vehicle_position = self.return_vehicle_position(vehicle_uuid)

            if (
                    self.waypoints_goal_id[vehicle_position] is None
                    and self.waypoints[vehicle_position]
            ):
                self.waypoints_goal_id[vehicle_position] = goal_id

            # IN PROGRESS
            if status_id == 1 and self.task_started[vehicle_position] == 0:
                try:
                    self.task_started[vehicle_position] = self.task_in_progress(
                        goal_id, status_id, vehicle_uuid
                    )
                except Exception as e:
                    self.log_error(
                        "[ROSAgent] Task in progress Callback Status error : %s", e
                    )
                    agent_sentry(e, "[ROSAgent] Task in progress Callback Status error")

            # PREEMPTED NEEDED
            if status_id == 2 and self.task_started[vehicle_position] == 1:
                self.task_preempted(goal_id, vehicle_uuid)

            # IF SUCCEEDED; ABORTED or REJECTED
            if (status_id in (3, 4, 5)) and self.task_started[vehicle_position] == 1:

                try:
                    self.task_started[vehicle_position] = self.task_finished(
                        goal_id, status_id, vehicle_uuid
                    )

                except Exception as e:
                    self.log_error(
                        "[ROSAgent] Task finished Callback Status error: %s", e
                    )
                    agent_sentry(e, "[ROSAgent] Task finished Callback Status error")

    def task_preempted(self, goal_id, vehicle_uuid):
        vehicle_position = self.return_vehicle_position(vehicle_uuid)
        self.goal_id_rerouted[vehicle_position] = goal_id

    def task_finished(self, goal_id, status_id, vehicle_uuid):
        vehicle_position = self.return_vehicle_position(vehicle_uuid)
        # TASK ONLINE
        try:
            if self.ws_open:
                if not self.waypoints[vehicle_position]:

                    if self.goal_id_rerouted[vehicle_position] is not None:
                        goal_id = self.goal_id_rerouted[vehicle_position]
                        self.goal_id_rerouted[vehicle_position] = None

                    elif self.waypoints_goal_id[vehicle_position] is not None:
                        goal_id = self.waypoints_goal_id[vehicle_position]
                        self.waypoints_goal_id[vehicle_position] = None

                    self.goal_id[vehicle_position] = goal_id
                    self.send_message_client(
                        constants.EVENT_GOAL_STATUS,
                        {"goal_id": goal_id, "status_id": status_id},
                        vehicle_uuid,
                    )
                    self.log_info(
                        f"[ROSAgent] Sending {goal_id} finished<<{status_id}>> of vehicle {vehicle_position} ")

                    self.log_info(f"Sending task finished {goal_id}")
        except Exception as e:
            self.log_info(f"({e})")
        # OFFLINE TASK
        if self.offline.offline:
            success = True

            for task in self.offline.offline_tasks:
                if self.offline.current_task_uuid == task[0]:

                    if not self.waypoints[vehicle_position]:
                        self.offline.logging_offlinetasks(
                            task,
                            self.number_of_tasks,
                            self.vehicle_list,
                            self.start_time,
                            success=success,
                        )
                        self.start_time = None
                        self.offline.task_offline_started = False
        return 0

    def callback_plan(self, msg, vehicle_uuid):
        """Callback Plan"""
        # Parse trajectory and send to the fms

        arr = [[pose.pose.position.x, pose.pose.position.y] for pose in msg.poses]
        vehicle_position = self.return_vehicle_position(vehicle_uuid)

        if len(arr) > self.path_length:
            self.arr_plan[vehicle_position] = arr[0:self.path_length]
        else:
            self.arr_plan[vehicle_position] = arr

        if (
                self.node.topic_streaming_mode == "REALTIME"
                and self.ws_open
        ):
            self.ping_trajectory()

    def callback_gps(self, msg, vehicle_uuid):
        """Callback GPS"""
        vehicle_position = self.return_vehicle_position(vehicle_uuid)
        self.msg_gps[vehicle_position] = msg
        # Parse current robot pose and sent to FMS task_msg_server
        if self.node.topic_streaming_mode == "REALTIME" and self.ws_open:
            self.ping_gps()

    ################################################
    def run(self, rate, pub_rate):
        """Running the agent"""
        # When Mode is filtering, all data is sent to the FMS task_msg_server at specific frequency
        self.check_topic_streaming_mode()

        while True:
            try:
                # Check internet connection
                if not self.offline.task_offline_started:
                    self.check_internet()
                    rate.sleep()
                if self.node.topic_streaming_mode == "FILTERING" and self.ws_open:
                    self.ping_filtering_mode(pub_rate)

            except Exception as error:
                capture_exception(error)
                self.node.get_logger().warning(
                    f"[ROSAgent] Run Error: {type(error).__name__}, {error}"
                )
