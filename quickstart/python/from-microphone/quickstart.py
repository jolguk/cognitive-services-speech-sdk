# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

# <code>
import azure.cognitiveservices.speech as speechsdk
import time

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
# speech_key, service_region = "36a492adffde420390f891fa14a8633f", "northeurope"
# speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config = speechsdk.SpeechConfig(
    endpoint="ws://localhost:5000/speech/recognition/conversation/cognitiveservices/v1")

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Say something...")


# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result. 
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query. 
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
# result = speech_recognizer.recognize_once()

# Checks result.
# if result.reason == speechsdk.ResultReason.RecognizedSpeech:
 #   print("Recognized: {}".format(result.text))
# elif result.reason == speechsdk.ResultReason.NoMatch:
#    print("No speech could be recognized: {}".format(result.no_match_details))
# elif result.reason == speechsdk.ResultReason.Canceled:
#    cancellation_details = result.cancellation_details
#    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#    if cancellation_details.reason == speechsdk.CancellationReason.Error:
#        print("Error details: {}".format(cancellation_details.error_details))


done = False


def stop_cb(evt):
    """callback that stops continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    speech_recognizer.stop_continuous_recognition()
    global done
    done = True

# Connect callbacks to the events fired by the speech recognizer
speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
# stop continuous recognition on either session stopped or canceled events
speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

# Start continuous speech recognition
speech_recognizer.start_continuous_recognition()

while not done:
    time.sleep(.5)

# </code>


