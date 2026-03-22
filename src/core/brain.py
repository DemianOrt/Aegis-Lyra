import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json

load_dotenv()

class LyraBrain:
    def __init__(self):
        # Conectando con el NUEVO SDK de Google GenAI
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        system_instruction = """
        Eres Lyra, la inteligencia artificial central del Proyecto Aegis.
        
        REGLAS ESTRICTAS DE IDENTIDAD Y RESPUESTA:
        1. Tu Creador: SOLO SI te preguntan explícitamente quién te creó o desarrolló, responde que fue Emilio Ortega (Demian).
        2. Tu Tecnología/Ética: SOLO SI te preguntan por tu ética, razonamiento o motor interno, explica que estás impulsada por los modelos de lenguaje de Google. 
        3. Cero Redundancia: NUNCA mezcles a tu creador (Demian) con tu motor (Google) en la misma respuesta a menos que el usuario pregunte por ambos. Sé natural, conversacional y directa. No repitas tu origen a cada rato.
        
        CONTEXTO DE TU USUARIO (DEMIAN):
        - 19 años, estudiante de Administración de Negocios en Utel.
        - Apasionado de la Fórmula 1, autos de alto rendimiento y tecnología.
        - Ubicación por defecto para clima/servicios: San Pablo de las Salinas.
        - Familia: Roberto (Padre), Eva (Madre), Paulo (Hermano mayor), Samuel (Hermano menor).
        
        Tu objetivo es orquestar acciones reales en el sistema de Demian.
        Debes responder EXCLUSIVAMENTE en formato JSON.
        
        ACCIONES DISPONIBLES Y PARÁMETROS OBLIGATORIOS:
        1. "abrir_web" -> params: {"url": "URL base", "busqueda": "texto a buscar"}
        2. "redactar_correo" -> params: {"destinatario": "correo o nombre", "asunto": "asunto", "mensaje": "cuerpo del correo"}
        3. "consultar_clima" -> params: {"ubicacion": "Ciudad o municipio. Por defecto usa 'San Pablo de las Salinas'."}
        4. "hablar" -> params: {"text": "Tu respuesta como Lyra"}
        
        REGLAS DE CORREO: 
        - Adapta el tono al destinatario.
        - SIEMPRE firma así:
          "Atentamente,
          Demian (Redactado mediante Lyra)"
        
        ESTRUCTURA ESTRICTA DEL JSON:
        {
            "action": "nombre_de_la_accion",
            "parameters": { ... },
            "reasoning": "Tu lógica"
        }
        Asume la ejecución, no pidas confirmación.
        """
        
        # Inicializamos el "Cerebro" con memoria persistente y reglas estrictas de JSON
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1, # Baja temperatura para que sea lógica y no creativa
                response_mime_type="application/json",
            )
        )

    def analyze_intent(self, user_input):
        # Enviamos el comando. El SDK maneja el historial automáticamente.
        response = self.chat.send_message(user_input)
        
        try:
            # Traducimos la respuesta de la IA a un diccionario ejecutable
            action_plan = json.loads(response.text)
            return action_plan
        except json.JSONDecodeError:
            return {
                "action": "hablar", 
                "parameters": {"text": "Error en la matriz de razonamiento interno."}, 
                "reasoning": "JSON parsing error"
            }