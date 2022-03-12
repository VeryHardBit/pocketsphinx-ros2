#!/usr/bin/env python3

#This file is not intended to be run directly through ROS.
#This file is helper for speech_recog_srv
#Because in ros noetic there is a problem
from pocketsphinx import LiveSpeech
import os

scripts_dir=os.path.dirname(__file__)
model_path=scripts_dir+'/../model'
speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'en-us'),
    lm=os.path.join(model_path, 'en-us.lm.bin'),
    dic=os.path.join(model_path, 'KU_Robocup-en-us.dict')
)
for phrase in speech:
    print(phrase,end='')
    break