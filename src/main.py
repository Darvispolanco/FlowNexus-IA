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

  /exit
      Cierra FlowNexus.

Cualquier otro texto será tratado como mensaje normal.
""")


def handle_command(agent: FlowNexusAgent, command: str) -> bool:
    """
    Procesa comandos especiales.

    Devuelve:
        True  -> continuar ejecutando FlowNexus
        False -> salir
    """

    command = command.strip()

    if command == "/exit":
        print("\nCerrando FlowNexus...\n")
        return False

    if command == "/help":
        show_help()
        return True

    if command == "/status":
        agent.status()
        return True

    if command == "/memory":
        agent.memory.show()
        return True

    if command == "/clear":
        agent.clear_memory()
        print("\nMemoria eliminada correctamente.\n")
        return True

    if command.startswith("/search "):
        query = command[8:].strip()

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

    if command.startswith("/read "):
        url = command[6:].strip()

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

    if command.startswith("/check "):
        file_path = command[7:].strip()

        if not file_path:
            print("Debes indicar un archivo.")
            return True

        result = agent.check_code(file_path)

        if result.success:
            print("\n✓ Sintaxis correcta.\n")
        else:
            print("\n✗ Se encontraron errores:\n")
            print(result.error)

        return True

    if command.startswith("/run "):
        file_path = command[5:].strip()

        if not file_path:
            print("Debes indicar un archivo.")
            return True

        agent.executor.run_and_print(file_path)
        return True

    return None


def main():
    show_banner()

    agent = FlowNexusAgent()

    print("Escribe /help para ver los comandos disponibles.")
    print("Escribe /exit para salir.\n")

    while True:
        try:
            user_input = input("Tú → ").strip()

            if not user_input:
                continue

            if user_input.startswith("/"):
                result = handle_command(agent, user_input)

                if result is False:
                    break

                if result is True:
                    continue

                print("Comando desconocido. Escribe /help.")
                continue

            agent.remember(
                role="user",
                content=user_input
            )

            print(
                "\n[FlowNexus] "
                "Todavía no tengo conectado el modelo de IA."
            )

            print(
                "La estructura del agente ya está preparada "
                "para conectarlo.\n"
            )

        except KeyboardInterrupt:
            print("\n\nFlowNexus detenido.")
            break

        except EOFError:
            print("\n\nFlowNexus detenido.")
            break

        except Exception as error:
            print(
                f"\n[ERROR] {error}\n"
            )


if __name__ == "__main__":
    main()
