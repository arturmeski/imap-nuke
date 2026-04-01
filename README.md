```
                ___ __  __    _   ____
               |_ _|  \/  |  /_\ |  _ \
                | || \  / | /\_\\| |_) |
                | || |\/| |/ ___ \  __/
               |___|_|  |_/_/   \_\_|

                 _   _ _   _ _  _____
                | \ | | | | | |/ / __|
                |  \| | | | | ' /| _|
                | |\  | |_| | . \| |__
                |_| \_|\___/|_|\_\____|

  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |  a  t o o l  f o r  d i g i t a l  a r s o n  |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


///////////////////////////////////////////////////////////////////////////////
//                                                                           //
//  imap-nuke                                           release: 2026        //
//  "scorched earth for your inbox"                                          //
//                                                                           //
//  brought to you by someone who finally got tired of 47,821 unread emails  //
//                                                                           //
///////////////////////////////////////////////////////////////////////////////


-[ WTF IS THIS ]----------------------------------------------------------------

You have n emails. You want 0 emails. Not zero after unsubscribing from
every mailing list like some kind of COWARD. Zero. NULL. The void.

imap-nuke connects to your Gmail over IMAP/TLS and deletes every single
message in every single folder until there is nothing left. No filter. No
mercy. No "are you sure you want to delete this memory from 2009?" - well,
one confirmation prompt, but that's it, and you have to type it in ALL CAPS
like you mean it.


-[ HOW IT WORKS ]---------------------------------------------------------------

  [your gmail]                  [imap-nuke]              [google's servers]
       |                             |                           |
       |   u type ur password        |                           |
       |<----------------------------|                           |
       |                             |--- TLS connect ---------->|
       |                             |--- LOGIN ---------------->|
       |                             |<-- OK yeah whatever ------|
       |                             |--- LIST "" * ------------>|
       |                             |<-- here's 40 folders -----|
       |    "type NUKE to confirm"   |                           |
       |<----------------------------|                           |
       |--- "NUKE" ----------------->|                           |
       |                             |--- SELECT [folder] ------>|
       |                             |--- STORE +FLAGS \Deleted->|
       |                             |--- EXPUNGE -------------->|
       |                             |  (repeat for all folders) |
       |                             |                           |
       |                         nothing                      nothing

-[ USAGE ]----------------------------------------------------------------------

$ python3 nuke.py

============================================================
  imap-nuke - Gmail account wiper
============================================================

Gmail address: doomed@gmail.com
Password (or App Password): ****************

Connecting to imap.gmail.com...
Logged in successfully.

Found 12 folder(s):
  INBOX
  [Gmail]/Sent Mail
  [Gmail]/Drafts
  [Gmail]/Spam
  [Gmail]/Trash
  [Gmail]/All Mail
  ... and more

WARNING: This will PERMANENTLY delete every message in every folder.
Account : doomed@gmail.com

Type "NUKE" to confirm, anything else to abort: NUKE

Nuking 'INBOX'... 12847 message(s) deleted.
Nuking '[Gmail]/Sent Mail'... 3291 message(s) deleted.
Nuking '[Gmail]/Drafts'... 17 message(s) deleted.
Nuking '[Gmail]/Spam'... 4012 message(s) deleted.
Nuking '[Gmail]/Trash'... 839 message(s) deleted.
Nuking '[Gmail]/All Mail'... 0 message(s) deleted.

Done. 21006 message(s) deleted across 12 folder(s).

[Gmail]/All Mail is always processed LAST. Gmail is sneaky about restoring
messages via All Mail if you nuke it first. We outsmart it.


-[ WARNINGS ]-------------------------------------------------------------------

  /!\ THIS IS IRREVERSIBLE /!\

  There is no undo. There is no "recently deleted" after expunge.
  Google may retain copies on their end for some period - that's
  between you and Google. From YOUR account's perspective: gone.

  Do not run this on an account you want to keep.
  Do not run this on someone else's account.
  Do not come crying.

-=[ EOF ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                     "delete it before they screenshot it"

  imap-nuke is free software. use it, fork it, don't blame anyone.
  no warranty. no support. no prisoners.

                              the inbox is a lie

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
```
