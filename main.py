import paho.mqtt.client as mqtt
import json, multiprocessing, subprocess, os, sys, pyautogui
from time import sleep


def parse_data(jsonData):
    return json.loads(jsonData)


# The callback for when the client receives a CONNACK response from the server.
def runSubProcess(file):
    result = subprocess.run(file, capture_output=True, text=True, shell=True)
    return


def error_log_report(Topic, msg):
    if config['debug']:
        log_errors = open("log.txt", "a")
        log_errors.write(
            "\n------------------------Topic: " + Topic + "-----------------------------------------------------------\n")
        log_errors.write(str(msg))
        log_errors.write(
            "\n--------------------------------------------------------------------------------------------------\n")
        log_errors.close()
    return


def exec(cmd):
    p = multiprocessing.Process(target=runSubProcess, args=[cmd])
    p.start()


def disconnect():
    mqttc.disconnect()


def open_url(url):
    if sys.platform == "win32":
        os.startfile(url)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, url])
    return


# ignoreMsg
def ignoreMsg(msg):
    for m in config['ignoreMsg']:
        if m == msg:
            return True
    return False


def press(payload):
    if payload:
        pyautogui.press(payload)


def click(x, y):
    if x & y:
        pyautogui.click(x, y)


def getMapKeys(payload):
    print(payload)
    if payload in mapKeys:
        return mapKeys[payload]
    else:
        return


# The callback for when a PUBLISH message is received from the server.
def on_message(mqttc, userdata, msg):
    error_log_report(msg.topic, msg.payload)
    msg.payload = msg.payload.decode()
    if ignoreMsg(msg.payload):
        return
    if msg.topic == config['topics'][config['rTopic']]:
        msg.payload = getMapKeys(msg.payload)
        press(msg.payload)
    else:
        payload = parse_data(msg.payload)
        if payload['type'] == "exec":
            exec(payload['cmd'])
        elif payload['type'] == "url":
            open_url(payload['cmd'])
        elif payload['type'] == "press":
            press(payload['cmd'])
        elif payload['type'] == "click":
            click(payload['cmd'][0], payload['cmd'][1])
        elif payload['type'] == "disconnect":
            disconnect()


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in config['topics']:
        client.subscribe(topic)


if __name__ == "__main__":
    global config
    global mapKeys
    global startLoopPress
    startLoopPress = 0
    config = parse_data(open("mqttrunerConfig.json", "r").read())
    mapKeys = parse_data(open("mapKeys.json", "r").read())
    multiprocessing.freeze_support()
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.username = config['username']
    mqttc.password = config['password']
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(config['addr'], config['port'], config['keepalive'])
    mqttc.loop_forever()
