import openai
import speech_recognition as sr
import pyttsx3

import time

engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0')

recognize = sr.Recognizer()

<<<<<<< HEAD
openai.api_key="APIKEY"
=======
openai.api_key="KEY"
>>>>>>> 8b3a1da10c6a7544d546bb58620c89efdd811516

def audio_to_text(file):
    """with sr.AudioFile(file) as source:
        audio=recognize.record(source)
    try:
        recognize.recognize_google(audio, language="ru-RU")
    except:
        print("erreur évitée")"""
    audio_file= open(file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)
    return transcript["text"]


def text_to_audio(text):
    engine.say(text)
    engine.runAndWait()



def generate_response(prompt):
    response= openai.completion.create(
        engine="text-davinci-003",
        prompt="Ответь на это с нюансом иронии "+prompt,
        max_tokens=2000,
        temperature=0.5,
    )
    print(response)
    return response ["Choices"][0]["text"]


def main():
    while True:
        #Wait for user say "genius"
        print("Скажите пупсик")
        with sr.Microphone() as source:
            audio=recognize.listen(source)
            try:
                transcription = recognize.recognize_google(audio, language="ru-RU")
                if transcription.lower()=="пупсик":
                    #record audio
                    filename ="input.wav"
                    print("?????")
                    with sr.Microphone() as source:
                        source.pause_threshold=1
                        audio=recognize.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename,"wb")as f:
                            f.write(audio.get_wav_data())
                    print("écriture de l'audio terminée")   
                    #transcript audio to test 
                    text=audio_to_text(filename)
                    if text:
                        print(f"вы сказали{text}")
                        
                        #Generate the response
                        response = generate_response(text)
                        print(f"chat gpt 3 ответил {response}")
                            
                        #read resopnse using GPT3
                        text_to_audio(response)
            except Exception as e:
                
                print("An error ocurred : {}".format(e))

if __name__=="__main__":
    main()
