import openai
import speech_recognition as sr
import pyttsx3

import time

engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0')
engine.setProperty('rate', 160)

with open("apikey.txt", 'r') as f:
    openai.api_key=f.read()

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


def audiowhisper(file):
    audio_file= open(file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

def text_to_audio(text):
    engine.say(text)
    engine.runAndWait()



def generate_response(messages):
    response= openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.5,
    )
    return response["choices"][0]["message"]


print("dites carnaval")
run=True
filename="input.wav"

messages = [
    {"role":"system", 'content':"Tu réponds avec une petite nuance d'ironie"}
]

while run:
    with sr.Microphone() as source:
            r=sr.Recognizer()
            audio=r.listen(source)

            try:
                transcription = r.recognize_google(audio, language="fr-FR")

                if "carnaval" in transcription.lower():
                    text_to_audio("je vous écoute")

                    while True:
                        print("j'attends votre réponse")
                        with sr.Microphone() as source:
                            r=sr.Recognizer()
                            r.adjust_for_ambient_noise(source)
                            audiorep=r.listen(source)
                            with open(filename,"wb")as f:
                                f.write(audiorep.get_wav_data())
                        print("analyse du texte")
                        text=audiowhisper(filename)
                        print("analyse terminée")

                        #On vérifie si demande de sortie
                        if "quitter" in text.lower() or "au revoir" in text.lower():
                            text_to_audio("au revoir mon coco")
                            run =False
                            break
                        
                        messages.append({'role':'user', "content":text})
                        print(f"Vous avez dit {text}")
                        
                        #génère réponse par chat gpt
                        response = generate_response(messages)
                        messages.append(response)
                        print(f"chat gpt 3 a répondu {response.content}")
                            
                        #on lit la réponse de chat gpt
                        text_to_audio(response.content)
                else:
                    pass
            except Exception as e:
                print("on fait du skip")




"""
            
def main():
    while True:
        #Wait for user say "carnaval"
        print("dites carnaval")
        with sr.Microphone() as source:
            r=sr.Recognizer()
            audio=r.listen(source)
            try:
                transcription = r.recognize_google(audio, language="fr-FR")
                print(transcription)
                if transcription.lower()=="carnaval":
                    #record audio
                    print("???")
                    source.pause_threshold=1
                    with sr.Microphone() as source:
                        r=sr.Recognizer()
                        r.adjust_for_ambient_noise(source)
                        audiorep=r.listen(source)

                    text=r.recognize_google(audiorep, language="fr-FR")
                    if text:
                        print(f"Vous avez dit {text}")
                        
                        #Generate the response
                        response = generate_response(text)
                        print(f"chat gpt 3 a répondu {response}")
                            
                        #read resopnse using GPT3
                        text_to_audio(response)
            except Exception as e:
                
                print("An error ocurred : {}".format(e))

if __name__=="__main__":
    main()"""

