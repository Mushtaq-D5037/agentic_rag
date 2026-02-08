import project_path
from langchain_core.tools import tool
import pandas as pd
from src.config import USERS_FILE, FEATURES_FILE, LICENSE_COSTS
from src.helper_functions import identify_zombie_accounts, load_and_merge_data
from src.helper_functions import identify_inactive_users


@tool
def tool_identify_zombie_accounts(state) -> dict:
    """
    Identify zombie accounts from the loaded dataframe.
    """
    print('calling tool_identify_zombie_accounts...')
    df = load_and_merge_data()
    zombies = identify_zombie_accounts(df)
    return {
        "messages": [f"There are {len(zombies)} zombie accounts."],
    }


@tool
def tool_identify_inactive_users(state) -> dict:
    """
    Identify inactive users from the loaded dataframe.
    """
    print('calling tool_identify_inactive_users...')

    df = load_and_merge_data()
    inactive = identify_inactive_users(df)
    return {
        "messages": [f"There are {len(inactive)} inactive users."],
    }
