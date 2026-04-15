from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver

# 🔥 System prompt inside LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

# 🔥 Memory
memory = MemorySaver()

# 🔥 Create Agent (NO state_modifier)
agent = create_react_agent(
    llm,
    tools=[],
    checkpointer=memory
)