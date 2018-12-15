"""
    Handles events from a chromecast device, and reports these to various endpoints
"""

import time
from chromestate import ChromeState
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt_client
import os

class ChromeEvent:
    """ Chrome event handling """
    def __init__(self, device, room, mqtt):

        self.device = device
        self.device.register_status_listener(self)
        self.device.media_controller.register_status_listener(self)
        self.status = ChromeState(device.device)
        self.room = room
        self.mqtt = mqtt
        self.mqttpath = 'Home/' + self.room + '/ChromeCasts/' + self.device.name
        self.mqtt.subscribe(self.mqttpath + '/action')
        self.mqtt.message_callback_add(self.mqttpath + '/action', self.mqtt_action)
        # self.device.media_controller.register_status_listener(self)
        # if self.device.cast_type != 'audio':
        #     self.status.setApp('Backdrop')
        # client = mqtt_client.Client(self.device.cast_type + '_client')
        # client.on_message = self.on_mqtt_message
        # client.connect(self.mqtthost)
        # client.loop_start()
        # client.subscribe(self.mqttroot + '/control/#')
        # client.on_disconnect = self.on_mqtt_disconnect

    # def on_mqtt_message(self, client, userdata, message):
    #     parameter = message.payload.decode("utf-8")
    #     cmd = os.path.basename(os.path.normpath(message.topic))
    #     if cmd == 'play':
    #         self.play(parameter)
    #     else:
    #         if parameter == 'pause':
    #             self.pause()
    #         if parameter == 'fwd':
    #             self.fwd()
    #         if parameter == 'rev':
    #             self.rev()
    #         if parameter == 'quit':
    #             self.quit()
    #         if parameter == 'stop':
    #             self.stop()
    #         if parameter == 'play':
    #             self.play()
    #
    # def on_mqtt_disconnect(self, client, userdata, rc):
    #     print("----------- mqtt disconnect ---------------")
    #     print(self.device.cast_type)
    #     print(rc)
    #
    def new_cast_status(self, status):
        print("----------- new cast status ---------------")
        print(status)
        app_name = status.display_name
        if app_name == "Backdrop":
            self.status.clear()
        if (app_name is None) or (app_name == ""):
            app_name = "None"
            self.status.clear()

        self.status.setApp(app_name)

        if self.device.media_controller.status.player_state == "PLAYING":
            self.state()
        self.mqtt.publish(self.mqttpath +'/app', app_name)

    def new_media_status(self, status):
        print("----------- new media status ---------------")
        print(json.dumps(self.device.media_controller.status.media_metadata))
        self.mqtt.publish(self.mqttpath + "/media", json.dumps(self.device.media_controller.status.media_metadata))

    def mqtt_action(self, mosq, obj, msg):
        print(msg.payload)
        payload = msg.payload
        if payload == b"stop":
            self.stop()
        elif payload == b"pause":
            self.pause()
        elif payload == b"fwd" or payload == b"next":
            self.fwd()
        elif payload == b"rev" or payload == b"prev":
            self.rev()
        elif payload == b"quit":
            self.quit()
        elif payload == b"play":
            self.play()

    def action(self, payload):
        if payload == "stop":
            self.stop()
        elif payload == "pause":
            self.pause()
        elif payload == "fwd" or payload == "next":
            self.fwd()
        elif payload == "rev" or payload == "prev":
            self.rev()
        elif payload == "quit":
            self.quit()
        elif payload == "play":
            self.play()

    def stop(self):
        """ Stop playing on the chromecast """
        self.device.media_controller.stop()
        self.status.clear()

    def pause(self):
        """ Pause playback """
        self.device.media_controller.pause()

    def fwd(self):
        """ Skip to next track """
        self.device.media_controller.skip()

    def rev(self):
        """ Rewind to previous track """
        self.device.media_controller.rewind()

    def quit(self):
        """ Quit running application on chromecast """
        self.device.media_controller.stop()
        self.device.quit_app()
        self.status.clear()

    def play(self, media=None):
        """ Play a media URL on the chromecast """
        self.device.media_controller.play()
        self.__mqtt_publish(self.state())


    def state_json(self):
        """ Returns status as json encoded string """
        return self.status.json()
