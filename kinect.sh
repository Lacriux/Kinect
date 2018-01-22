#!/bin/bash

case "$(pidof jackdbus | wc -w)" in

0)  echo "Running jack server:"
    sudo jack_control start
    ;;
1)  echo "Jack server already running"
    ;;
esac


sudo jack_control ds alsa
sudo amsynth &
sudo qjackctl &



case "$(pidof a2jmidid | wc -w)" in

0)  echo "Running a2jmidid:"
    sudo a2jmidid &
    ;;
1)  echo "a2jmidid already running"
    ;;
esac

sleep 2


sudo jack_connect "amsynth:midi_in" "a2j:Midi Through [14] (capture): Midi Through Port-0"

/home/electrizarte/Kinect/Codigo/Kinect2.6/kinect_drumming/kinect_drumming.py

