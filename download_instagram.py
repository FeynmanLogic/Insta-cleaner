from instagrapi import Client
from pathlib import Path
from getpass import getpass
import json
import re
import time

OUTPUT = Path("../Instagram-All")
SESSION = OUTPUT / "instagram_session.json"


def safe_name(name):
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    return name.strip().strip(".") or "Unnamed Collection"


def download_media(client, media, folder):
    # Photo
    if media.media_type == 1:
        return client.photo_download(
            media.pk,
            folder=folder,
            overwrite=False
        )

    # Video or Reel
    if media.media_type == 2:
        if media.product_type == "clips":
            return client.clip_download(
                media.pk,
                folder=folder
            )

        return client.video_download(
            media.pk,
            folder=folder,
            overwrite=False
        )

    # Carousel or album
    if media.media_type == 8:
        return client.album_download(
            media.pk,
            folder=folder,
            overwrite=False
        )

    raise ValueError(f"Unknown media type: {media.media_type}")


# Create the main folder before saving the session
OUTPUT.mkdir(parents=True, exist_ok=True)

username = input("Instagram username: ").strip()
password = getpass("Instagram password: ")

client = Client()
client.delay_range = [2, 5]

if SESSION.exists():
    client.load_settings(SESSION)

client.login(username, password)
client.dump_settings(SESSION)

# Exclude Instagram's automatic "All posts" collection
collections = [
    collection
    for collection in client.collections()
    if collection.name.strip().casefold() != "all posts"
]

print(f"Found {len(collections)} named collections.")

for collection in collections:
    collection_name = safe_name(collection.name)
    folder = OUTPUT / collection_name
    folder.mkdir(parents=True, exist_ok=True)

    print(f"\nDownloading collection: {collection.name}")

    media_items = client.collection_medias(
        collection.id,
        amount=0
    )

    metadata = []
    index_file = folder / "index.json"

    for number, media in enumerate(media_items, start=1):
        print(f"  {number}/{len(media_items)}: {media.code}")

        record = {
            "media_pk": str(media.pk),
            "shortcode": media.code,
            "url": f"https://www.instagram.com/p/{media.code}/",
            "caption": media.caption_text,
            "owner": media.user.username if media.user else None,
            "taken_at": (
                media.taken_at.isoformat()
                if media.taken_at else None
            )
        }

        try:
            downloaded = download_media(client, media, folder)

            if isinstance(downloaded, (list, tuple)):
                record["downloaded_paths"] = [
                    str(path) for path in downloaded
                ]
            else:
                record["downloaded_paths"] = [str(downloaded)]

            record["status"] = "downloaded"

        except Exception as error:
            print(f"    Failed: {error}")
            record["status"] = "failed"
            record["error"] = str(error)

        metadata.append(record)

        # Save progress after each post
        with open(index_file, "w", encoding="utf-8") as file:
            json.dump(
                metadata,
                file,
                indent=2,
                ensure_ascii=False
            )

        time.sleep(3)

print("\nBackup complete.")
print(f"Files are in: {OUTPUT.resolve()}")