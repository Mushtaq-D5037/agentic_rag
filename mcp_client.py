# mcp_client.py
import requests

BASE_URL = "http://127.0.0.1:8000"

class MCPClient:
    def __init__(self):
        self.data_loaded = False

    def load_data(self):
        res = requests.post(f"{BASE_URL}/load_data").json()
        if res.get("status") == "ok":
            self.data_loaded = True
        return res

    def identify_zombie_accounts(self):
        if not self.data_loaded:
            self.load_data()
        res = requests.post(f"{BASE_URL}/identify_zombie_accounts").json()
        return res

    def identify_inactive_users(self):
        if not self.data_loaded:
            self.load_data()
        res = requests.post(f"{BASE_URL}/identify_inactive_users").json()
        return res
