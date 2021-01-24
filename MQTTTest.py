import paho.mqtt.client as mqtt
from gpiozero import LED
import SequenceHelper
import time


#y = SequenceHelper.decodeSequence(x)


outlets = [LED(26), LED(21)]

def on_message(client, userdata, message):
    payload = message.payload
    print("message received=", payload)
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)
    if "DragonBox/Sequence" in message.topic:
        parse_message(payload)
    
def on_log(client, userdata, level, buf):
    print("log: ", buf)
    
def parse_message(message):
    payload = str(message.decode("utf-8","ignore"))
    print(payload)
    steps = SequenceHelper.decodeSequence(payload)
    for step in steps:
        stepType = step["type"]
        if "toggle" in stepType:
            outlet = outlets[int(step["relay"])]
            if step["value"] == 1:
                outlet.on()
            else:
                outlet.off()
        elif "delay" in stepType:
            time.sleep(float(step["value"]))
            
    
client = mqtt.Client('MQTTTest-Client')
client.connect('localhost')
client.on_message = on_message
client.on_log = on_log
    
client.subscribe('DragonBox/Sequence')

client.loop_start()