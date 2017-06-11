#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

import os
queryString = ""

def readAudio():
    # [START speech_quickstart]
    import io
    

    # Imports the Google Cloud client library
    from google.cloud import speech

    # Instantiates a client
    speech_client = speech.Client()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'audio.raw')

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        sample = speech_client.sample(
            content,
            source_uri=None,
            encoding='LINEAR16',
            sample_rate_hertz=16000)

    # Detects speech in the audio file
    alternatives = sample.recognize('en-US')

    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
    global queryString
    queryString = format(alternative.transcript)
    #print(queryString)
    # [END speech_quickstart]

def recAudio():
    import pyaudio
    import wave

    FORMAT = pyaudio.paInt16
    #CHANNELS = 2
    CHANNELS = 1
    #RATE = 44100
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 5
    #WAVE_OUTPUT_FILENAME = "file.wav"
    WAVE_OUTPUT_FILENAME = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'audio.raw')
     
    audio = pyaudio.PyAudio()
     
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print "recording..."
    frames = []
     
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording"
     
     
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def answerQueryLevel1():
    print(queryString)
    import pyttsx
    engine = pyttsx.init()
    if "balance" in queryString:        
        engine.say('Your balance is 100 rupees')
    elif "caller tune" in queryString:
        engine.say('Setting a caller tune to your number will cost 10 rupees per month.')
    elif "roaming" in queryString:
        if "incoming" in queryString:
            engine.say('Roaming incoming rate is 1 rupee per minute.')    
        elif "outgoing" in queryString:
            engine.say('Roaming outgoing rate is 3 rupees per minute.')    
        else:
            engine.say('Roaming incoming rate is 1 rupee per minute and outgoing rate is 3 rupees per minute.')                
        
    engine.runAndWait()



if __name__ == '__main__':
    
    recAudio()
    readAudio()
    answerQueryLevel1()

