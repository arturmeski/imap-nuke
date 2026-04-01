#!/usr/bin/env python3
"""
imap-nuke: Permanently delete every message in a Gmail account via IMAP.

Prerequisites:
  - IMAP must be enabled in Gmail settings (Settings -> See all settings -> Forwarding and POP/IMAP)
  - If your account uses 2-Step Verification, generate an App Password:
    Google Account -> Security -> 2-Step Verification -> App passwords
    Use that 16-character password instead of your real password.
"""

import imaplib
import sys
import getpass
import socket

IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993
BATCH_SIZE = 500


def connect(email: str, password: str) -> imaplib.IMAP4_SSL:
    print(f"Connecting to {IMAP_HOST}...")
    try:
        conn = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    except (socket.gaierror, OSError) as e:
        sys.exit(f"Connection failed: {e}")

    try:
        conn.login(email, password)
    except imaplib.IMAP4.error as e:
        sys.exit(f"Login failed: {e}")

    print("Logged in successfully.")
    return conn


def list_folders(conn: imaplib.IMAP4_SSL) -> list[str]:
    status, data = conn.list()
    if status != "OK":
        sys.exit("Failed to list folders.")

    folders = []
    for item in data:
        if item is None:
            continue
        # IMAP LIST response: (\Flags) "delimiter" "name"  or  (\Flags) "delimiter" name
        decoded = (item.decode() if isinstance(item, bytes) else item).strip()
        if decoded.endswith('"'):
            # Quoted name: extract between the last two double-quotes
            name = decoded.rsplit('"', 2)[-2]
        else:
            # Unquoted name: last whitespace-separated token
            name = decoded.rsplit(None, 1)[-1]
        if name:
            folders.append(name)

    return folders


def nuke_folder(conn: imaplib.IMAP4_SSL, folder: str) -> int:
    """Mark all messages in a folder as deleted and expunge. Returns count deleted."""
    status, _ = conn.select(f'"{folder}"', readonly=False)
    if status != "OK":
        print(f"  Skipping {folder!r} (could not select)")
        return 0

    # Search for all messages
    status, data = conn.search(None, "ALL")
    if status != "OK" or not data or not data[0]:
        return 0

    msg_ids = data[0].split()
    if not msg_ids:
        return 0

    count = len(msg_ids)
    print(f"\n  {count} message(s) found.", flush=True)
    # Mark and expunge in batches to avoid server timeouts on large folders
    deleted = 0
    for i in range(0, len(msg_ids), BATCH_SIZE):
        batch = msg_ids[i:i + BATCH_SIZE]
        id_range = b",".join(batch)
        conn.store(id_range, "+FLAGS", "\\Deleted")
        conn.expunge()
        deleted += len(batch)
        print(f"  {deleted}/{count} deleted...", flush=True)
    return count


def main() -> None:
    print("=" * 60)
    print("  imap-nuke - Gmail account wiper")
    print("=" * 60)
    print()

    email = input("Gmail address: ").strip()
    if not email:
        sys.exit("No email provided.")

    password = getpass.getpass("Password (or App Password): ")
    if not password:
        sys.exit("No password provided.")

    conn = connect(email, password)

    folders = list_folders(conn)
    print(f"\nFound {len(folders)} folder(s):")
    for f in folders:
        print(f"  {f}")

    print()
    print("WARNING: This will PERMANENTLY delete every message in every folder.")
    print(f"Account : {email}")
    confirm = input('\nType "NUKE" to confirm, anything else to abort: ').strip()
    if confirm != "NUKE":
        print("Aborted.")
        conn.logout()
        sys.exit(0)

    print()
    total_deleted = 0

    # Process [Gmail]/All Mail last - deleting from individual labels first
    # avoids Gmail re-creating messages from All Mail.
    priority_last = {"[Gmail]/All Mail", "[Google Mail]/All Mail"}
    ordered = [f for f in folders if f not in priority_last] + \
              [f for f in folders if f in priority_last]

    for folder in ordered:
        print(f"Nuking {folder!r}...", end="", flush=True)
        try:
            count = nuke_folder(conn, folder)
        except imaplib.IMAP4.abort as e:
            print(f"\n  Connection dropped ({e}), reconnecting...")
            conn = connect(email, password)
            count = nuke_folder(conn, folder)
        total_deleted += count
        print(f"  Done ({count} message(s) deleted).")

    print()
    print(f"Done. {total_deleted} message(s) deleted across {len(folders)} folder(s).")
    conn.logout()


if __name__ == "__main__":
    main()
