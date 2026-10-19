from instagrapi import Client
from pathlib import Path
import csv
import json

ROOT = Path("../Instagram-All")
SESSION = ROOT / "instagram_session.json"

CSV_FILE = ROOT / "following.csv"
TXT_FILE = ROOT / "following.txt"
JSON_FILE = ROOT / "following.json"

if not SESSION.exists():
    raise FileNotFoundError(
        f"Session file not found: {SESSION.resolve()}"
    )

username = input("Your Instagram username: ").strip()

client = Client()
client.load_settings(SESSION)

user_id = client.user_id_from_username(username)

print("Retrieving the complete following list...")

following = client.user_following(
    user_id,
    amount=0
)

users = sorted(
    following.values(),
    key=lambda user: user.username.casefold()
)

records = []

for user in users:
    records.append({
        "username": user.username,
        "full_name": user.full_name or "",
        "profile_url": (
            f"https://www.instagram.com/{user.username}/"
        ),
        "user_id": str(user.pk),
        "is_private": bool(user.is_private),
        "is_verified": bool(user.is_verified)
    })


# Detailed CSV
with open(
    CSV_FILE,
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "username",
            "full_name",
            "profile_url",
            "user_id",
            "is_private",
            "is_verified"
        ]
    )
    writer.writeheader()
    writer.writerows(records)


# Simple readable list
with open(TXT_FILE, "w", encoding="utf-8") as file:
    for number, user in enumerate(records, start=1):
        file.write(
            f"{number}. @{user['username']}"
            f" | {user['full_name']}"
            f" | {user['profile_url']}\n"
        )


# Complete machine-readable version
with open(JSON_FILE, "w", encoding="utf-8") as file:
    json.dump(
        records,
        file,
        indent=2,
        ensure_ascii=False
    )


print(f"\nExported {len(records)} accounts.")
print(f"CSV:  {CSV_FILE.resolve()}")
print(f"Text: {TXT_FILE.resolve()}")
print(f"JSON: {JSON_FILE.resolve()}")