KNOWLEDGE = [
    {
        "topic": "rag",
        "content": (
            "Retrieval-Augmented Generation (RAG) combines information "
            "retrieval with language generation. A retrieval system finds "
            "relevant documents, and the language model uses those documents "
            "to generate a grounded response."
        ),
    },
    {
        "topic": "agents",
        "content": (
            "An AI agent is a system that uses an AI model to reason about "
            "a goal, decide what actions to take, use tools, observe results, "
            "and continue working until the goal is completed."
        ),
    },
    {
        "topic": "tool calling",
        "content": (
            "Tool calling allows an AI model to request that an external "
            "function be executed. The application executes the function "
            "and sends the result back to the model."
        ),
    },
    {
        "topic": "agent loops",
        "content": (
            "An agent loop generally consists of reasoning about the current "
            "state, taking an action such as calling a tool, observing the "
            "result, and deciding what to do next."
        ),
    },
]


def search_knowledge(query: str) -> str:
    """
    Search the AI engineering knowledge base.

    Args:
        query: A short natural-language query describing the
            AI engineering concept or information to find.
    """

    query_words = set(query.lower().split())

    matches = []

    for item in KNOWLEDGE:
        searchable_text = (
            f"{item['topic']} {item['content']}"
        ).lower()

        text_words = set(searchable_text.split())

        if query_words & text_words:
            matches.append(item["content"])

    if not matches:
        return "No relevant information was found."

    return "\n\n".join(matches)