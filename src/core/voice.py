import os
import pyttsx3
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr  # <-- NUEVA LIBRERÍA DE ESCUCHA

class LyraVoice:
    def __init__(self):
        # Configuración del Motor de Emergencia (Offline)
        self.offline_engine = pyttsx3.init()
        voces = self.offline_engine.getProperty('voices')
        for voz in voces:
            if 'spanish' in voz.name.lower() or 'es' in voz.languages:
                self.offline_engine.setProperty('voice', voz.id)
                break
                
        # Inicializamos el reconocedor de voz
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        print(f">>> [AUDIO] Lyra dice: {text} <<<")
        try:
            tts = gTTS(text=text, lang='es', tld='com.mx')
            archivo_audio = "temp_voice.mp3"
            if os.path.exists(archivo_audio):
                os.remove(archivo_audio)
            tts.save(archivo_audio)
            playsound(archivo_audio)
            os.remove(archivo_audio)
        except Exception as e:
            print(f">>> [SISTEMA] Motor primario inestable. Activando cuerdas vocales de respaldo... <<<")
            self.offline_engine.say(text)
            self.offline_engine.runAndWait()

    # --- NUEVO MÓDULO B: ESCUCHA ACTIVA ---
    def listen(self):
        with sr.Microphone() as source:
            print("\n[Aegis] Calibrando ruido de fondo... (silencio un segundo)")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("[Aegis] Escuchando... (Habla ahora)")
            
            try:
                # Escucha hasta por 5 segundos si no dices nada, y corta la frase a los 10 segundos máximo
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("[Aegis] Procesando onda de voz...")
                
                # Traducimos usando el motor gratuito de Google
                texto = self.recognizer.recognize_google(audio, language="es-MX")
                print(f"[Demian (Voz)] -> {texto}")
                return texto
                
            except sr.WaitTimeoutError:
                # Si no hablaste, no hace nada y vuelve a empezar
                return ""
            except sr.UnknownValueError:
                print("[Aegis] Ruido detectado, pero no logré entender la orden.")
                return ""
            except sr.RequestError as e:
                print(f"[ERROR DE RED] El traductor de voz falló: {e}")
                return ""