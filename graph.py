import operator
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import check_k8s_health, analyze_error_pattern, get_hindsight_memory

class State(TypedDict):
    messages: Annotated[List, operator.add]

# Logic: Gemini 1.5 Flash using the tools we defined
tools = [check_k8s_health, analyze_error_pattern, get_hindsight_memory]
MODEL_NAME = "gemini-flash-latest"
model = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0).bind_tools(tools)

def call_model(state: State):
    return {"messages": [model.invoke(state["messages"])]}

workflow = StateGraph(State)
workflow.add_node("investigator", call_model)
workflow.add_node("action", ToolNode(tools))

workflow.set_entry_point("investigator")

def should_continue(state: State):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "action"
    return END

workflow.add_conditional_edges("investigator", should_continue)
workflow.add_edge("action", "investigator")

app = workflow.compile()