import json

from src.memory import Memory


def test_memory_creates_file(tmp_path):
    memory_file = tmp_path / "memory.json"

    memory = Memory(memory_file)

    assert memory_file.exists()
    assert memory.load() == []


def test_add_message(tmp_path):
    memory_file = tmp_path / "memory.json"

    memory = Memory(memory_file)

    memory.add_message(
        role="user",
        content="Hola FlowNexus"
    )

    messages = memory.load()

    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hola FlowNexus"


def test_get_messages(tmp_path):
    memory_file = tmp_path / "memory.json"

    memory = Memory(memory_file)

    memory.add_message(
        role="user",
        content="Primer mensaje"
    )

    memory.add_message(
        role="assistant",
        content="Primera respuesta"
    )

    messages = memory.get_messages()

    assert messages == [
        {
            "role": "user",
            "content": "Primer mensaje"
        },
        {
            "role": "assistant",
            "content": "Primera respuesta"
        }
    ]


def test_get_recent_messages(tmp_path):
    memory_file = tmp_path / "memory.json"

    memory = Memory(memory_file)

    for number in range(10):
        memory.add_message(
            role="user",
            content=f"Mensaje {number}"
        )

    recent = memory.get_recent_messages(
        limit=3
    )

    assert len(recent) == 3
    assert recent[0]["content"] == "Mensaje 7"
    assert recent[1]["content"] == "Mensaje 8"
    assert recent[2]["content"] == "Mensaje 9"


def test_memory_count(tmp_path):
    memory_file = tmp_path / "memory.json"

    memory = Memory(memory_file)

    memory.add_message(
        role="user",
        content="Uno"
    )

    memory.add_message(
        role="assistant",
        content="Dos"
    )

    assert memory.count() == 2


def test_clear_memory(tmp_path):
    memory_file = tmp_path / "memory.json"

    memory = Memory(memory_file)

    memory.add_message(
        role="user",
        content="Mensaje"
    )

    assert memory.count() == 1

    memory.clear()

    assert memory.count() == 0
    assert memory.load() == []


def test_memory_file_contains_valid_json(tmp_path):
    memory_file = tmp_path / "memory.json"

    memory = Memory(memory_file)

    memory.add_message(
        role="user",
        content="Prueba JSON"
    )

    content = memory_file.read_text(
        encoding="utf-8"
    )

    data = json.loads(content)

    assert isinstance(data, list)
    assert data[0]["content"] == "Prueba JSON"
