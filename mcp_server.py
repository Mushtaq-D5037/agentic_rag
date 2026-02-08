# mcp_server.py
from fastapi import FastAPI
import pandas as pd
from src.helper_functions import load_and_merge_data, identify_zombie_accounts, identify_inactive_users
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Usage Analysis MCP Server")

# ---------------------------
# Global state (cached data)
# ---------------------------
DATA = None

# ---------------------------
# Endpoint: load data
# ---------------------------
@app.post("/load_data")
def load_data_endpoint():
    global DATA
    DATA = load_and_merge_data()
    return {"status": "ok", "rows_loaded": len(DATA)}

# ---------------------------
# Endpoint: identify zombie accounts
# ---------------------------
@app.post("/identify_zombie_accounts")
def identify_zombies_endpoint():
    global DATA
    if DATA is None:
        return {"error": "No data loaded. Call /load_data first."}

    zombies = identify_zombie_accounts(DATA)
    return {
        "num_zombies": len(zombies),
        # "preview": zombies.head(5).to_dict(orient="records")
    }

# ---------------------------
# Endpoint: identify inactive users
# ---------------------------
@app.post("/identify_inactive_users")
def identify_inactive_users_endpoint():
    global DATA
    if DATA is None:
        return {"error": "No data loaded. Call /load_data first."}

    inactive = identify_inactive_users(DATA)
    return {
        "num_inactive": len(inactive),
        # "preview": inactive.head(5).to_dict(orient="records")
    }

if __name__ == "__main__":
    

    print("="*80)
    print("STARTING MCP SERVER")
    print("="*80)
    print("\nAvailable Tools:")
    print(" POST /load_data          - Load user data")
    print(" POST /identify_zombie_accounts - Find zombie accounts")
    print(" POST /identify_inactive_users  - Find inactive users")
    print("\n" + "="*80)
    print("\nStarting server at http://localhost:8000")
    print("API docs at http://localhost:8000/docs\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)