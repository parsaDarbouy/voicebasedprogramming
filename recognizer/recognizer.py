import speech_recognition as SRG
import time

store = SRG.Recognizer()
with SRG.Microphone() as s:
    print("Speak...")

    audio_input = store.record(s,duration=None)
    print("Recording time:", time.strftime("%I:%M:%S"))

    try:
        # text_output = store.recognize_google(audio_input)
        text_output2 = store.recognize_sphinx(audio_input)
        print("Text converted from audio:\n")
        # print(text_output)
        print(text_output2)
        print("Finished!!")

        print("Execution time:", time.strftime("%I:%M:%S"))
    except:
        print("Couldn't process the audio input.")
# from pocketsphinx import LiveSpeech
# for phrase in LiveSpeech(): print(phrase)