import json
from datetime import datetime
from pathlib import Path

from .config import MEMORY_FILE


# ============================================================
# MEMORIA DE FLOWNEXUS
# ============================================================

class Memory:
    """
    Sistema básico de memoria de FlowNexus.

    Guarda las conversaciones en un archivo JSON
    para poder recuperarlas posteriormente.
    """

    def __init__(self, memory_file: Path = MEMORY_FILE):
        self.memory_file = Path(memory_file)

        self._ensure_memory_file()

    # --------------------------------------------------------
    # CREAR ARCHIVO DE MEMORIA
    # --------------------------------------------------------

    def _ensure_memory_file(self):
        """
        Crea el directorio y archivo de memoria
        si todavía no existen.
        """

        self.memory_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.memory_file.exists():

            self.memory_file.write_text(
                "[]",
                encoding="utf-8"
            )

    # --------------------------------------------------------
    # CARGAR MEMORIA
    # --------------------------------------------------------

    def load(self):
        """
        Carga todas las conversaciones guardadas.
        """

        try:

            content = self.memory_file.read_text(
                encoding="utf-8"
            )

            data = json.loads(content)

            if isinstance(data, list):
                return data

            return []

        except (
            json.JSONDecodeError,
            OSError
        ):

            return []

    # --------------------------------------------------------
    # GUARDAR MEMORIA
    # --------------------------------------------------------

    def save(self, memories):
        """
        Guarda la memoria completa.
        """

        self.memory_file.write_text(
            json.dumps(
                memories,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )

    # --------------------------------------------------------
    # AGREGAR MENSAJE
    # --------------------------------------------------------

    def add_message(
        self,
        role: str,
        content: str
    ):
        """
        Agrega un mensaje a la memoria.

        role:
            user
            assistant
            system
        """

        memories = self.load()

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        memories.append(message)

        self.save(memories)

    # --------------------------------------------------------
    # OBTENER HISTORIAL
    # --------------------------------------------------------

    def get_messages(self):
        """
        Devuelve los mensajes guardados
        en un formato compatible con el agente.
        """

        memories = self.load()

        messages = []

        for memory in memories:

            messages.append({
                "role": memory["role"],
                "content": memory["content"]
            })

        return messages

    # --------------------------------------------------------
    # OBTENER ÚLTIMOS MENSAJES
    # --------------------------------------------------------

    def get_recent_messages(
        self,
        limit: int = 20
    ):
        """
        Devuelve solamente los últimos mensajes.
        """

        messages = self.get_messages()

        return messages[-limit:]

    # --------------------------------------------------------
    # LIMPIAR MEMORIA
    # --------------------------------------------------------

    def clear(self):
        """
        Elimina todo el historial.
        """

        self.save([])

    # --------------------------------------------------------
    # CONTAR MENSAJES
    # --------------------------------------------------------

    def count(self):
        """
        Devuelve la cantidad de mensajes almacenados.
        """

        return len(self.load())

    # --------------------------------------------------------
    # MOSTRAR MEMORIA
    # --------------------------------------------------------

    def show(self):
        """
        Muestra el historial almacenado.
        """

        memories = self.load()

        if not memories:

            print("La memoria está vacía.")

            return

        print("\n========== MEMORIA ==========\n")

        for memory in memories:

            role = memory.get(
                "role",
                "unknown"
            )

            content = memory.get(
                "content",
                ""
            )

            print(
                f"[{role.upper()}]"
            )

            print(content)

            print("-" * 50)

        print()
