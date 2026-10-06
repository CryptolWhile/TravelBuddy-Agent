from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv
import os

load_dotenv()

model_name = os.getenv("DEFAULT_MODEL", "cx/gpt-5.6-terra")
base_url = os.getenv("BASE_URL", "")

# 1. System Prompt
with open("system_prompts.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# 3. LLM + Tools
tools_list = [search_hotels, search_flights, calculate_budget]
llm = ChatOpenAI(model=model_name, base_url=base_url)
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]

    # 1. Kiểm tra an toàn để tránh IndexError và đảm bảo có System Prompt
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    # 2. Gọi LLM
    response = llm_with_tools.invoke(messages)

    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Call tool: {tc['name']} ({tc['args']})")
    else:
        print(f"Tra loi truc tiep")

    return {"messages": [response]}

#5 build Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy — Trợ lý Du lịch Thông minh")
    print("Gõ 'quit' để thoát")
    print("=" * 60)

    state = {"messages": []}
    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nTravelBuddy đang suy nghĩ...")
        state["messages"].append(("human", user_input))
        result = graph.invoke(state)
        state = result
        final = result["messages"][-1]
        print(f"\nTravelBuddy: {final.content}")

