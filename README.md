# Chrome Domoticz

This is a small python script using pychromecast to propegate status from chromecast devices to MQTT. Currently it only supports one AUDIO and one VIDEO chromecasts, and it expects both to be available!

It also implement a simple webservice to control the chromecast (ie. start stream, pause/forward/stop etc), which I have used in a companion dashboard

The listed audio / video streams (in chrome.py) is mainly for some danish tv/radio channels

the included Dockerfile can be used to build a docker image, with the following command


```
docker build -t chromecast-integrator .
```

afterwards start it with 

```
docker run --name chromecast --restart unless-stopped -v /opt/chromecast:/config -d -t --net=host -p8181:8181 chromecast-integrator
```
