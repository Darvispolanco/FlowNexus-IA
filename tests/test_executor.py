from src.executor import CodeExecutor


def test_executor_creates_workspace(tmp_path):
    workspace = tmp_path / "workspace"

    executor = CodeExecutor(
        workspace=workspace
    )

    assert workspace.exists()
    assert workspace.is_dir()


def test_check_valid_python_file(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    file_path = workspace / "programa.py"

    file_path.write_text(
        'print("Hola FlowNexus")',
        encoding="utf-8"
    )

    executor = CodeExecutor(
        workspace=workspace
    )

    result = executor.check_syntax(
        file_path
    )

    assert result.success is True
    assert result.return_code == 0


def test_check_invalid_python_file(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    file_path = workspace / "error.py"

    file_path.write_text(
        'print("Hola"',
        encoding="utf-8"
    )

    executor = CodeExecutor(
        workspace=workspace
    )

    result = executor.check_syntax(
        file_path
    )

    assert result.success is False
    assert result.error


def test_run_valid_python_file(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    file_path = workspace / "programa.py"

    file_path.write_text(
        'print("FlowNexus funcionando")',
        encoding="utf-8"
    )

    executor = CodeExecutor(
        workspace=workspace
    )

    result = executor.run(
        file_path
    )

    assert result.success is True
    assert "FlowNexus funcionando" in result.output
    assert result.return_code == 0


def test_run_python_with_error(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    file_path = workspace / "error.py"

    file_path.write_text(
        """
numero = 10
resultado = numero / 0
print(resultado)
""",
        encoding="utf-8"
    )

    executor = CodeExecutor(
        workspace=workspace
    )

    result = executor.run(
        file_path
    )

    assert result.success is False
    assert result.error
    assert result.return_code != 0


def test_reject_non_python_file(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    file_path = workspace / "archivo.txt"

    file_path.write_text(
        "Hola",
        encoding="utf-8"
    )

    executor = CodeExecutor(
        workspace=workspace
    )

    try:
        executor.run(file_path)
        assert False, "Debió rechazar el archivo"
    except ValueError as error:
        assert ".py" in str(error)


def test_reject_file_outside_workspace(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    outside_file = tmp_path / "fuera.py"

    outside_file.write_text(
        'print("Fuera")',
        encoding="utf-8"
    )

    executor = CodeExecutor(
        workspace=workspace
    )

    try:
        executor.run(outside_file)
        assert False, "Debió rechazar el archivo"
    except ValueError as error:
        assert "workspace" in str(error)


def test_missing_file(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    executor = CodeExecutor(
        workspace=workspace
    )

    missing_file = workspace / "no_existe.py"

    try:
        executor.run(missing_file)
        assert False, "Debió detectar que el archivo no existe"
    except FileNotFoundError:
        pass
