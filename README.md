# beets-yt-dlp

Download audio from yt-dlp sources and import into beets.

> **Forked from [vmassuchetto/beets-yt-dlp](https://github.com/vmassuchetto/beets-yt-dlp)** — extended with yt-dlp support and YouTube search functionality.

**Download a direct URL:**

    $ beet yt-dlp "https://www.youtube.com/watch?v=wW6ykueIhX8"

**Search YouTube and download the best match:**

    $ beet yt-dlp --search "Short Music for Short People Fat Wreck"

**List imported tracks:**

    $ beet ls short music for short people

    59 Times the Pain - Short Music for Short People - We Want the Kids
    7 Seconds - Short Music for Short People - F.O.F.O.D.
    88 Fingers Louie - Short Music for Short People - All My Friends Are in Popular Bands
    Adrenalin O.D. - Short Music for Short People - Your Kung Fu Is Old... And Now You Must Die!
    Aerobitch - Short Music for Short People - Steamroller Blues
    [...]

## Installation

    pip install beets-yt-dlp

    uv add beets-yt-dlp

Then enable the plugin in your `config.yaml`:

```yaml
plugins: yt-dlp
```

## Configuration

Available options and default values in `config.yaml`:

```yaml
plugins: yt-dlp

yt-dlp:
    download: True          # download files from sources after getting information
    split_files: True       # try to split album files into separate tracks
    import: True            # import files into beets after downloading and splitting
    youtubedl_options: {}   # yt-dlp options -- https://github.com/yt-dlp/yt-dlp/blob/6f796a2bff332f72c3f250207cdf10db852f6016/yt_dlp/YoutubeDL.py#L199
    urls: []                # list of default URLs to download when no arguments are
                            # provided; you can point this at a playlist to check every time
```

## How it works

The plugin's main goal is to deliver an importable file set to the `beet import`
command. It downloads an audio file, looks for a tracklist with track times in
the video description, splits the file into per-track files, assigns basic ID3
tags to them, and finally runs `beet import` on
`${BEETS_CONFIG}/yt-dlp-cache/${VIDEO_ID}`.

### Search mode

When the `--search` / `-s` flag is used, the argument is treated as a free-text
query instead of a URL. The plugin will:

1. Query YouTube for the **top 10** matching results using yt-dlp's `ytsearch10:`
   scheme (metadata only — nothing is downloaded at this stage).
2. Pass those results through a **ranking function** (`rank_results`) to pick the
   best match.
3. Hand the winning URL to the normal download and import flow.

The ranking function is simple view count, title similarity, and official audio title. Implement your own scoring logic inside `rank_results()` in
the plugin source — see the docstring there for ideas and a ready-to-use
skeleton using `difflib`.

**CLI flags:**

| Flag | Short | Description |
|---|---|---|
| `--search` | `-s` | Treat the argument as a search query rather than a URL |
| `--no-download` | | Fetch metadata only, skip downloading |
| `--no-split-files` | | Skip splitting album files into tracks |
| `--no-import` | | Skip importing into beets |
| `--force-download` | `-f` | Re-download even if already in library |
| `--keep-files` | `-k` | Keep cached files after import |
| `--write-dummy-mp3` | `-w` | Write blank MP3s with valid ID3 tags (for testing) |
| `--verbose` | `-v` | Print detailed processing information |

## Tips

- **Search mode picks the first-ranked result automatically.** If the wrong
  video is chosen, try a more specific query or implement custom ranking logic
  in `rank_results()`.

- The video title can trick beets into misidentifying an album — if that
  happens, manually enter a search term when beets prompts you.

- Use the `bandcamp` plugin for better metadata results.

- Use a `.netrc` file to access your own YouTube playlists:

      machine youtube login somelogin@gmail.com password somepassword

  Check [the yt-dlp netrc docs](https://git.io/fN2TD) for more information.
  This lets you download private playlists or your subscriptions:

      beet yt-dlp "https://www.youtube.com/feed/subscriptions"

- **Download now, import later:**

  Download and split without importing:

      beet yt-dlp "<url>" --keep-files --no-import

  Then import when ready:

      beet yt-dlp "<url>" --no-download --no-split-files

  Useful for large playlists that need manual beets intervention.

- **(Possibly) enhance audio quality:**

  The default format is `bestaudio/best` at 192 kbps. For higher quality:

  ```yaml
  yt-dlp:
      youtubedl_options:
          format: 'best'
          postprocessors:
              key: 'FFmpegExtractAudio'
              preferredcodec: 'mp3'
              preferredquality: '320'
              nopostoverwrites: True
  ```

  Note that 320 kbps may be nominal if the source audio isn't that quality.
  See [this discussion](https://askubuntu.com/q/634584).

## Development

    uv sync
    uv run test.py

## Credits

Based on [vmassuchetto/beets-yt-dlp](https://github.com/vmassuchetto/beets-yt-dlp)
by Vinicius Massuchetto, originally licensed under the MIT License.