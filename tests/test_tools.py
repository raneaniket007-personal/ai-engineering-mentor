import pytest

from app.agent.executor import ToolExecutor


def test_search_knowledge_valid_arguments() -> None:
    executor = ToolExecutor()

    result = executor.execute(
        "search_knowledge",
        {"query": "tool calling"},
    )

    assert "Tool calling" in result


def test_unknown_tool() -> None:
    executor = ToolExecutor()

    with pytest.raises(ValueError, match="Unknown tool"):
        executor.execute(
            "does_not_exist",
            {},
        )


def test_invalid_tool_arguments() -> None:
    executor = ToolExecutor()

    with pytest.raises(
        ValueError,
        match="Invalid arguments",
    ):
        executor.execute(
            "search_knowledge",
            {"wrong_parameter": "hello"},
        )

def test_invalid_arguments_type() -> None:
    executor = ToolExecutor()

    with pytest.raises(ValueError, match="Invalid arguments"):
        executor.execute(
            "search_knowledge",
            {"query": 123},
        )