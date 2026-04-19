from langchain_core.tools import tool

@tool
def check_k8s_health(service_name: str):
    """Query Kubernetes for pod status."""
    if "billing" in service_name.lower():
        return f"Status for {service_name}: Pod 'billing-v2' is in CrashLoopBackOff. Restart count: 15."
    return f"Status for {service_name}: All pods running normally."

@tool
def analyze_error_pattern(logs: str):
    """Detects high-priority patterns in logs."""
    if "500" in logs or "NullPointer" in logs:
        return "Priority: High. Type: Server Error. Fix: Memory leak detected."
    return "Priority: Low. No critical patterns detected."

import os
import requests

@tool
def get_hindsight_memory(issue: str):
    """Recalls past incidents from memory."""
    hindsight_url = os.getenv("HINDSIGHT_API_URL")
    hindsight_key = os.getenv("HINDSIGHT_API_KEY")

    if hindsight_url and hindsight_key:
        try:
            # Attempt to query the external Hindsight API
            headers = {
                "Authorization": f"Bearer {hindsight_key}",
                "Content-Type": "application/json"
            }
            # Using a typical '/search' or '/query' endpoint format
            endpoint = f"{hindsight_url}/search" 
            payload = {"query": issue}
            response = requests.post(endpoint, json=payload, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    return f"Hindsight Recall (from API): {data['result']}"
                elif "data" in data and len(data["data"]) > 0:
                     return f"Hindsight Recall (from API): {data['data']}"
        except Exception as e:
            # If the external API fails (e.g. offline, mock endpoint), we silently fallback to internal memory
            pass

    # Fallback to local dict memory
    past_incidents = {"billing service": "Hindsight Recall: Last time, restarting Redis cache fixed it."}
    for key in past_incidents:
        if key in issue.lower():
            return past_incidents[key]
    return "Hindsight: No past incidents found."