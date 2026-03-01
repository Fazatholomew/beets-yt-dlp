#!/usr/bin/env python

from beetsplug.yt_dlp import YtDlpPlugin, Colors
import os
import subprocess
from hashlib import md5

#
# To get a checksum: leave the first field blank, put an URL in the
# second field, and then run the test
#
TESTS = [
    ("4e4372f5d09d872b69654c81620bf6ac", "https://www.youtube.com/watch?v=uMMUcxvWOkY"),
    ("bb31adda714de9244de82ef6dbff806e", "https://www.youtube.com/watch?v=Zi_XLOBDo_Y"),
    ("ec734593c0a61678f8a9399f1325d180", "https://www.youtube.com/watch?v=wW6ykueIhX8"),
]

dbfile = "env.lib.db"
ydl_cmd = [
    "beet",
    "-c",
    "env.config.yml",
    "-l",
    dbfile,
    "yt-dlp",
    "--no-download",
    "--no-import",
    "--verbose",
]

if os.path.exists(dbfile):
    os.remove(dbfile)

failed = False

# --- original URL tests (unchanged) ---
for checksum, source in TESTS:
    cmd = ydl_cmd + [source]
    print(Colors.INFO + "=> " + Colors.END + Colors.BOLD + " ".join(cmd) + Colors.END)
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    md5_result = md5(str(result.stdout).encode()).hexdigest()

    if checksum and md5_result == checksum:
        output = Colors.SUCCESS + "   [OK] " + Colors.END + md5_result
    elif checksum:
        output = (
            Colors.WARNING + "   [ERROR] " + Colors.END + md5_result + " <> " + checksum
        )
        failed = True
    else:
        output = Colors.INFO + "   [CHECKSUM] " + md5_result + Colors.END
        print(result.stdout.decode("unicode_escape"))
    print(output)

# --- search test: check that search_youtube returns exactly 10 results ---
print(
    Colors.INFO
    + "\n=> "
    + Colors.END
    + Colors.BOLD
    + 'search_youtube("Never Gonna Give You Up")'
    + Colors.END
)
plugin = YtDlpPlugin.__new__(YtDlpPlugin)
plugin.config = {"youtubedl_options": {"quiet": True}}
results = plugin.search_youtube("Never Gonna Give You Up")
if len(results) == 10:
    print(Colors.SUCCESS + "   [OK] " + Colors.END + "Got 10 results")
else:
    print(
        Colors.WARNING
        + "   [ERROR] "
        + Colors.END
        + "Expected 10 results, got %d" % len(results)
    )
    failed = True

if failed:
    exit(2)
else:
    exit(0)
