import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from config import WORKSPACE_DIR


@dataclass
class ExecutionResult:
    success: bool
    output: str
    error: str
    return_code: int | None


class CodeExecutor:
    """
    Ejecuta archivos Python dentro del workspace de FlowNexus.

    IMPORTANTE:
    Este ejecutor tiene controles básicos, pero no constituye
    un sandbox de seguridad completo.
    """

    def __init__(self, workspace: Path = WORKSPACE_DIR, timeout: int = 20):
        self.workspace = Path(workspace).resolve()
        self.timeout = timeout

        self.workspace.mkdir(parents=True, exist_ok=True)

    def _validate_file(self, file_path: str | Path) -> Path:
        """
        Comprueba que el archivo esté dentro de workspace/
        y que tenga extensión .py.
        """

        path = Path(file_path)

        if not path.is_absolute():
            path = self.workspace / path

        path = path.resolve()

        try:
            path.relative_to(self.workspace)
        except ValueError:
            raise ValueError(
                "El archivo está fuera del directorio workspace."
            )

        if path.suffix.lower() != ".py":
            raise ValueError(
                "FlowNexus solo puede ejecutar archivos .py."
            )

        if not path.exists():
            raise FileNotFoundError(
                f"No existe el archivo: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"La ruta no corresponde a un archivo: {path}"
            )

        return path

    def check_syntax(self, file_path: str | Path) -> ExecutionResult:
        """
        Comprueba la sintaxis del archivo sin ejecutarlo.
        """

        try:
            path = self._validate_file(file_path)

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "py_compile",
                    str(path),
                ],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.workspace,
            )

            if result.returncode == 0:
                return ExecutionResult(
                    success=True,
                    output="Sintaxis correcta.",
                    error="",
                    return_code=0,
                )

            return ExecutionResult(
                success=False,
                output=result.stdout,
                error=result.stderr,
                return_code=result.returncode,
            )

        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="",
                error="La comprobación de sintaxis excedió el tiempo límite.",
                return_code=None,
            )

        except Exception as error:
            return ExecutionResult(
                success=False,
                output="",
                error=str(error),
                return_code=None,
            )

    def run(self, file_path: str | Path) -> ExecutionResult:
        """
        Ejecuta un archivo Python dentro de workspace/.
        """

        try:
            path = self._validate_file(file_path)

            syntax_result = self.check_syntax(path)

            if not syntax_result.success:
                return syntax_result

            environment = {
                "PATH": os.environ.get("PATH", ""),
                "PYTHONIOENCODING": "utf-8",
            }

            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    str(path),
                ],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.workspace,
                env=environment,
            )

            return ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                return_code=result.returncode,
            )

        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="",
                error=(
                    f"La ejecución superó el límite de "
                    f"{self.timeout} segundos."
                ),
                return_code=None,
            )

        except Exception as error:
            return ExecutionResult(
                success=False,
                output="",
                error=str(error),
                return_code=None,
            )

    def run_and_print(self, file_path: str | Path) -> ExecutionResult:
        """
        Ejecuta el archivo y muestra el resultado en pantalla.
        """

        result = self.run(file_path)

        print("\n========== FLOWNEXUS EXECUTOR ==========\n")

        if result.success:
            print("✓ Ejecución completada correctamente.")

            if result.output:
                print("\n--- SALIDA ---")
                print(result.output)

        else:
            print("✗ La ejecución terminó con errores.")

            if result.output:
                print("\n--- SALIDA ---")
                print(result.output)

            if result.error:
                print("\n--- ERROR ---")
                print(result.error)

        print("\n========================================\n")

        return result
