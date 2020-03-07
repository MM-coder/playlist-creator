import users

# Settings
raw = "f6pYBUgCTWtyRe3VhUVrLTt22CxQAJSZ6oqQszPhGEJqm94MmzeEjKQXvcngwcoGWYBF3awaKEpjBAGKdnN4vuYMaadgqPUEocSDs428WEfikxanjKBstTAz6bxnndgE"
user ="admin"

# Logic
password = users.hash_plain_text(raw)
users.create_user_if_not_exists(user, password, True)

# Output
print("-"*32)
print("Created user!")
print(f"Username: {user}")
print(f"Password: {password}")
print("-"*32)