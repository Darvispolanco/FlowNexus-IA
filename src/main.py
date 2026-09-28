from agent import FlowNexusAgent


def show_banner():
    print()
    print("=" * 60)
    print("                 FLOWNEXUS AI")
    print("=" * 60)
    print("      Personal Research & Programming Agent")
    print("=" * 60)
    print()


def show_help():
    print("""
Comandos disponibles:

  /help
      Muestra esta ayuda.

  /status
      Muestra el estado de FlowNexus.

  /memory
      Muestra la memoria guardada.

  /clear
      Borra la memoria de conversación.

  /search <consulta>
      Realiza una búsqueda en Internet.

  /read <URL>
      Lee el contenido textual de una página.

  /check <archivo.py>
      Comprueba la sintaxis de un archivo.

  /run <archivo.py>
      Ejecuta un archivo Python dentro de workspace/.

  /test
      Comprueba la conexión con el modelo de IA.

  /exit
      Cierra FlowNexus.

Cualquier otro texto será enviado al modelo de IA.
""")


def handle_command(agent: FlowNexusAgent, command: str):
    """
    Procesa comandos especiales.

    Retorna:
        True  -> comando procesado
        False -> salir
        None  -> no es un comando conocido
    """

    command = command.strip()

    # ----------------------------------------------------------
    # SALIR
    # ----------------------------------------------------------

    if command == "/exit":
        print("\nCerrando FlowNexus...\n")
        return False

    # ----------------------------------------------------------
    # AYUDA
    # ----------------------------------------------------------

    if command == "/help":
        show_help()
        return True

    # ----------------------------------------------------------
    # ESTADO
    # ----------------------------------------------------------

    if command == "/status":
        agent.status()
        return True

    # ----------------------------------------------------------
    # MEMORIA
    # ----------------------------------------------------------

    if command == "/memory":
        agent.memory.show()
        return True

    # ----------------------------------------------------------
    # LIMPIAR MEMORIA
    # ----------------------------------------------------------

    if command == "/clear":
        agent.clear_memory()
        print("\nMemoria eliminada correctamente.\n")
        return True

    # ----------------------------------------------------------
    # TEST DE CONEXIÓN
    # ----------------------------------------------------------

    if command == "/test":
        print("\nProbando conexión con el modelo...\n")

        success = agent.llm.test_connection()

        if success:
            print("\n✓ Conexión correcta.\n")
        else:
            print("\n✗ No se pudo establecer la conexión.\n")

        return True

    # ----------------------------------------------------------
    # BÚSQUEDA WEB
    # ----------------------------------------------------------

    if command.startswith("/search "):
        query = command[len("/search "):].strip()

        if not query:
            print("Debes escribir una consulta.")
            return True

        print("\nBuscando información...\n")

        results = agent.search(query)

        if not results:
            print("No se encontraron resultados.")
            return True

        for index, result in enumerate(results, start=1):
            print(f"[{index}] {result.title}")
            print(f"URL: {result.url}")
            print(f"{result.description}")
            print("-" * 60)

        return True

    # ----------------------------------------------------------
    # LEER URL
    # ----------------------------------------------------------

    if command.startswith("/read "):
        url = command[len("/read "):].strip()

        if not url:
            print("Debes proporcionar una URL.")
            return True

        print("\nLeyendo página...\n")

        content = agent.read_url(url)

        if content is None:
            print("No fue posible leer la página.")
            return True

        print(content)

        return True

    # ----------------------------------------------------------
    # COMPROBAR CÓDIGO
    # ----------------------------------------------------------

    if command.startswith("/check "):
        file_path = command[len("/check "):].strip()

        if not file_path:
            print("Debes indicar un archivo.")
            return True

        result = agent.check_code(file_path)

        if result.success:
            print("\n✓ Sintaxis correcta.\n")
        else:
            print("\n✗ Se encontraron errores:\n")

            if result.error:
                print(result.error)

        return True

    # ----------------------------------------------------------
    # EJECUTAR CÓDIGO
    # ----------------------------------------------------------

    if command.startswith("/run "):
        file_path = command[len("/run "):].strip()

        if not file_path:
            print("Debes indicar un archivo.")
            return True

        agent.executor.run_and_print(file_path)

        return True

    return None


def main():
    show_banner()

    try:
        agent = FlowNexusAgent()

    except Exception as error:
        print("\n[ERROR] No se pudo iniciar FlowNexus.")
        print(error)
        print()
        return

    print("FlowNexus está listo.")
    print("Escribe /help para ver los comandos.")
    print("Escribe /exit para salir.")
    print()

    while True:

        try:
            user_input = input("Tú → ").strip()

        except KeyboardInterrupt:
            print("\n\nFlowNexus detenido.")
            break

        except EOFError:
            print("\n\nFlowNexus detenido.")
            break

        if not user_input:
            continue

        # ------------------------------------------------------
        # COMANDOS
        # ------------------------------------------------------

        if user_input.startswith("/"):
            result = handle_command(
                agent,
                user_input
            )

            if result is False:
                break

            if result is True:
                continue

            print(
                "Comando desconocido. "
                "Escribe /help."
            )

            continue

        # ------------------------------------------------------
        # MENSAJE NORMAL → IA
        # ------------------------------------------------------

        print("\nFlowNexus → ", end="", flush=True)

        try:
            response = agent.ask(user_input)

            print(response)
            print()

        except Exception as error:
            print("\n[ERROR]")
            print(error)
            print()


if __name__ == "__main__":
    main()
