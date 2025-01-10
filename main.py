import ctypes
import time
import pyautogui
import subprocess
import os
import sys
import paho.mqtt.client as mqtt
import json
import multiprocessing

log_file_path = "EventLog.txt"  # Path to the log file
last_processed_line = 0  # Keeps track of the last processed line in the log

# Clear the log file when the program starts
open(log_file_path, "w").close()

def monitor_log_file():
    """Monitor the log file for new entries and send them as MQTT messages."""
    global last_processed_line
    try:
        with open(log_file_path, "r") as log_file:
            lines = log_file.readlines()

            # Process new lines
            if last_processed_line < len(lines):
                new_lines = lines[last_processed_line:]
                last_processed_line = len(lines)

                for line in new_lines:
                    if line.strip():  # Ignore empty lines
                        eventmsg = line.strip().split('-')
                        if len(eventmsg) == 2:
                            send_update(config['topics']['eventLog'], {"eventTime": eventmsg[0], "payload": eventmsg[1]})
                            if config['debug']:
                                print(f"Log entry sent: {line.strip()}")
                        else:
                            print(f"Invalid log entry format: {line.strip()}")
    except FileNotFoundError:
        print(f"Log file not found: {log_file_path}")
    except Exception as e:
        print(f"Error monitoring log file: {e}")

def send_update(topic, message):
    """Publish an update to an MQTT topic."""
    try:
        mqttc.publish(topic, json.dumps(message))
        if config['debug']:
            print(f"Sent update to topic '{topic}': {message}")
    except Exception as e:
        print(f"Failed to send update: {e}")

def on_message(mqttc, userdata, msg):
    error_log_report(msg.topic, msg.payload)
    p = multiprocessing.Process(target=runJob, args=[msg.topic, msg.payload.decode(), config, mapKeys])
    p.start()

def on_connect(client, userdata, flags, reason_code, properties):
    """Callback for handling MQTT connection events."""
    print(f"Connected with result code {reason_code}")
    for topic in config['topics']:
        client.subscribe(topic)
    send_update(config['topics']['status'], {"status": "connected", "reason_code": str(reason_code)})

def runJob(topic, payload, config, mapKeys):
    """Run a job based on the message topic and payload."""
    try:
        payload = parse_data(payload)
        cmd_type = payload.get('type')
        cmd = payload.get('cmd')
        if cmd_type == "exec":
            subprocess.run(cmd, shell=True, check=True)
        elif cmd_type == "url":
            open_url(cmd)
        elif cmd_type == "press":
            press(cmd)
        elif cmd_type == "click" and isinstance(cmd, list) and len(cmd) == 2:
            click(cmd[0], cmd[1])
        else:
            print(f"Unknown command type or format: {payload}")
    except Exception as e:
        send_update(config['topics']['error'], {"error": str(e)})
        if config['debug']:
            print(f"Error processing job: {e}")

def error_log_report(topic, msg):
    """Log errors to a file if debugging is enabled."""
    if config['debug']:
        with open("log.txt", "a") as log_errors:
            log_errors.write(
                f"\n------------------------Topic: {topic}-----------------------------------------------------------\n")
            log_errors.write(str(msg))
            log_errors.write(
                "\n--------------------------------------------------------------------------------------------------\n")
    return

def parse_data(json_data):
    """Parse JSON and ensure topics are structured as a dictionary."""
    data = json.loads(json_data)
    if isinstance(data.get('topics'), list):
        data['topics'] = {f"topic_{i}": topic for i, topic in enumerate(data['topics'])}
    return data

def ignoreMsg(msg, config):
    """Check if a message should be ignored based on the config."""
    return msg in config['ignoreMsg']

def press(payload):
    """Simulate a key press using pyautogui."""
    if payload:
        pyautogui.press(payload)

def click(x, y):
    """Simulate a mouse click at the specified coordinates."""
    if x and y:
        pyautogui.click(x, y)

def getMapKeys(payload, mapKeys):
    """Get the mapped value for a given key from mapKeys."""
    return mapKeys.get(payload)

def open_url(url):
    """Open a URL in the default web browser."""
    if sys.platform == "win32":
        os.startfile(url)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, url])
    return

if __name__ == "__main__":
    global config
    global mapKeys
    config = parse_data(open("mqttrunerConfig.json", "r").read())
    mapKeys = parse_data(open("mapKeys.json", "r").read())
    multiprocessing.freeze_support()

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.username = config['username']
    mqttc.password = config['password']
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(config['addr'], config['port'], config['keepalive'])

    mqttc.loop_start()

    while True:
        monitor_log_file()  # Monitor the log file for new entries
        time.sleep(config['eventPullInterval'])  # Sleep for eventPullInterval seconds before checking again
