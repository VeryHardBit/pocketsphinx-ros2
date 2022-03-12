#!/usr/bin/env python3

import os
from pocketsphinx import LiveSpeech
import rospy
from std_msgs.msg import String
import pyttsx3
#This is working badly
#from playsound import playsound

from pocketsphinx_ros.srv import TTS,TTSResponse

import re
import time

#playsound can be
# $ ffplay -nodisp -autoexit -loglevel quiet /tmp/test.wav
# $ play -b 16 --endian little -r 16000 /tmp/test.wav
# $ aplay

def playsound(f):
    os.system("aplay "+f)
    #os.system("ffplay -nodisp -autoexit -loglevel quiet -af \"atempo=1.0\" "+f)

def perform_tts(msg,tts_type='pico2wave'):
    if tts_type=='espeak':
        os.system(f'espeak "{msg}" -s70 -v en-us')
    elif tts_type=='pico2wave':
        
        ss=re.split('(\.|\,|\?)', msg)
        for s in ss:
            if s=='.':
                time.sleep(0.2)
            elif s==',':
                time.sleep(0.1)
            elif s=='?':
                time.sleep(0.3)
            else:
                os.system(f'pico2wave -l en-US -w /tmp/test.wav "{s}"')
                playsound('/tmp/test.wav')
    elif tts_type=='festival':
        os.system(f'echo "{msg}" | festival --tts')
    else:
        msg=msg.strip().strip('.')
        for extension in [".wav",".mp3"]:
            dir=get_package_share_directory('pocketsphinx_ros')+'/glados-pre-sound/'
            fn=msg.lower()+".wav"
            if os.path.exists(dir+fn):
                playsound(dir+fn)
def tts_callback(req):
    rospy.loginfo(f'speaking "{req.sentence}"')
    perform_tts(req.sentence,tts_type='pico2wave')
    return TTSResponse(True)

if __name__=='__main__':
    rospy.init_node('pocketsphinx_tts_node')
    s = rospy.Service('tts_input', TTS,tts_callback )
    print("Send request to tts_output for text-to-speech activation.")

    rospy.spin()