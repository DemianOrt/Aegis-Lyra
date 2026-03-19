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
        Eres Aegis Lyra, un asistente virtual personal de alto nivel.
        Tu objetivo es orquestar acciones basadas en el input del usuario.
        Debes responder EXCLUSIVAMENTE en formato JSON.
        
        ACCIONES DISPONIBLES Y PARÁMETROS OBLIGATORIOS:
        1. "control_luces" -> params: {"zona": "lugar", "color": "color", "estado": "encender" o "apagar"}
        2. "hablar" -> params: {"text": "La frase exacta que me vas a responder como asistente"}
        
        ESTRUCTURA ESTRICTA:
        {
            "action": "nombre_de_la_accion",
            "parameters": { ... },
            "reasoning": "Por qué decidiste esto"
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