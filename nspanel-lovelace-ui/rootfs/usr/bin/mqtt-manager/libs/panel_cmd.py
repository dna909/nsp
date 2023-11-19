import logging


def init(mqtt_client_from_manager):
    global mqtt_client
    mqtt_client = mqtt_client_from_manager


def custom_send(topic, msg):
    global mqtt_client
    mqtt_client.publish(topic, msg)
    logging.debug("Sent Message to NsPanel: %s", msg)


def page_type(topic, target_page):
    if target_page == "cardUnlock":
        target_page = "cardAlarm"
    custom_send(topic, f"pageType~{target_page}")


def send_time(topic, time, addTimeText=""):
    custom_send(topic, f"time~{time}~{addTimeText}")


def send_date(topic, date):
    custom_send(topic, f"date~{date}")


def entityUpd(topic, data):
    custom_send(topic, f"entityUpd~{data}")
