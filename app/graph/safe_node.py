from collections.abc import Callable
from typing import Any


def safe_node(
    node: Callable[..., dict],
) -> Callable[..., dict]:
    def wrapped(
        state: Any,
    ) -> dict:
        try:
            return node(state)

        except Exception as exc:
            print(
                f"\nNode failed: {exc}"
            )

            return {
                "error": str(exc),
            }

    return wrapped