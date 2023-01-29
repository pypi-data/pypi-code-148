from ..events import *
from jennie.events.constants import KEY_STACK_ANGULAR_AUTOMATION, KEY_STACK_DJANGO_AUTOMATIONS, \
    KEY_STACK_ANGULAR_UI_LIB, KEY_EVENT_TYPE

class RuleEngine():
    def __init__(self, app_name, app_type, logger, token):
        self.app_name = app_name
        self.logger = logger
        self.token = token
        self.get_types(app_type)

    def get_types(self, app_type):
        if app_type == KEY_STACK_ANGULAR_AUTOMATION:
            self.TYPE = KEY_STACK_ANGULAR_AUTOMATION
            self.all_events = EVENTS_ANGULAR_AUTOMATIONS

        elif app_type == KEY_STACK_DJANGO_AUTOMATIONS:
            self.TYPE = KEY_STACK_DJANGO_AUTOMATIONS
            self.all_events = EVENTS_DJANGO_AUTOMATIONS
        else:
            self.TYPE = KEY_STACK_ANGULAR_UI_LIB
            self.all_events = EVENTS_ANGULAR_UI_LIB

        all_events_str = []
        for key in self.all_events:
            all_events_str.append(key)
        self.logger.debug("Supported event for protocol {} are".format(self.TYPE), {
            "all_events": all_events_str
        })

    def validate_events(self, automation_conf):
        idx = 0
        final_events = []
        for event_info in automation_conf:
            self.logger.debug("Validating Automation conf : ", event_info)
            if event_info[KEY_EVENT_TYPE] in self.all_events:
                event_resp = self.all_events[event_info[KEY_EVENT_TYPE]](
                    user_key=self.token, app_name=self.app_name, type=self.TYPE
                ).validate(event_info)
                if not event_resp:
                    raise ValueError("There is some error in automation event at index {} with type {}".format(
                        str(idx), event_info["event_type"]))
                else:
                    final_events.append(event_resp)
            else:
                print ("Event {} is not found in type {}".format(event_info[KEY_EVENT_TYPE], self.TYPE))
                raise ValueError("Invalid Automation Configuration")
        return final_events

    def add_event(self, event_type=None):
        self.event_type = event_type
        if not self.event_type:
            print ("\n\nSelect event type ")
            counter = 1
            events_arr = []
            for event in self.all_events:
                print ("Enter {}  ->  {}".format(str(counter).zfill(2), event.replace("-", " ").title()))
                events_arr.append(event)
                counter += 1

            user_choice = input("\n>> ")

            return self.all_events[events_arr[int(user_choice) - 1]](
                user_key=self.token, app_name=self.app_name, type=self.TYPE
            ).build_event()
        else:
            self.logger.debug("Building Event for {}".format(self.event_type))
            self.all_events[self.event_type](
                user_key=self.token, app_name=self.app_name, type=self.TYPE
            ).build_event()

    def execute_events(self, automation_conf):
        """
        Executes all events from automation conf one by one.
        :param automation_conf: Array of automation events
        :return: success_status
        """
        success_status = True
        for event_info in automation_conf:
            self.logger.debug("Executing Automation conf : ", event_info)
            if event_info[KEY_EVENT_TYPE] in self.all_events:
                event_execute_status = self.all_events[event_info[KEY_EVENT_TYPE]](
                    user_key=self.token, app_name=self.app_name, type=self.TYPE
                ).execute(event_info)
                if not event_execute_status:
                    print ("Some error occurred, stopping process")
                    success_status = False
                    return success_status
            else:
                print ("Event not in supported event type")
        return success_status