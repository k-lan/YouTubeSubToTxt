# YouTube Subtitle Scraper

This Python script downloads and processes YouTube subtitles for videos on a specified channel. It saves subtitles in `.vtt` format, converts them to plain text, and combines them into a single output file.

## Features
- Retrieves video URLs from a YouTube channel.
- Downloads video subtitles (if available) in `.vtt` format.
- Converts `.vtt` subtitle files to plain text and combines them into a single output file.

### Prerequisites
- Python 3.6+
- Install required packages:
  - `yt-dlp`
  - `BeautifulSoup4`
  - `requests`

### Installation

1. Clone this repository or copy the script.
2. Set up a virtual environment (optional):

   ```bash
   python3 -m venv yt_subtitle_scraper_env
   source yt_subtitle_scraper_env/bin/activate  # On Windows use: yt_subtitle_scraper_env\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install yt-dlp beautifulsoup4 requests
   ```

### Usage

To scrape subtitles from a YouTube channel, run the following:

```bash
python youtube_subtitle_scraper.py https://www.youtube.com/@channelname
```

The combined subtitles will be saved in the `subtitles/all_subtitles.txt` file.

