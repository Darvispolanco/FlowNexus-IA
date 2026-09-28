from typing import Optional

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL, validate_config


class LLMClient:
    """
    Cliente del modelo de lenguaje de FlowNexus.

    Utiliza el SDK oficial de OpenAI y la Responses API.
    """

    def __init__(self):
        validate_config()

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

        self.model = OPENAI_MODEL

    def generate(
        self,
        prompt: str,
        instructions: Optional[str] = None
    ) -> str:
        """
        Envía una solicitud al modelo y devuelve
        únicamente el texto generado.
        """

        if not prompt.strip():
            raise ValueError(
                "El prompt no puede estar vacío."
            )

        parameters = {
            "model": self.model,
            "input": prompt,
        }

        if instructions:
            parameters["instructions"] = instructions

        response = self.client.responses.create(
            **parameters
        )

        return response.output_text

    def chat(
        self,
        messages: list[dict[str, str]]
    ) -> str:
        """
        Envía una conversación completa al modelo.
        """

        if not messages:
            raise ValueError(
                "La conversación está vacía."
            )

        response = self.client.responses.create(
            model=self.model,
            input=messages,
        )

        return response.output_text

    def test_connection(self) -> bool:
        """
        Comprueba que FlowNexus pueda comunicarse
        con el modelo.
        """

        try:
            response = self.client.responses.create(
                model=self.model,
                input="Responde únicamente: conexión correcta."
            )

            print("\nRespuesta del modelo:")
            print(response.output_text)

            return True

        except Exception as error:
            print(
                f"\n[ERROR] No se pudo conectar con el modelo: {error}"
            )

            return False
