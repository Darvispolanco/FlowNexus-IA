from typing import Optional

from typing import Optional

from .executor import CodeExecutor, ExecutionResult
from .llm import LLMClient
from .memory import Memory
from .prompts import SYSTEM_PROMPT
from .researcher import SearchResult, WebResearcher, format_results

class FlowNexusAgent:
    """
    Agente principal de FlowNexus AI.

    Coordina:

    - Modelo de IA
    - Memoria
    - Investigación web
    - Ejecución de código
    """

    def __init__(self):
        self.memory = Memory()
        self.researcher = WebResearcher()
        self.executor = CodeExecutor()
        self.llm = LLMClient()

    # ==========================================================
    # CONVERSACIÓN CON EL MODELO
    # ==========================================================

    def ask(self, prompt: str) -> str:
        """
        Envía una pregunta al modelo utilizando
        el historial reciente de conversación.
        """

        if not prompt.strip():
            raise ValueError(
                "El mensaje no puede estar vacío."
            )

        self.remember(
            role="user",
            content=prompt
        )

        messages = [
            {
                "role": "developer",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(
            self.get_memory(limit=20)
        )

        response = self.llm.chat(messages)

        self.remember(
            role="assistant",
            content=response
        )

        return response

    # ==========================================================
    # MEMORIA
    # ==========================================================

    def remember(
        self,
        role: str,
        content: str
    ):
        """
        Guarda un mensaje en la memoria.
        """

        self.memory.add_message(
            role=role,
            content=content
        )

    def get_memory(
        self,
        limit: int = 20
    ):
        """
        Obtiene los últimos mensajes.
        """

        return self.memory.get_recent_messages(
            limit
        )

    def clear_memory(self):
        """
        Elimina toda la memoria.
        """

        self.memory.clear()

    # ==========================================================
    # INVESTIGACIÓN
    # ==========================================================

    def search(
        self,
        query: str,
        max_results: Optional[int] = None
    ) -> list[SearchResult]:
        """
        Realiza una búsqueda web.
        """

        return self.researcher.search(
            query=query,
            max_results=max_results
        )

    def research(
        self,
        query: str,
        max_results: Optional[int] = None
    ) -> str:
        """
        Busca información y devuelve las fuentes
        encontradas.
        """

        results = self.search(
            query=query,
            max_results=max_results
        )

        return format_results(results)

    def read_url(
        self,
        url: str,
        max_chars: int = 20000
    ) -> Optional[str]:
        """
        Lee el contenido de una página web.
        """

        return self.researcher.read_page(
            url=url,
            max_chars=max_chars
        )

    # ==========================================================
    # EJECUCIÓN DE CÓDIGO
    # ==========================================================

    def check_code(
        self,
        file_path: str
    ) -> ExecutionResult:
        """
        Comprueba la sintaxis de un archivo Python.
        """

        return self.executor.check_syntax(
            file_path
        )

    def run_code(
        self,
        file_path: str
    ) -> ExecutionResult:
        """
        Ejecuta un archivo Python.
        """

        return self.executor.run(
            file_path
        )

    # ==========================================================
    # ESTADO
    # ==========================================================

    def status(self):
        """
        Muestra el estado del agente.
        """

        print("\n========== FLOWNEXUS STATUS ==========\n")

        print(
            f"Mensajes en memoria: "
            f"{self.memory.count()}"
        )

        print(
            f"Workspace: "
            f"{self.executor.workspace}"
        )

        print(
            f"Modelo: "
            f"{self.llm.model}"
        )

        print(
            f"Investigador: "
            f"{type(self.researcher).__name__}"
        )

        print(
            f"Ejecutor: "
            f"{type(self.executor).__name__}"
        )

        print("\n======================================\n")
