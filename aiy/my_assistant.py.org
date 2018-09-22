#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import sys

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.voicehat
from google.assistant.library.event import EventType
import aiy.audio
import subprocess


radio=False

mpsyt = subprocess.Popen(["/usr/local/bin/mpsyt",""],stdin=subprocess.PIPE,stdout=subprocess.PIPE)



logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)




def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)

def test_message():
    aiy.audio.say('This is a test message')

def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))

def classic_fm():
    subprocess.call('mpc clear', shell=True)
    subprocess.call('mpc add http://52.3.202.102:8000/stream.mp3', shell=True)
    subprocess.call('mpc play', shell=True)

def vizag_radio():
    subprocess.call('mpc clear', shell=True)
    subprocess.call('mpc add http://fmout.spicefm.in:8000/spice_b', shell=True)
    subprocess.call('mpc play', shell=True)

def sdjazz():
    subprocess.call('mpc clear', shell=True)
    subprocess.call('mpc add http://listen.jazz88.org/ksds.mp3', shell=True)
    subprocess.call('mpc play', shell=True)
    
def news():
    subprocess.call('mpc clear', shell=True)
    subprocess.call('mpc add http://media-ice.musicradio.com/LBCUKMP3Low', shell=True)
    subprocess.call('mpc play', shell=True)
    
def radio_off():
    subprocess.call('mpc clear', shell=True)
    subprocess.call('mpc stop', shell=True)
    
#GET_VOLUME = r'amixer get Master | grep "Front Left:" | sed "s/.*\[\([0-9]\+\)%\].*/\1/"'
#SET_VOLUME = 'amixer -q set Master %d%%'

GET_VOLUME = r'mpc volume | sed "s/volume: \([0-9]\+\)\%.*/\1/"'
SET_VOLUME = 'mpc volume %d'

def get_volume():
    result = subprocess.check_output(GET_VOLUME, shell=True).strip()
    aiy.audio.say('Volume is %s' % result.decode('utf-8'))


def set_volume( res ):
    vol = int(res) 
    vol = max(0, min(100, vol))
    subprocess.call(SET_VOLUME % vol, shell=True)
    aiy.audio.say('Volume at %d %%.' % vol)


GET_MASTER_VOLUME = r'amixer get Master | grep "Front Left:" | sed "s/.*\[\([0-9]\+\)%\].*/\1/"'
SET_MASTER_VOLUME = 'amixer -q set Master %d%%'

def get_master_volume():
    result = subprocess.check_output(GET_MASTER_VOLUME, shell=True).strip()
    aiy.audio.say('Master volume is %s' % result.decode('utf-8'))


def set_master_volume( res ):
    vol = int(res) 
    vol = max(0, min(100, vol))
    subprocess.call(SET_VOLUME % vol, shell=True)
    aiy.audio.say('Master volume at %d %%.' % vol)




def play_track( search_string ):

    global mpsyt
    
    mpsyt.stdin.write(bytes('/' + search_string + '\n1\n', 'utf-8'))
    mpsyt.stdin.flush()
    
    
def play_list( search_string ):

    global mpsyt
    
    mpsyt.stdin.write(bytes('//' + search_string + '\n1\n', 'utf-8'))
    mpsyt.stdin.flush()
    
 

















def process_event(assistant, event):
    print(event)
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')
        # eswar
        check_radio=subprocess.check_output("mpc status", shell=True)
        if "playing" in str(check_radio):
            global radio
            radio = True
            print (radio)
            print ("The radio was playing")
        else:
            global radio
            radio = False
            print ("The radio wasn't playing")
        subprocess.call('mpc stop', shell=True)

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'sleep':
            assistant.stop_conversation()
            power_off_pi()
        if text == 'check audio':
            assistant.stop_conversation()
            test_message()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()

        elif text == 'get volume':
            assistant.stop_conversation()
            get_volume()

        elif 'set volume' in text:
            assistant.stop_conversation()
            value = text.split(" ")[-1]

            try:
                value = int(value)
            except Exception as err:
                value = 50

            set_volume(value )

        elif text == 'get master':
            assistant.stop_conversation()
            get_master_volume()

        elif 'set master' in text:
            assistant.stop_conversation()
            value = text.split(" ")[-1]

            try:
                value = int(value)
            except Exception as err:
                value = 50

            set_master_volume(value )


        elif 'play song' in text:
            assistant.stop_conversation()
            value = text.split(" ")[2:]
            play_track( " ".join(value) )


        elif 'play list' in text:
            assistant.stop_conversation()
            value = text.split(" ")[2:]
            play_track( " ".join(value) )


        elif text == 'my radio':
            assistant.stop_conversation()
            classic_fm()

        elif text == 'my two radio':
            assistant.stop_conversation()
            vizag_radio()

        elif text == 'my jazz':
            assistant.stop_conversation()
            sdjazz()

        elif text == 'stop my radio':
            assistant.stop_conversation()
            radio_off()
        elif text == 'my news':
            assistant.stop_conversation()
            news()


    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)

    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
