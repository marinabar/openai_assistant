import openai
import speech_recognition as sr
import pyttsx3


engine = pyttsx3.init()

# propriétés de la voix artificielle
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0')
engine.setProperty('rate', 160)

# clé contenu dans le fichier
with open("apikey.txt", 'r') as f:
    openai.api_key=f.read()


def audiowhisper(file):
    """
    Analyse un fichier audio vocal et renvoie le texte trouvé
    """
    audio_file= open(file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, 
        prompt="Bonjour, euh",
        language="fr")
    return transcript["text"]

def text_to_audio(text):
    """
    Prononce le texte en entrée
    """
    engine.say(text)
    engine.runAndWait()


def generate_response(messages):
    """
    Génère la réponse de GPT3
    """
    response= openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.5,
    )
    return response["choices"][0]["message"]


print("dites carnaval")
run=True
filename="input.wav"

#liste des messages de notre conversation avec chatPT
messages = [
    {"role":"system", 'content':"Tu réponds avec une petite touche de passif aggressif"},
    ]

while run:
    # on écoute jusqu'à reconnaître le mot clé
    with sr.Microphone() as source:
            r=sr.Recognizer()
            audio=r.listen(source)

            try:

                transcription = r.recognize_google(audio, language="fr-FR")

                #test si mot clé présent
                if "carnaval" in transcription.lower():
                    text_to_audio("je vous écoute")

                    while True:
                        print("j'attends votre réponse")

                        # on enregistre la réponse
                        with sr.Microphone() as source:
                            r=sr.Recognizer()
                            r.adjust_for_ambient_noise(source)
                            audiorep=r.listen(source)
                            with open(filename,"wb")as f:
                                f.write(audiorep.get_wav_data())
                        print("analyse du texte")

                        # analyse avec whisper
                        text=audiowhisper(filename)

                        #On vérifie si demande de sortie
                        if "quitter" in text.lower() or "au revoir" in text.lower():
                            text_to_audio("au revoir mon coco")

                            # permet de sortir de la boucle principale 
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