
from langgraph.graph import StateGraph, END
from langchain_community.chat_models import ChatOllama
from chatbot.tools import predict_employee_attrition
from typing import TypedDict
import json
import re

# ✅ Local LLM
llm = ChatOllama(model="phi3", temperature=0)


# ✅ State Definition
class State(TypedDict):
    input: str
    decision: str
    output: str


# 🧠 Decision Node
def llm_node(state: State):
    query = state["input"]

    prompt = f"""
    Classify the query:
    - If user wants prediction → return "predict"
    - Otherwise → return "info"

    Only return one word.

    Query: {query}
    """

    decision = llm.invoke(prompt).content.strip().lower()
    return {"decision": decision}



def extract_features_llm(query):
    prompt = f"""
    Extract employee details from the text.

    Return ONLY JSON. No explanation.

    Format:
    {{
      "satisfaction_level": float,
      "last_evaluation": float,
      "number_project": int,
      "average_montly_hours": int,
      "time_spend_company": int,
      "department": "sales",
      "salary": "low/medium/high"
    }}

    If missing values, use defaults.

    Text: {query}
    """

    try:
        response = llm.invoke(prompt).content

        # ✅ Extract JSON safely
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    
    try:
        # satisfaction (handles "is", "=", etc.)
        sat_match = re.search(r"satisfaction\s*(?:=|is)?\s*([\d.]+)", query, re.IGNORECASE)
        satisfaction = float(sat_match.group(1)) if sat_match else 0.5

        # hours
        hours_match = re.search(r"(\d+)\s*hours", query, re.IGNORECASE)
        hours = int(hours_match.group(1)) if hours_match else 200

        # projects
        proj_match = re.search(r"(\d+)\s*project", query, re.IGNORECASE)
        projects = int(proj_match.group(1)) if proj_match else 4

        # years
        year_match = re.search(r"(\d+)\s*year", query, re.IGNORECASE)
        years = int(year_match.group(1)) if year_match else 3

        # salary
        if "low" in query.lower():
            salary = "low"
        elif "high" in query.lower():
            salary = "high"
        else:
            salary = "medium"

        return {
            "satisfaction_level": satisfaction,
            "last_evaluation": 0.7,
            "number_project": projects,
            "average_montly_hours": hours,
            "time_spend_company": years,
            "department": "sales",
            "salary": salary
        }

    except:
        return None


# 🔧 Tool Node (Prediction + Explanation)
def tool_node(state: State):
    query = state["input"]

    features = extract_features_llm(query)

    if not features:
        return {
            "output": "❌ Could not understand input. Try: satisfaction=0.3, 220 hours, low salary"
        }

    result = predict_employee_attrition.invoke(features)

    explain_prompt = f"""
    Explain this prediction in simple HR terms in 2-3 bullet points.

    Input: {features}
    Result: {result}
    """

    explanation = llm.invoke(explain_prompt).content

    final_output = f"{result}\n\n📊 Explanation:\n{explanation}"

    return {"output": final_output}


#  knowledge_node
def knowledge_node(state: State):
    query = state["input"]

    prompt = f"""
    You are an HR analytics expert.

    Give a clear, structured answer in 4-5 bullet points.

    Use strong, professional wording.
    Keep each point concise and impactful.

    Question: {query}
    """

    response = llm.invoke(prompt).content

    return {"output": response}


# 🔀 Router
def route(state: State):
    return "tool" if "predict" in state["decision"] else "knowledge"


# 🏗️ Build Graph
def build_graph():
    graph = StateGraph(State)

    graph.add_node("llm", llm_node)
    graph.add_node("tool", tool_node)
    graph.add_node("knowledge", knowledge_node)

    graph.set_entry_point("llm")

    graph.add_conditional_edges("llm", route, {
        "tool": "tool",
        "knowledge": "knowledge"
    })

    graph.add_edge("tool", END)
    graph.add_edge("knowledge", END)

    return graph.compile()