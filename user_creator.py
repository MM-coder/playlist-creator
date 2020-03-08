import users, secrets

# Recursive user creator since I'm lazy

with open('9b_acessos.txt', 'w+') as f:
    for i in range(1, 17):
        user = f"9b_{i}"
        raw = secrets.token_urlsafe(6)
        password = users.hash_plain_text(raw)
        users.create_user_if_not_exists(user, password, False)
        f.write(user + ':' + raw + '\n')

with open('9a_acessos.txt', 'w+') as f:
    for i in range(1, 18):
        user = f"9a_{i}"
        raw = secrets.token_urlsafe(6)
        password = users.hash_plain_text(raw)
        users.create_user_if_not_exists(user, password, False)
        f.write(user + ':' + raw + '\n')

# Create Admin Accounts (2 teachers, 1 random admin)

with open('professores.txt', 'w+') as f:
    for i in range(1, 3):
        user = f"prof_{i}"
        raw = secrets.token_urlsafe(6)
        password = users.hash_plain_text(raw)
        users.create_user_if_not_exists(user, password, True)
        f.write(user + ':' + raw + '\n')

with open('admin.txt', 'w+') as f:
    user = "admin"
    raw = secrets.token_urlsafe(126)
    password = users.hash_plain_text(raw)
    users.create_user_if_not_exists(user, password, True)
    f.write(user + ':' + raw + '\n')