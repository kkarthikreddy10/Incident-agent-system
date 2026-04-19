import os
import sys
from dotenv import load_dotenv

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

from graph import app
from langchain_core.messages import HumanMessage

import cascadeflow
# Initialize CascadeFlow for performance tracing, speculative execution, and model optimization
cascadeflow.init(mode='observe')

def run_incident_response(alert_text):
    print("\n" + "="*50)
    print("🚀 INCIDENT AGENT INVESTIGATION STARTING...")
    print("="*50)
    
    inputs = {"messages": [HumanMessage(content=alert_text)]}
    
    try:
        for output in app.stream(inputs):
            for key, value in output.items():
                print(f"\n[SYSTEM NODE: {key.upper()}]")
                last_msg = value["messages"][-1]
                
                if hasattr(last_msg, 'content') and last_msg.content:
                    if isinstance(last_msg.content, list):
                        text = "".join([c.get("text", "") for c in last_msg.content if isinstance(c, dict)])
                        print(f"AI: {text}")
                    else:
                        print(f"AI: {last_msg.content}")
                
                if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                    for tool in last_msg.tool_calls:
                        print(f"🛠️  EXECUTING TOOL: {tool['name']}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    run_incident_response("The billing service is down and throwing 500 errors.")