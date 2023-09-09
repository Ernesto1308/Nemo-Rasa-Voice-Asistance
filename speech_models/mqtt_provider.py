import paho.mqtt.client as mqtt


class Mqtt:
    def __init__(
            self,
            broker,
            client_id,
            topic,
    ):
        self.broker = broker
        self.client_id = client_id
        self.topic = topic
        self.client = mqtt.Client(self.client_id)
        self.client.connect(self.broker)


class MqttSubscriber(Mqtt):
    def subscribe(self):
        self.client.subscribe(self.topic)
        self.client.loop_forever()


class MqttPublisher(Mqtt):
    def publish(self, value=None):
        self.client.publish(self.topic, payload=value)
