'''Script pour envoyer message mqtt

Usage:
    mqtt_send [OPTION]
    Options :
    -h,  --host      hostname of the mqtt broker (default : 'localhost')
    -p,  --port      port of the mqtt broker (default : 1883)
    -t,  --topic     topic of the message
    -m,  --message   message payload

'''

import paho.mqtt.client as mqtt
import sys
import getopt

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"h:p:t:m:",["host=","port=","topic=","message="])
        host = 'localhost'
        port = 1883
        topic = None
        payload = None
        for o,a in opts:
            if o in ("-h","--host"):
                host = a
            if o in ("-p","--port"):
                port = int(a)
            if o in ("-t","--topic"):
                topic = a
            if o in ("-m","--message"):
                payload = a
        assert topic is not None, "Argument missing : topic."
        assert payload is not None, "Argument missing : message(payload)."
    except (ValueError, AssertionError, getopt.GetoptError) as err:
        print("Envoie un message via MQTT")
        print(str(err))
        print("Usage:")
        print("mqtt_send [OPTION]")
        print("Options :")
        print("-h,  --host      hostname of the mqtt broker (default : 'localhost')")
        print("-p,  --port      port of the mqtt broker (default : 1883)")
        print("-t,  --topic     topic of the message")
        print("-m,  --message   message payload")
        sys.exit(2)
    mqttc = mqtt.Client()
    mqttc.connect(host, port=port)
    mqttc.publish(topic, payload)

if __name__ == "__main__":
    main()
