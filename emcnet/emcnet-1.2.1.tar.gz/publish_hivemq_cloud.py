# pip install paho-mqtt
import paho.mqtt.client as mqtt
import numpy as np
import time
import ssl

MQTTBROKER = '6eaa5ee5fbea4bab88ecf04950b54db5.s2.eu.hivemq.cloud'
PORT = 8883
TOPIC = "my/test/topic"
USER = "jmfife"
PW = "Freakish1!"

def on_connect(client, userdata, flags, rc):
    print('CONNACK received with code %d.' % (rc))

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

mqttc = mqtt.Client("python_pub")
mqttc.tls_set(tls_version=ssl.PROTOCOL_TLS)
mqttc.username_pw_set(USER, PW)
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.tls_insecure_set(True)
mqttc.connect(MQTTBROKER, PORT)
mqttc.loop_start()

while True:
    MESSAGE = "measurement1,location=mac rnd=" + str(np.random.uniform(20,30))
    mqttc.publish(TOPIC, MESSAGE)
    print("Published to " + MQTTBROKER + ': ' + 
          TOPIC + ':' + MESSAGE)
    time.sleep(10)

