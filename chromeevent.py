"""
    Handles events from a chromecast device, and reports these to various endpoints
"""

import time
from chromestate import ChromeState
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
        print(self.update_status())
        self.mqtt.publish(self.mqttpath + "media", self.update_status())

    def __mqtt_publish(self, msg):
        self.mqtt.publish(self.mqttpath + '/media', msg.json())
        self.mqtt.publish(self.mqttpath + '/state', msg.player_state)


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

    def update_status(self):
        """ Return state of the player """
        self.status = {
            'metadata_type': self.device.media_metadata.type,
            'title': self.device.media_metadata.title,
            'series_title': self.device.media_metadata.series_title,
            'season': self.device.media_metadata.season,
            'episode': self.device.media_metadata.episode,
            'artist': self.device.media_metadata.artist,
            'album_name': self.device.media_metadata.album_name,
            'album_artist': self.device.media_metadata.album_artist,
            'track': self.device.media_metadata.track,
            'subtitle_tracks': self.device.media_metadata.subtitle_tracks,
            'images': self.device.media_metadata.images,
            'supports_pause': self.device.media_metadata.supports_pause,
            'supports_seek': self.device.media_metadata.supports_seek,
            'supports_stream_volume': self.device.media_metadata.supports_stream_volume,
            'supports_stream_mute': self.device.media_metadata.supports_stream_mute,
            'supports_skip_forward': self.device.media_metadata.supports_skip_forward,
            'supports_skip_backward': self.device.media_metadata.supports_skip_backward,
        }
        return self.status

    def state_json(self):
        """ Returns status as json encoded string """
        return self.status.json()
