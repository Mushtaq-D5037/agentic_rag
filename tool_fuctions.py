def identify_zombie_accounts(df):
    """
    Find disabled accounts that still hold licenses
    
    Args:
        df: User dataframe
        
    Returns:
        pd.DataFrame: Zombie accounts
    """
    zombies = df[df['accountEnabled'] == False].copy()
    
    # Add recommendation
    zombies['recommendation'] = 'IMMEDIATE: Deprovision license from disabled account'
    zombies['priority'] = 'CRITICAL'
    
    print(f"  Found {len(zombies)} zombie accounts")
    
    return zombies

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
    from zoneinfo import ZoneInfo

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

def identify_e5_downgrade_candidates(df):
    """
    Find E5 users with zero premium feature usage
    Excludes: Executives, certain departments
    
    Args:
        df: User dataframe
        
    Returns:
        pd.DataFrame: Downgrade candidates
    """
    # Filter to E5 users only
    e5_users = df[df['assignedLicenses'] == LICENSE_SKUS['E5']].copy()
    
    # Identify zero premium usage
    zero_usage = e5_users[
        (e5_users['pstnCallMinutes30d'] == 0) &
        (e5_users['audioConferencingUsed'] == False) &
        (e5_users['powerBIAccessCount'] == 0) &
        (e5_users['advancedThreatAlerts'] == 0) &
        (e5_users['eDiscoveryCases'] == 0) &
        (e5_users['dlpPoliciesApplied'] == 0) &
        (e5_users['informationProtectionLabels'] == 0)
    ].copy()
    
    # Exclude executives (they may legitimately have low usage)
    def is_executive(job_title):
        if pd.isna(job_title):
            return False
        return any(keyword in str(job_title) for keyword in EXECUTIVE_KEYWORDS)
    
    zero_usage['isExecutive'] = zero_usage['jobTitle'].apply(is_executive)
    
    # Separate executives for manual review
    exec_candidates = zero_usage[zero_usage['isExecutive'] == True].copy()
    non_exec_candidates = zero_usage[zero_usage['isExecutive'] == False].copy()
    
    # Add recommendations
    non_exec_candidates['recommendation'] = 'DOWNGRADE: E5→E3. Zero premium features used in 30 days.'
    non_exec_candidates['priority'] = 'MEDIUM'
    non_exec_candidates['monthlySavings'] = 21  # $57 - $36
    non_exec_candidates['annualSavings'] = 252
    
    exec_candidates['recommendation'] = 'REVIEW: Executive with zero E5 usage. Manual review recommended.'
    exec_candidates['priority'] = 'LOW'
    exec_candidates['monthlySavings'] = 21
    exec_candidates['annualSavings'] = 252
    
    # Combine (but flag separately)
    all_candidates = pd.concat([non_exec_candidates, exec_candidates], ignore_index=True)
    
    print(f"  Found {len(non_exec_candidates)} clear downgrade candidates")
    print(f"  Found {len(exec_candidates)} executive accounts for manual review")
    
    return all_candidates

def calculate_savings(downgrade_df):
    """
    Calculate total cost savings from E5→E3 downgrades
    
    Args:
        downgrade_df: DataFrame of downgrade candidates
        
    Returns:
        dict: Savings breakdown
    """
    count = len(downgrade_df)
    
    # Cost difference E5 vs E3
    e5_cost = LICENSE_COSTS[LICENSE_SKUS['E5']]['monthly']
    e3_cost = LICENSE_COSTS[LICENSE_SKUS['E3']]['monthly']
    savings_per_user = e5_cost - e3_cost
    
    monthly_savings = count * savings_per_user
    annual_savings = monthly_savings * 12
    
    return {
        "count": count,
        "savings_per_user_monthly": savings_per_user,
        "total_monthly_savings": monthly_savings,
        "total_annual_savings": annual_savings
    }

def analyze_department_waste(df, department):
    """
    Analyze license waste for a specific department
    
    Args:
        df: User dataframe
        department: Department name
        
    Returns:
        dict: Department-specific findings
    """
    dept_df = df[df['department'] == department].copy()
    
    zombies = identify_zombie_accounts(dept_df)
    inactive = identify_inactive_users(dept_df)
    downgrades = identify_e5_downgrade_candidates(dept_df)
    
    return {
        "department": department,
        "total_users": len(dept_df),
        "zombies": len(zombies),
        "inactive": len(inactive),
        "downgrades": len(downgrades),
        "potential_savings": calculate_savings(downgrades)
    }
