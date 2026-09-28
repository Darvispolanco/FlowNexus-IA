from src.researcher import (
    SearchResult,
    WebResearcher,
    format_results,
)


def test_search_result_creation():
    result = SearchResult(
        title="Python",
        url="https://www.python.org/",
        description="Lenguaje de programación Python."
    )

    assert result.title == "Python"
    assert result.url == "https://www.python.org/"
    assert result.description == "Lenguaje de programación Python."


def test_format_results_with_results():
    results = [
        SearchResult(
            title="Python",
            url="https://www.python.org/",
            description="Página oficial de Python."
        ),
        SearchResult(
            title="Documentación",
            url="https://docs.python.org/",
            description="Documentación oficial."
        ),
    ]

    formatted = format_results(results)

    assert "FUENTE 1" in formatted
    assert "FUENTE 2" in formatted
    assert "Python" in formatted
    assert "https://www.python.org/" in formatted
    assert "Documentación" in formatted


def test_format_results_without_results():
    formatted = format_results([])

    assert formatted == "No se encontraron resultados."


def test_invalid_url():
    researcher = WebResearcher()

    assert researcher.fetch_page(
        "esto-no-es-una-url"
    ) is None


def test_invalid_url_scheme():
    researcher = WebResearcher()

    assert researcher.fetch_page(
        "ftp://example.com"
    ) is None


def test_extract_text():
    researcher = WebResearcher()

    html = """
    <html>
        <head>
            <title>Prueba</title>
            <script>
                console.log("No debería aparecer");
            </script>
        </head>

        <body>
            <h1>Hola FlowNexus</h1>
            <p>Este es un texto de prueba.</p>

            <footer>
                Pie de página
            </footer>
        </body>
    </html>
    """

    text = researcher.extract_text(html)

    assert "Hola FlowNexus" in text
    assert "Este es un texto de prueba." in text
    assert "console.log" not in text
    assert "Pie de página" not in text


def test_empty_html():
    researcher = WebResearcher()

    assert researcher.extract_text("") == ""


def test_read_page_invalid_url():
    researcher = WebResearcher()

    result = researcher.read_page(
        "url-invalida"
    )

    assert result is None
