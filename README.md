# Insta-cleaner

This project downloads Instagram posts and reels that are stored inside named Saved collections. It preserves the collection structure as folders, checks the resulting indexes for failed downloads, and exports a list of accounts followed by the authenticated user.

It intentionally skips Instagram's automatic **All posts** collection. Therefore, uncategorized saved posts are not downloaded.

## Files

### `download_instagram.py`

Logs into Instagram, retrieves all named Saved collections, and downloads their contents into separate folders.

It creates an `index.json` inside each collection folder. The index contains the original Instagram URL, shortcode, owner, caption, date, downloaded paths, and download status for every item.

### `check_insta_errors.py`

Scans every `index.json` under `Instagram-All` and reports:

- the number of collection indexes found;
- the number of records checked;
- failed downloads;
- malformed or unreadable index files.

It saves the result as `Instagram-All/error_report.txt`.

### `export_following.py`

Uses the saved authenticated session to export every account currently followed by the user.

It creates:

- `following.csv`, for Excel or Google Sheets;
- `following.txt`, for a simple readable list;
- `following.json`, for machine-readable data.

## Requirements

- Windows, macOS, or Linux
- Python 3.10 or newer
- Internet access
- An active Instagram account
- Enough disk space for all selected photos, reels, videos, and carousels

Install the required Python package:

```bash
python -m pip install -U instagrapi
```

## Recommended folder layout

Place the three scripts together inside a folder such as `Code`:

```text
Desktop/
├── Code/
│   ├── download_instagram.py
│   ├── check_insta_errors.py
│   └── export_following.py
└── Instagram-All/
```

The scripts use this output path:

```python
Path("../Instagram-All")
```

Therefore, run them from inside the `Code` directory. The `Instagram-All` folder will be created beside `Code`. If the scripts are stored elsewhere, update their paths accordingly.

## Run order

### 1. Download named collections

Run:

```bash
python download_instagram.py
```

Enter the Instagram username and password when prompted. Password input remains invisible in the terminal.

Wait until the terminal prints:

```text
Backup complete.
```

The output should resemble:

```text
Instagram-All/
├── Collection A/
│   ├── downloaded media files
│   └── index.json
├── Collection B/
│   ├── downloaded media files
│   └── index.json
└── instagram_session.json
```

The program deliberately waits between requests. A large backup can take several hours. Keep the computer awake and connected to stable internet. Individual failures are recorded without stopping the remaining downloads.

### 2. Check for download errors

After the downloader finishes, run:

```bash
python check_insta_errors.py
```

A clean result should show:

```text
Failed items: 0
Unreadable index files: 0
```

Review `Instagram-All/error_report.txt`. Also open a sample of photos, reels, and carousel files manually before treating the backup as complete.

### 3. Export the following list

Run this before deleting or deactivating the Instagram account:

```bash
python export_following.py
```

Enter the username when prompted. The script reuses `instagram_session.json`, so that file must still exist and the session must remain valid.

Confirm that these files were created:

```text
Instagram-All/following.csv
Instagram-All/following.txt
Instagram-All/following.json
```

## Important limitations

This is not a complete Instagram account export. It downloads only items stored inside named Saved collections and exports the following list.

It does not automatically include:

- uncategorized saved posts from **All posts**;
- the user's own uploaded posts and reels;
- archived posts or archived stories;
- direct messages;
- followers;
- likes, comments, or account settings;
- reposts that were not also saved into a named collection.

Download any important omitted content separately before deleting the account.

## Security

`instagram_session.json` contains reusable authentication information. Treat it like a password.

- Never send, upload, commit, or share this file.
- Add it to `.gitignore` if the scripts are placed in a Git repository.
- Remove it before sharing the `Instagram-All` folder.
- Delete it after all three scripts have finished.
- If it is exposed, change the Instagram password and terminate existing sessions.

Suggested `.gitignore` entry:

```gitignore
instagram_session.json
Instagram-All/
```

## Before deleting an Instagram account

1. Confirm the downloader reached `Backup complete`.
2. Confirm the error report shows no unexpected failures.
3. Open representative downloaded files from every collection.
4. Confirm the following-list exports are complete.
5. Copy `Instagram-All` to a second safe location.
6. Remove `instagram_session.json` from every backup and shared copy.
7. Confirm that none of the omitted account data is still needed.

Instagram automation uses an unofficial interface and can be affected by login challenges, rate limits, or future Instagram changes. Avoid running several Instagram automation tools or sessions simultaneously.
