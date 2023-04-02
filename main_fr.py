import openai
import speech_recognition as sr
import pyttsx3

import time

engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0')


openai.api_key="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"

def audio_to_text(file):
    
    r=sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio=r.record(source)
    try:
        print("début de l'analyse du ")
        r.recognize_google(audio, language="fr-FR")
        print("tentative frux")
    except:
        print("erreur évitée")


def text_to_audio(text):
    engine.say(text)
    engine.runAndWait()



def generate_response(prompt):
    response= openai.completion.create(
        engine="text-davinci-003",
        prompt="Réponds à ceci avec une nuance d'ironie ; "+prompt,
        max_tokens=2000,
        temperature=0.5,
    )
    print(response)
    return response ["Choices"][0]["text"]


def main():
    while True:
        #Wait for user say "carnaval"
        print("dites carnaval")
        r=sr.Recognizer()
        with sr.Microphone() as source:
            audio=r.listen(source)
            try:
                transcription = r.recognize_google(audio, language="fr-FR")
                print(transcription)
                if transcription.lower()=="carnaval":
                    #record audio
                    filename ="input.wav"
                    print("?????")
                    source.pause_threshold=1
                    with sr.Microphone() as source:
                        r=sr.Recognizer()
                        r.adjust_for_ambient_noise(source)
                        audiorep=r.listen(source)
                        with open(filename,"wb")as f:
                            f.write(audiorep.get_wav_data())
                    print("écriture de l'audio terminée")   
                    #transcript audio to test 
                    text=audio_to_text(filename)
                    print(text, "texteeee")
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