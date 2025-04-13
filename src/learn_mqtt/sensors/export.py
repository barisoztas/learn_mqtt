import json
import os
import random
import time

import click
from dotenv import find_dotenv, load_dotenv
from paho.mqtt import client as mqtt_client

from learn_mqtt.sensors.clock import ClockReading, GenericClock


class MQTTClient:
    """MQTTClient is a class that provides methods to connect to an MQTT broker
    and publish messages to a topic.
    """

    def __init__(self, client_id, broker, port, topic):
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.topic = topic

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Ready to send messages to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self, client):
        clock = GenericClock()  # Initialize the clock
        msg_count = 1

        while True:
            time.sleep(10)
            # Create a ClockReading instance
            clock_reading = ClockReading(
                clock_id=f"clock-{msg_count}",
                time_initiate=clock.time_initiate,
                difference_now=clock.difference,
            )
            # Serialize the ClockReading instance to JSON
            msg = clock_reading.json()
            result = client.publish(self.topic, msg)
            status = result[0]
            if status == 0:
                print(f"Sent `{msg}` to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")
            msg_count += 1


@click.command()
def publish_mqtt():
    """Publish data to MQTT broker."""

    # load environment variables from .env file
    load_dotenv(find_dotenv())

    broker = os.environ["broker"]
    port = int(os.environ["port"])
    topic = os.environ["topic"]
    # Generate a Client ID with the publish prefix.
    client_id = f"publish-{random.randint(0, 1000)}"

    mqtt_client = MQTTClient(client_id, broker, port, topic)

    client = mqtt_client.connect_mqtt()
    client.loop_start()
    mqtt_client.publish(client)
    client.loop_stop()


if __name__ == "__main__":
    publish_mqtt()
