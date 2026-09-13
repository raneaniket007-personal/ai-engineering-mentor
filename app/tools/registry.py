from app.tools.base import ToolDefinition
from app.tools.knowledge import SearchKnowledgeArgs, search_knowledge


SEARCH_KNOWLEDGE = ToolDefinition(
    name="search_knowledge",
    description="Search the AI engineering knowledge base.",
    function=search_knowledge,
    args_schema=SearchKnowledgeArgs,
)

TOOLS: dict[str, ToolDefinition] = {
    SEARCH_KNOWLEDGE.name: SEARCH_KNOWLEDGE,
}