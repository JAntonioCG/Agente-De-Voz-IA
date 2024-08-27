import speech_recognition as sr
import pyttsx3
import pywhatkit
from time import time
import threading

# Inicializa el motor de texto a voz
engine = pyttsx3.init()

# Nombre del asistente virtual
name = 'alexa'
attempts = 0

# Configuración de voz
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.7)

# Función para hablar
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Función para obtener comandos de voz
def get_audio(recognizer, source):
    status = False
    rec = ""

    try:
        audio = recognizer.listen(source, timeout=5)  # Timeout para evitar largos periodos de espera
        rec = recognizer.recognize_google(audio, language='es-ES').lower()
        if name in rec:
            rec = rec.replace(f"{name} ", "")
            status = True
        else:
            print(f"No reconozco el comando: {rec}")
    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
    except sr.RequestError:
        print("Error al conectarse al servicio de reconocimiento de voz.")
    except sr.WaitTimeoutError:
        print("Tiempo de espera agotado. Intentando de nuevo...")
    return {'text': rec, 'status': status}

# Función para reproducir música en YouTube
def play_music(query):
    if query:
        speak(f'Reproduciendo {query}')
        try:
            pywhatkit.playonyt(query)  # Reproduce en YouTube
        except Exception as e:
            speak("Ocurrió un error al intentar reproducir la música.")
            print(f"Error: {e}")
    else:
        speak("No se especificó ninguna canción.")

def listen_and_execute():
    global attempts
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print(f"({attempts}) Escuchando...")
            r.adjust_for_ambient_noise(source, duration=1)
            rec_json = get_audio(r, source)
            rec = rec_json['text']
            status = rec_json['status']

            if status:
                if 'reproduce' in rec:
                    music = rec.replace('reproduce', '').strip()
                    play_music(music)
                elif 'descansa' in rec:
                    speak("Saliendo...")
                    break
                else:
                    speak("No reconozco el comando.")
                    print(f"No reconozco el comando: {rec}")

                attempts = 0
            else:
                attempts += 1

# Inicia el temporizador para medir la duración
start_time = time()

# Ejecuta la función de escucha y ejecución en un hilo separado
thread = threading.Thread(target=listen_and_execute)
thread.start()
thread.join()

# Imprime la duración total del programa
print(f"PROGRAMA FINALIZADO CON UNA DURACIÓN DE: {int(time() - start_time)} SEGUNDOS")
