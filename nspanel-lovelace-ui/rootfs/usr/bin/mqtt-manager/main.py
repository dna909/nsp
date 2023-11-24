#!/usr/bin/env python
import logging
import paho.mqtt.client as mqtt
import time
import json
import subprocess
import libs.home_assistant
import libs.panel_cmd
import yaml
from uuid import getnode as get_mac
from panel import LovelaceUIPanel
import os
import threading
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import signal
import sys
from queue import Queue

logging.getLogger("watchdog").propagate = False

settings = {}
panels = {}
panel_queues = {}
last_settings_file_mtime = 0
mqtt_connect_time = 0
has_sent_reload_command = False
mqtt_client_name = "NSPanelLovelaceManager_" + str(get_mac())
client = mqtt.Client(mqtt_client_name)
logging.basicConfig(level=logging.DEBUG)

def on_connect(client, userdata, flags, rc):
    global settings
    logging.info("Connected to MQTT Server")
    # subscribe to panelRecvTopic of each panel
    for settings_panel in settings["nspanels"].values():
        client.subscribe(settings_panel["panelRecvTopic"])

def on_ha_update(entity_id):
    global panel_queues
    for queue in panel_queues.values():
        queue.put(("HA:", entity_id))

def on_message(client, userdata, msg):
    global panel_queues
    try:
        if msg.payload.decode() == "":
            return
        parts = msg.topic.split('/')
        if msg.topic in panel_queues.keys():
            data = json.loads(msg.payload.decode('utf-8'))
            if "CustomRecv" in data:
                queue = panel_queues[msg.topic]
                queue.put(("MQTT:", data["CustomRecv"]))
        else:
            logging.debug("Received unhandled message on topic: %s", msg.topic)

    except Exception:  # pylint: disable=broad-exception-caught
        logging.exception("Something went wrong during processing of message:")
        try:
            logging.error(msg.payload.decode('utf-8'))
        except:  # pylint: disable=bare-except
            logging.error(
                "Something went wrong when processing the exception message, couldn't decode payload to utf-8.")

def get_config_file():
    CONFIG_FILE = os.getenv('CONFIG_FILE')
    if not CONFIG_FILE:
        CONFIG_FILE = './panels.yaml'
    return CONFIG_FILE

def get_config(file):
    global settings

    try:
        with open(file, 'r', encoding="utf8") as file:
            settings = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print ("Error while parsing YAML file:")
        if hasattr(exc, 'problem_mark'):
            if exc.context != None:
                print ('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                    str(exc.problem) + ' ' + str(exc.context) +
                    '\nPlease correct data and retry.')
            else:
                print ('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                    str(exc.problem) + '\nPlease correct data and retry.')
        else:
            print ("Something went wrong while parsing yaml file")
        return False

    if not settings.get("mqtt_username"):
        settings["mqtt_username"] = os.getenv('MQTT_USER')
    if not settings.get("mqtt_password"):
        settings["mqtt_password"] = os.getenv('MQTT_PASS')
    if not settings.get("mqtt_port"):
        settings["mqtt_port"] = os.getenv('MQTT_PORT')
    if not settings.get("mqtt_server"):
        settings["mqtt_server"] = os.getenv('MQTT_SERVER')


    settings["is_addon"] = False

    if not settings.get("home_assistant_token"):
        st = os.getenv('SUPERVISOR_TOKEN')
        if st and "home_assistant_token" not in settings and "home_assistant_address" not in settings:
            settings["home_assistant_token"] = st
            settings["home_assistant_address"] = "http://supervisor"
            settings["is_addon"] = True
    return True

def connect():
    global settings, home_assistant, client
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(
        settings["mqtt_username"], settings["mqtt_password"])
    # Wait for connection
    connection_return_code = 0
    mqtt_server = settings["mqtt_server"]
    mqtt_port = int(settings["mqtt_port"])
    logging.info("Connecting to %s:%i as %s",
                 mqtt_server, mqtt_port, mqtt_client_name)
    while True:
        try:
            client.connect(mqtt_server, mqtt_port, 5)
            break  # Connection call did not raise exception, connection is sucessfull
        except:  # pylint: disable=bare-except
            logging.exception(
                "Failed to connect to MQTT %s:%i. Will try again in 10 seconds. Code: %s", mqtt_server, mqtt_port, connection_return_code)
            time.sleep(10.)

    # MQTT Connected, start APIs if configured
    if settings["home_assistant_address"] != "" and settings["home_assistant_token"] != "":
        libs.home_assistant.init(settings, on_ha_update)
        libs.home_assistant.connect()
    else:
        logging.info("Home Assistant values not configured, will not connect.")

    libs.panel_cmd.init(client)

    setup_panels()

def loop():
    global client
    # Loop MQTT
    client.loop_forever()

def setup_panels():
    global settings, panel_queues
    # Create NsPanel object
    for name, settings_panel in settings["nspanels"].items():
        if "timeZone" not in settings_panel:
            settings_panel["timeZone"] = settings.get("timeZone", "Europe/Berlin")
        if "locale" not in settings_panel:
            settings_panel["timezone"] = settings.get("locale", "en_US")
        if "hiddenCards" not in settings_panel:
            settings_panel["hiddenCards"] = settings.get("hiddenCards", [])

        #panels[name] = LovelaceUIPanel(name, settings_panel)

        mqtt_queue = Queue(maxsize=20)
        panel_queues[settings_panel["panelRecvTopic"]] = mqtt_queue
        panel_thread = threading.Thread(target=panel_thread_target, args=(mqtt_queue, name, settings_panel))
        panel_thread.daemon = True

        panel_thread.start()

def panel_thread_target(queue, name, settings_panel):
    panel = LovelaceUIPanel(name, settings_panel)
    while True:
        msg = queue.get()
        #print(msg)
        if msg[0] == "MQTT:":
            panel.customrecv_event_callback(msg[1])
        elif msg[0] == "HA:":
            panel.ha_event_callback(msg[1])







def config_watch():
    class ConfigChangeEventHandler(FileSystemEventHandler):
        def __init__(self, base_paths):
            self.base_paths = base_paths

        def dispatch(self, event):
            for base_path in self.base_paths:
                if event.src_path.endswith(base_path):
                    super(ConfigChangeEventHandler, self).dispatch(event)
                    return

        def on_modified(self, event):
            logging.info('Modification detected. Reloading panels.')
            pid = os.getpid()
            os.kill(pid, signal.SIGTERM)

    logging.info('Watching for changes in config file')
    project_files = []
    project_files.append(get_config_file())
    handler = ConfigChangeEventHandler(project_files)
    observer = Observer()
    observer.schedule(handler, path=os.path.dirname(get_config_file()), recursive=True)
    observer.start()
    while True:
        time.sleep(1)

def signal_handler(signum, frame):
    logging.info(f"Received signal {signum}. Initiating restart...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_handler)
    threading.Thread(target=config_watch).start()
    if (get_config(get_config_file())):
        connect()
        loop()
    else:
        while True:
          time.sleep(100)