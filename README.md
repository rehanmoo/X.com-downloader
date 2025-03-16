# X.com Video Downloader

A tool that automatically downloads videos from X.com (formerly Twitter) when you play them in your browser.

## Components

1. **Python Backend Script**: Runs a local server that receives video URLs and downloads them
2. **Browser Extension**: Detects when you play videos on X.com and sends the URLs to the backend

## Prerequisites

- Python 3.6 or higher
- yt-dlp (for downloading videos)
- A Chromium-based browser (Chrome, Edge, Brave) or Firefox

## Installation

### 1. Install yt-dlp

```bash
pip install yt-dlp
```

### 2. Set up the Python backend

The Python script (`x_video_downloader.py`) is ready to use. By default, videos will be saved to `~/Downloads/x_videos`.

### 3. Set up the browser extension

1. Open your browser's extension page:
   - **Chrome/Edge**: Go to `chrome://extensions/`
   - **Firefox**: Go to `about:debugging#/runtime/this-firefox`

2. Enable "Developer mode" (Chrome/Edge only)

3. Click "Load unpacked" (Chrome/Edge) or "Load Temporary Add-on" (Firefox)

4. Select the `extension` folder from this project

## Usage

1. Start the Python backend server:

```bash
python x_video_downloader.py
```

2. Browse X.com (or twitter.com) with the extension enabled

3. When you play a video, it will automatically be downloaded to the `~/Downloads/x_videos` directory

## How It Works

- The browser extension detects when you play a video on X.com
- It sends the tweet URL to the local server running on port 8765
- The server uses yt-dlp to download the video in the background
- Videos are saved with their original title and ID

## Customization

You can modify the following in `x_video_downloader.py`:

- `DOWNLOAD_DIR`: Change where videos are saved
- `PORT`: Change the port the server runs on (remember to update the same in `content.js`)

## Troubleshooting

- Make sure the Python script is running before playing videos
- Check the terminal output for any error messages
- If videos aren't downloading, ensure yt-dlp is installed and up to date
