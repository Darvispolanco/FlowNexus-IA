from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

from config import MAX_SEARCH_RESULTS, REQUEST_TIMEOUT


# ============================================================
# RESULTADO DE UNA BÚSQUEDA
# ============================================================

@dataclass
class SearchResult:
    title: str
    url: str
    description: str


# ============================================================
# INVESTIGADOR WEB
# ============================================================

class WebResearcher:
    """
    Herramienta de investigación web de FlowNexus.

    Permite:
    - Buscar información pública.
    - Obtener páginas web.
    - Extraer texto.
    - Preparar fuentes para que el agente las analice.
    """

    def __init__(
        self,
        max_results: int = MAX_SEARCH_RESULTS,
        timeout: int = REQUEST_TIMEOUT
    ):
        self.max_results = max_results
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "FlowNexus/0.1 "
                "(Personal Research Agent)"
            )
        })

    # ========================================================
    # BUSCAR EN INTERNET
    # ========================================================

    def search(
        self,
        query: str,
        max_results: Optional[int] = None
    ):
        """
        Busca información pública en Internet.

        Devuelve una lista de SearchResult.
        """

        if not query.strip():
            return []

        limit = (
            max_results
            if max_results is not None
            else self.max_results
        )

        results = []

        try:

            with DDGS() as search_engine:

                search_results = search_engine.text(
                    query,
                    max_results=limit
                )

                for result in search_results:

                    title = result.get(
                        "title",
                        ""
                    )

                    url = result.get(
                        "href",
                        ""
                    )

                    description = result.get(
                        "body",
                        ""
                    )

                    if not url:
                        continue

                    results.append(
                        SearchResult(
                            title=title,
                            url=url,
                            description=description
                        )
                    )

        except Exception as error:

            print(
                f"[ERROR] No se pudo realizar "
                f"la búsqueda: {error}"
            )

        return results

    # ========================================================
    # DESCARGAR PÁGINA
    # ========================================================

    def fetch_page(
        self,
        url: str
    ) -> Optional[str]:
        """
        Descarga una página web y devuelve
        su HTML.
        """

        if not self._is_valid_url(url):

            return None

        try:

            response = self.session.get(
                url,
                timeout=self.timeout,
                allow_redirects=True
            )

            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type",
                ""
            ).lower()

            if (
                "text/html" not in content_type
                and "application/xhtml" not in content_type
            ):

                return None

            return response.text

        except requests.RequestException as error:

            print(
                f"[ERROR] No se pudo obtener "
                f"{url}: {error}"
            )

            return None

    # ========================================================
    # EXTRAER TEXTO
    # ========================================================

    def extract_text(
        self,
        html: str,
        max_chars: int = 20000
    ) -> str:
        """
        Extrae texto legible del HTML.
        """

        if not html:

            return ""

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # Eliminar elementos que normalmente
        # no contienen el contenido principal.
        for element in soup(
            [
                "script",
                "style",
                "noscript",
                "svg",
                "nav",
                "footer"
            ]
        ):

            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # Limpiar espacios repetidos.
        text = " ".join(
            text.split()
        )

        return text[:max_chars]

    # ========================================================
    # LEER PÁGINA COMPLETA
    # ========================================================

    def read_page(
        self,
        url: str,
        max_chars: int = 20000
    ) -> Optional[str]:
        """
        Descarga una página y extrae su texto.
        """

        html = self.fetch_page(url)

        if html is None:

            return None

        return self.extract_text(
            html,
            max_chars=max_chars
        )

    # ========================================================
    # INVESTIGAR
    # ========================================================

    def research(
        self,
        query: str,
        max_results: Optional[int] = None
    ):
        """
        Realiza una búsqueda y devuelve
        resultados estructurados.
        """

        return self.search(
            query,
            max_results=max_results
        )

    # ========================================================
    # VALIDAR URL
    # ========================================================

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """
        Comprueba que una URL tenga un esquema
        HTTP o HTTPS y un dominio.
        """

        try:

            parsed = urlparse(url)

            return (
                parsed.scheme in {
                    "http",
                    "https"
                }
                and bool(parsed.netloc)
            )

        except Exception:

            return False


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def format_results(
    results: list[SearchResult]
) -> str:
    """
    Convierte resultados de búsqueda
    en texto fácil de leer.
    """

    if not results:

        return "No se encontraron resultados."

    output = []

    for index, result in enumerate(
        results,
        start=1
    ):

        output.append(
            f"""
FUENTE {index}
Título: {result.title}
URL: {result.url}
Descripción: {result.description}
"""
        )

    return "\n".join(output)
