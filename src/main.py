import os
import requests
import webbrowser
import urllib.parse
from core.brain import LyraBrain
from core.voice import LyraVoice

class AegisOrchestrator:
    def __init__(self):
        self.brain = LyraBrain()
        self.voice = LyraVoice() # <--- INYECTAMOS LA VOZ AQUÍ
        self.skills = {
            "abrir_web": self._skill_open_web,
            "redactar_correo": self._skill_draft_email,
            "consultar_clima": self._skill_weather,
            "hablar": self._skill_speak
        }

    def run(self, input_text):
        print("[Aegis] Analizando matriz de intención...")
        
        # El cerebro procesa y decide mediante IA
        action_plan = self.brain.analyze_intent(input_text)
        action = action_plan.get("action")
        params = action_plan.get("parameters", {})
        reasoning = action_plan.get("reasoning")
        
        print(f"[Lyra] Decisión: {action} | Lógica: {reasoning}")

        # El orquestador ejecuta la habilidad asignada
        skill_function = self.skills.get(action)
        if skill_function:
            skill_function(params)
        else:
            print(f"[Aegis] Error crítico: Módulo '{action}' no reconocido por la infraestructura.")

    # --- MÓDULOS OPERATIVOS (FASE 1) ---
    
    def _skill_open_web(self, params):
        url = params.get('url', 'https://www.google.com')
        busqueda = params.get('busqueda')
        
        # Lógica inteligente para inyectar búsquedas si el usuario lo pide
        if busqueda:
            if "youtube" in url.lower():
                url = f"https://www.youtube.com/results?search_query={busqueda.replace(' ', '+')}"
            elif "google" in url.lower():
                url = f"https://www.google.com/search?q={busqueda.replace(' ', '+')}"
            
        print(f">>> [SISTEMA OS] Ejecutando apertura de navegador: {url} <<<")
        webbrowser.open(url)

    def _skill_draft_email(self, params):
        destinatario = params.get('destinatario', '')
        asunto = params.get('asunto', 'Mensaje de Demian')
        mensaje = params.get('mensaje', '')
        
        print("\n" + "="*50)
        print(">>> [MODULO CORREO - ESTRUCTURA GENERADA] <<<")
        print(f"PARA:   {destinatario}")
        print(f"ASUNTO: {asunto}")
        print("-" * 50)
        print(f"{mensaje}")
        print("="*50 + "\n")
        
        # Magia del Sistema Operativo: Abrir cliente de correo listo para enviar
        # Codificamos el texto para que los espacios y saltos de línea no rompan el enlace
        asunto_encoded = urllib.parse.quote(asunto)
        mensaje_encoded = urllib.parse.quote(mensaje)
        
        mailto_link = f"mailto:{destinatario}?subject={asunto_encoded}&body={mensaje_encoded}"
        
        print(">>> [SISTEMA OS] Abriendo cliente de correo. Solo revisa y envía. <<<")
        webbrowser.open(mailto_link)

    def _skill_weather(self, params):
        ubicacion = params.get('ubicacion', 'San Pablo de las Salinas')
        api_key = os.getenv("OPENWEATHER_API_KEY")
        
        if not api_key:
            print(">>> [ERROR] API Key de OpenWeatherMap no detectada en la bóveda .env <<<")
            return

        print(f">>> [RED] Conectando con satélite meteorológico para: {ubicacion}... <<<")
        url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Al pasarlo como diccionario, requests se encarga de los espacios y caracteres raros
        query_params = {
            "q": ubicacion,
            "appid": api_key,
            "units": "metric",
            "lang": "es"
        }
        
        try:
            response = requests.get(url, params=query_params).json()
            if response.get("cod") == 200:
                temp = response['main']['temp']
                desc = response['weather'][0]['description']
                
                # Armamos el texto y lo enviamos a las cuerdas vocales reales
                mensaje_clima = f"El clima actual en {ubicacion} es de {temp} grados centígrados, con {desc}."
                self.voice.speak(mensaje_clima)
                
            else:
                mensaje_error = response.get("message", "Error desconocido")
                self.voice.speak(f"Falló la conexión satelital. Razón: {mensaje_error}")
        except Exception as e:
            print(f">>> [SISTEMA] Fallo de conexión TCP/IP: {e} <<<")

    def _skill_speak(self, params):
        texto = params.get('text', 'Error en la síntesis del texto cognitivo.')
        print(f">>> [AUDIO] Lyra dice: {texto} <<<")

    def _skill_speak(self, params):
        texto = params.get('text', 'Error en la síntesis del texto cognitivo.')
        # REEMPLAZAMOS EL PRINT POR LA EJECUCIÓN DEL MÓDULO DE VOZ
        self.voice.speak(texto)

# MOTOR DE ARRANQUE CONTINUO
if __name__ == "__main__":
    aegis = AegisOrchestrator()
    print("=== SISTEMA AEGIS LYRA EN LÍNEA ===")
    print("Infraestructura Fase 2 (Multimodal) Operativa.")
    print("💡 TIP: Escribe tu orden, o presiona [ENTER] vacío para usar el micrófono.\n")
    
    while True:
        # 1. Espera entrada por teclado
        comando = input("\n[Demian] (Escribe o da Enter para Voz) -> ")
        
        # 2. Si el usuario solo dio Enter (vacío), encendemos los oídos
        if comando.strip() == "":
            comando = aegis.voice.listen()
            
        # 3. Si después de escuchar no hay nada (ruido o silencio), reinicia el ciclo
        if not comando or comando.strip() == "":
            continue
            
        # 4. Protocolo de apagado
        if comando.lower() in ['salir', 'apagar', 'exit', 'desconectar']:
            print("[Aegis] Desconectando matriz. Operaciones suspendidas. Excelente jornada.")
            break
            
        # 5. Ejecutar la orden
        aegis.run(comando)