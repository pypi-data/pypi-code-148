from event_generator import Severity, KafkaConnection
import re
import time

my_producer = KafkaConnection(servers=["localhost:9092"], topic="opennms-kafka-events")

message_up = "Apr 20 00:30:54 MI_PHC-US-TN-GREE-HPM011-VC Velocloud: Apr 20 00:30:54 %Parker Hannifin Corporation-5-LINK_ALIVE: Enterprise:Parker Hannifin Corporation, Severity:INFO, Edge:PH-US-TN-GREE-HPM011-VC, Event:LINK_ALIVE, Message:Link GE4 is no longer DEAD"

pattern = "^.* Velocloud: (.*) %(.*): Enterprise:(.*), Severity:(.*), Edge:(.*), Event:(.*), Message:(.*)$"

message_down = "Apr 20 00:30:38 MI_PHC-US-TN-GREE-HPM011-VC Velocloud: Apr 20 00:30:38 %Parker Hannifin Corporation-3-LINK_DEAD: Enterprise:Parker Hannifin Corporation, Severity:ALERT, Edge:PH-US-TN-GREE-HPM011-VC, Event:LINK_DEAD, Message:Link GE4 is now DEAD"

parsed = re.search(pattern, message_down)
fields = parsed.groups()


link_name = re.search("^Link (.*) is no", fields[6]).groups()[0]
my_event_down = my_producer.create_event(
    uei="uei.opennms.org/vendor/silverpeak/654321/down",
    # uei="uei.opennms.org/vendor/silverpeak/196617/down",
    severity=Severity.WARNING,
    raisedTime=fields[0],
    eventKey=fields[1],
    _foreignSource=fields[2].replace(" ", "_"),
    _foreignId="5678",
    eventText=fields[5],
    enterprise=fields[2],
    linkName=link_name,
    passiveReasonCode=message_down,
)
my_event_up = my_producer.create_event(
    uei="uei.opennms.org/vendor/silverpeak/654321/up",
    severity=Severity.WARNING,
    raisedTime=fields[0],
    eventKey=fields[1],
    _foreignSource=fields[2].replace(" ", "_"),
    _foreignId="5678",
    eventText=fields[5],
    enterprise=fields[2],
    linkName=link_name,
    passiveReasonCode=message_down,
)
print(my_event_down)
result = my_producer.send_event(my_event_down, timeout=30)
time.sleep(16)
result = my_producer.send_event(my_event_up, timeout=30)
time.sleep(16)
result = my_producer.send_event(my_event_up, timeout=30)
time.sleep(16)
result = my_producer.send_event(my_event_down, timeout=30)
time.sleep(16)
result = my_producer.send_event(my_event_down, timeout=30)


# for i in range(0, 5):
#    result = my_producer.send_event(my_event_down, timeout=30)
#    time.sleep(10)


# for i in range(0, 6):
#     for x in range(0, 850):
#         result = my_producer.send_event(my_event_down, timeout=30)
#         # time.sleep(0.5)
#         print(result)
#     print("Sleeping for 1 minutes")
#     break
#   time.sleep(60 * 1)
