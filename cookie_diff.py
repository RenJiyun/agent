"""
compare the cookies before and after the user login
the cookies before login is saved in cookies_login_before.json
the cookies after login is saved in cookies_login_after.json
and the cookies_before and cookies_after are list, so we need to convert them to dict
"""

import json

# Load cookies from JSON files
with open('cookies_login_before.json', 'r') as f:
    cookies_before = {cookie['name']: cookie['value'] for cookie in json.load(f)}



with open('cookies_login_after.json', 'r') as f:
    cookies_after = {cookie['name']: cookie['value'] for cookie in json.load(f)}

# Compare cookies
new_cookies = {k: v for k, v in cookies_after.items() if k not in cookies_before or cookies_before[k] != v}
deleted_cookies = {k: v for k, v in cookies_before.items() if k not in cookies_after}
unchanged_cookies = {k: v for k, v in cookies_before.items() if k in cookies_after and cookies_after[k] == v}

# Print results
print("New or modified cookies:")
for k, v in new_cookies.items():
    print(f"  {k}: {v}")

print("\nDeleted cookies:")
for k, v in deleted_cookies.items():
    print(f"  {k}: {v}")

print(f"\nUnchanged cookies: {len(unchanged_cookies)}")


