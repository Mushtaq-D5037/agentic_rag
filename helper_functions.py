import project_path
import pandas as pd
from src.config import USERS_FILE, FEATURES_FILE, LICENSE_COSTS, INACTIVE_THRESHOLD_DAYS, NEW_HIRE_GRACE_PERIOD_DAYS
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def load_and_merge_data():
    """
    Load user licenses and premium features data, merge them
    Returns:pd.DataFrame: Merged dataset with all user information
    """
    try:
        users_df = pd.read_csv(USERS_FILE)
        features_df = pd.read_csv(FEATURES_FILE)
        
        merged_df = users_df.merge(features_df, on='userPrincipalName', how='left')
        
        merged_df['licenseName'] = merged_df['assignedLicenses'].map(
            lambda x: LICENSE_COSTS.get(x, {}).get('name', 'Unknown')
        )
        
        merged_df['lastSignInDateTime'] = pd.to_datetime(merged_df['lastSignInDateTime'], errors='coerce')
        merged_df['createdDateTime'] = pd.to_datetime(merged_df['createdDateTime'], errors='coerce')
        merged_df['licenseAssignedDate'] = pd.to_datetime(merged_df['licenseAssignedDate'], errors='coerce')
        
        bool_columns = ['accountEnabled', 'audioConferencingUsed', 'vivaInsightsActive']
        for col in bool_columns:
            if col in merged_df.columns:
                merged_df[col] = merged_df[col].map(
                    lambda x: str(x).lower() == 'true' if pd.notna(x) else False
                )
        
        # print(f"Loaded {len(merged_df)} users")
        # print(f"E5 licenses: {len(merged_df[merged_df['licenseName'] == 'E5'])}")
        # print(f"E3 licenses: {len(merged_df[merged_df['licenseName'] == 'E3'])}")
        
        return merged_df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        raise



def identify_zombie_accounts(df):
    """
    Find disabled accounts that still hold licenses (zombie accounts)
    
    Args:
    df: User dataframe
    
    Returns:
    pd.DataFrame: Zombie accounts
    """
    df_z = df[(df['accountEnabled'] == False) & (df['licenseName'].notna())].copy()
    
    # Add recommendation
    df_z['recommendation'] = 'IMMEDIATE: Deprovision license from disabled account'
    df_z['priority'] = 'CRITICAL'
    
    # print(f"Found {len(df_z)} zombie accounts")
    
    return df_z


def identify_inactive_users(df, days=INACTIVE_THRESHOLD_DAYS):
    """
    Find users who haven't logged in for N days
    Excludes: users on leave (OOO), recent hires, disabled accounts
    
    Args:
        df: User dataframe
        days: Threshold for inactivity
        
    Returns:
        pd.DataFrame: Inactive users
    """
    
    UTC = ZoneInfo("UTC")

    now_utc = datetime.now(tz=UTC)
    cutoff_date = now_utc - timedelta(days=days)
    new_hire_cutoff = now_utc - timedelta(days=NEW_HIRE_GRACE_PERIOD_DAYS)
    
    # Filter criteria
    inactive = df[
        # Must be enabled
        (df['accountEnabled'] == True) &
        # Not on leave
        (df['outOfOfficeStatus'] != 'scheduled') &
        # Not a recent hire
        (df['createdDateTime'] < new_hire_cutoff) &
        # Either no last sign in, or last sign in before cutoff
        (
            (df['lastSignInDateTime'].isna()) | 
            (df['lastSignInDateTime'] < cutoff_date)
        )
    ].copy()
    
    # Calculate days inactive
    def calc_days_inactive(row):
        if pd.isna(row['lastSignInDateTime']):
            return "Never logged in"
        else:
            days = (now_utc - row['lastSignInDateTime']).days
            return f"{days} days"
    
    inactive['daysInactive'] = inactive.apply(calc_days_inactive, axis=1)
    inactive['recommendation'] = f'REVIEW: No login activity in {days}+ days. Verify with manager before action.'
    inactive['priority'] = 'HIGH'
    
    print(f"  Found {len(inactive)} inactive users (>{days} days, excluding recent hires & OOO)")
    
    return inactive

