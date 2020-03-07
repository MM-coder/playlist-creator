import psycopg2, hashlib
from urllib.parse import urlparse

url = "postgres://aohxordwzsnidl:0f5b748e243026e102f27babce51623f4350524ca7122606290cc4077c1c7b1e@ec2-54-195-247-108.eu-west-1.compute.amazonaws.com:5432/dcvdo3sgqr2bea"

# Databases

result = urlparse(url)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
db = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname
)
c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Users(
                      Username TEXT,
                      Password TEXT,
                      IsAdmin BOOLEAN,
                      Submitted INTEGER)""")


# Login Functions

def create_user_if_not_exists(username: str, password: str, admin: bool):
    # Takes Username, Hashed Password, Admin Status and creates a user
    c.execute("SELECT COUNT(*) FROM Users WHERE Username=%s", (str(username),))
    user_count = c.fetchone()[0]
    if user_count < 1:
        print("[Users Table] Creating user with  " + str(username))
        c.execute("INSERT INTO Users VALUES (%s, %s, %s, %s)", (str(username), str(password), bool(admin), 0))
        db.commit()

def get_password(username: str):
    # Returns hashed password stored in dB for comparison
    c.execute("SELECT Password FROM Users WHERE Username=%s", (str(username),))
    password = str(c.fetchone()[0])
    db.commit()
    return password

def get_admin_status(username: str):
    # Returns admin status (in Boolean) for permissions 
    c.execute("SELECT IsAdmin FROM Users WHERE Username=%s", (str(username),))
    admin = bool(c.fetchone()[0])
    db.commit()
    return admin

def hash_plain_text(string: str):
    # Hashes plain text (for external use) to pass as argument for comparison
    hash_object = hashlib.md5(string.encode())
    return hash_object.hexdigest()
