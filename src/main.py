from core.brain import LyraBrain

class AegisOrchestrator:
    def __init__(self):
        self.brain = LyraBrain()
        self.skills = {
            "control_luces": self._skill_lights,
            "hablar": self._skill_speak
        }

    def run(self, input_text):
        print(f"\n[Usuario] -> {input_text}")
        print("[Aegis] Analizando matriz de intención...")
        
        # El cerebro procesa y decide mediante IA
        action_plan = self.brain.analyze_intent(input_text)
        action = action_plan.get("action")
        params = action_plan.get("parameters")
        reasoning = action_plan.get("reasoning")
        
        print(f"[Lyra] Decisión: {action} | Lógica: {reasoning}")

        # El orquestador ejecuta la habilidad sin preguntar
        skill_function = self.skills.get(action)
        if skill_function:
            skill_function(params)
        else:
            print(f"[Aegis] Error: Módulo de habilidad '{action}' no disponible.")

    # --- Módulos Físicos (Simulación por ahora) ---
    def _skill_lights(self, params):
        estado = params.get('estado', 'encender')
        color = params.get('color', 'blanco')
        zona = params.get('zona', 'general')
        
        accion_txt = "Encendiendo" if estado == "encender" else "Apagando"
        print(f">>> [HARDWARE] {accion_txt} luces de '{zona}' (Color: {color}). Operación exitosa. <<<")

    def _skill_speak(self, params):
        mensaje = params.get('text', 'Error: El núcleo cognitivo no generó una respuesta de texto.')
        print(f">>> [AUDIO] Lyra dice: {mensaje} <<<")

# MOTOR DE ARRANQUE CONTINUO
if __name__ == "__main__":
    aegis = AegisOrchestrator()
    print("=== SISTEMA AEGIS LYRA EN LÍNEA ===")
    print("Sistemas listos. Escribe 'apagar' para desconectar el núcleo.\n")
    
    # El Bucle Infinito (Estado de Alerta)
    while True:
        comando = input("\n[Demian] -> ")
        
        # Protocolo de apagado seguro
        if comando.lower() in ['salir', 'apagar', 'exit', 'desconectar']:
            print("[Aegis] Desconectando matriz de Lyra. Hasta pronto, estratega.")
            break
            
        # Evitar procesar "Enter" vacíos
        if comando.strip() == "":
            continue
            
        # Enviar orden al Orquestador
        aegis.run(comando)