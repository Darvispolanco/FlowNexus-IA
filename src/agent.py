from typing import Optional

from executor import CodeExecutor, ExecutionResult
from memory import Memory
from researcher import SearchResult, WebResearcher, format_results


class FlowNexusAgent:
    """
    Agente principal de FlowNexus AI.

    Coordina:
    - Memoria
    - Investigación web
    - Ejecución de código

    La conexión con el modelo de IA se agregará posteriormente.
    """

    def __init__(self):
        self.memory = Memory()
        self.researcher = WebResearcher()
        self.executor = CodeExecutor()

    # ==========================================================
    # MEMORIA
    # ==========================================================

    def remember(self, role: str, content: str):
        """
        Guarda un mensaje en la memoria.
        """

        self.memory.add_message(
            role=role,
            content=content
        )

    def get_memory(self, limit: int = 20):
        """
        Obtiene los últimos mensajes almacenados.
        """

        return self.memory.get_recent_messages(limit)

    def clear_memory(self):
        """
        Borra toda la memoria de conversación.
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
        Realiza una búsqueda en la web.
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
        en un formato que posteriormente podrá
        utilizar el modelo de IA.
        """

        results = self.search(
            query=query,
            max_results=max_results
        )

        return format_results(results)

    # ==========================================================
    # LECTURA DE PÁGINAS
    # ==========================================================

    def read_url(
        self,
        url: str,
        max_chars: int = 20000
    ) -> Optional[str]:
        """
        Lee el contenido textual de una página web.
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
        Ejecuta un archivo Python dentro de workspace/.
        """

        return self.executor.run(
            file_path
        )

    # ==========================================================
    # INFORMACIÓN DEL AGENTE
    # ==========================================================

    def status(self):
        """
        Muestra el estado actual de FlowNexus.
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
            f"Buscador web: "
            f"{type(self.researcher).__name__}"
        )

        print(
            f"Ejecutor: "
            f"{type(self.executor).__name__}"
        )

        print("\n======================================\n")
