import gradio as gr
import subprocess
import shlex
import threading
import os
import tempfile
from pathlib import Path

# Define acceptable video and audio file extensions
VIDEO_EXTENSIONS = ['.mp4', '.mkv', '.webm', '.avi', '.flv', '.mov', '.m4v']
AUDIO_EXTENSIONS = ['.mp3', '.aac', '.flac', '.m4a', '.opus', '.vorbis', '.wav']

# Temporary directory to store downloads
TEMP_DIR = tempfile.gettempdir()

def run_yt_dlp(command, log_callback):
    """
    Executes the yt-dlp command and streams the output.
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in iter(process.stdout.readline, ''):
        log_callback(line)
    process.stdout.close()
    process.wait()

def find_latest_file(download_path, extensions):
    """
    Finds the latest file in the download_path with the given extensions.
    """
    downloaded_files = sorted(
        Path(download_path).glob("*"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    for file in downloaded_files:
        if file.is_file() and file.suffix.lower() in extensions:
            return str(file)
    return None

def download_video(options, url):
    """
    Constructs the yt-dlp command based on user inputs and executes it.
    Returns the yt-dlp logs and the path to the downloaded video/audio.
    """
    # Base command
    cmd = ["yt-dlp"]

    # General Options
    if options.get("help"):
        cmd.append("--help")
    if options.get("version"):
        cmd.append("--version")
    if options.get("update"):
        cmd.append("-U")
    if options.get("ignore_errors"):
        cmd.extend(["-i", "--ignore-errors"])
    if options.get("abort_on_error"):
        cmd.append("--abort-on-error")
    else:
        cmd.append("--no-abort-on-error")

    # Network Options
    if options.get("proxy"):
        cmd.extend(["--proxy", options["proxy"]])
    if options.get("socket_timeout"):
        cmd.extend(["--socket-timeout", str(options["socket_timeout"])])
    if options.get("source_address"):
        cmd.extend(["--source-address", options["source_address"]])

    # Video Selection
    if options.get("playlist_items"):
        cmd.extend(["--playlist-items", options["playlist_items"]])
    if options.get("min_filesize"):
        cmd.extend(["--min-filesize", options["min_filesize"]])
    if options.get("max_filesize"):
        cmd.extend(["--max-filesize", options["max_filesize"]])

    # Download Options
    if options.get("limit_rate"):
        cmd.extend(["--limit-rate", options["limit_rate"]])
    if options.get("retries"):
        retries = options["retries"]
        if isinstance(retries, (int, float)) and retries >= 0:
            cmd.extend(["--retries", str(int(retries))])
        elif isinstance(retries, str) and retries.lower() == "infinite":
            cmd.extend(["--retries", "infinite"])

    # Filesystem Options
    download_path = options.get("download_path") or TEMP_DIR
    cmd.extend(["--paths", download_path])
    if options.get("output_template"):
        cmd.extend(["--output", options["output_template"]])
    if options.get("restrict_filenames"):
        cmd.append("--restrict-filenames")
    if options.get("no_restrict_filenames"):
        cmd.append("--no-restrict-filenames")

    # Post-Processing Options
    if options.get("extract_audio"):
        cmd.append("-x")
        if options.get("audio_format"):
            cmd.extend(["--audio-format", options["audio_format"]])
        if options.get("audio_quality") is not None:
            cmd.extend(["--audio-quality", str(options["audio_quality"])])
    else:
        # If not extracting audio, set video format based on quality selection
        if options.get("video_format"):
            cmd.extend(["-f", options["video_format"]])

    # Custom Arguments
    if options.get("custom_args"):
        custom = shlex.split(options["custom_args"])
        cmd.extend(custom)

    # URL(s)
    if url:
        urls = shlex.split(url)
        cmd.extend(urls)

    logs = []
    media_path = None

    def log_callback(line):
        logs.append(line)
        output_logs.update(value=output_logs.value + line)

    # Run yt-dlp in a separate thread to prevent blocking
    thread = threading.Thread(target=run_yt_dlp, args=(cmd, log_callback))
    thread.start()
    thread.join()

    # Determine the type of file to look for
    if options.get("extract_audio"):
        extensions = AUDIO_EXTENSIONS
    else:
        extensions = VIDEO_EXTENSIONS

    # Find the latest downloaded file
    media_path = find_latest_file(download_path, extensions)

    return "\n".join(logs), media_path, media_path

def yt_dlp_interface(
    help_chk, version_chk, update_chk, ignore_errors_chk, abort_on_error_chk,
    proxy, socket_timeout, source_address,
    playlist_items, min_filesize, max_filesize,
    limit_rate, retries,
    download_path, output_template, restrict_filenames, no_restrict_filenames,
    extract_audio, video_quality, audio_format, audio_quality,
    custom_args,
    url
):
    """
    Gathers all user inputs, executes yt-dlp, and returns logs and media path.
    """
    # Map the video_quality to yt-dlp format selection
    quality_map = {
        "240p": "worst",
        "360p": "worst[height<=360]",
        "480p": "worst[height<=480]",
        "720p": "worst[height<=720]",
        "1080p": "worst[height<=1080]",
        "1440p": "worst[height<=1440]",
        "2160p": "worst[height<=2160]",
        "best": "best"
    }
    video_format = quality_map.get(video_quality, "best")

    options = {
        "help": help_chk,
        "version": version_chk,
        "update": update_chk,
        "ignore_errors": ignore_errors_chk,
        "abort_on_error": abort_on_error_chk,
        "proxy": proxy,
        "socket_timeout": socket_timeout,
        "source_address": source_address,
        "playlist_items": playlist_items,
        "min_filesize": min_filesize,
        "max_filesize": max_filesize,
        "limit_rate": limit_rate,
        "retries": retries,
        "download_path": download_path,
        "output_template": output_template,
        "restrict_filenames": restrict_filenames,
        "no_restrict_filenames": no_restrict_filenames,
        "extract_audio": extract_audio,
        "video_format": video_format,
        "audio_format": audio_format,
        "audio_quality": audio_quality,
        "custom_args": custom_args
    }

    logs, media_path, download_link = download_video(options, url)

    if media_path and os.path.exists(media_path):
        # Determine if the file is video or audio based on extension
        ext = Path(media_path).suffix.lower()
        if ext in VIDEO_EXTENSIONS:
            return logs, media_path, media_path
        elif ext in AUDIO_EXTENSIONS:
            return logs, None, media_path  # No video preview for audio
    else:
        return logs, None, None

# Define Gradio Interface
with gr.Blocks(theme=gr.themes.Default()) as demo:
    gr.Markdown("""
    # 🎥 yt-dlp Gradio Interface
    Download and manage videos from YouTube and other platforms with ease.
    """)

    with gr.Tab("Download"):
        with gr.Column():
            gr.Markdown("## 🔽 Enter Video Details and Options")

            with gr.Row():
                url = gr.Textbox(
                    label="📎 Video URL(s)", 
                    placeholder="Enter YouTube or other video URLs separated by space", 
                    lines=2
                )

            with gr.Row():
                # Video Quality Selection
                video_quality = gr.Dropdown(
                    label="🎞️ Video Quality",
                    choices=["240p", "360p", "480p", "720p", "1080p", "1440p", "2160p", "best"],
                    value="best",
                    type="value"
                )

                # Output Format Selection
                video_format = gr.Dropdown(
                    label="📁 Output Format",
                    choices=["mp4", "mkv", "webm", "avi", "flv", "mov", "m4v"],
                    value="mp4",
                    type="value"
                )

            with gr.Row():
                extract_audio = gr.Checkbox(
                    label="🎵 Extract Audio (--extract-audio)", 
                    value=False
                )

                # Audio Format Selection (visible only if extract_audio is True)
                audio_format = gr.Dropdown(
                    label="🎶 Audio Format (--audio-format)", 
                    choices=["best", "aac", "alac", "flac", "m4a", "mp3", "opus", "vorbis", "wav"],
                    value="best",
                    visible=False
                )

                # Audio Quality Slider (visible only if extract_audio is True)
                audio_quality = gr.Slider(
                    label="🎚️ Audio Quality (--audio-quality)", 
                    minimum=0, 
                    maximum=10, 
                    step=1, 
                    value=5,
                    visible=False
                )

            # Toggle visibility of audio options based on extract_audio
            def toggle_audio_options(extract):
                return gr.update(visible=extract), gr.update(visible=extract)

            extract_audio.change(
                fn=toggle_audio_options,
                inputs=[extract_audio],
                outputs=[audio_format, audio_quality]
            )

            with gr.Row():
                # Download Button
                run_btn = gr.Button("🚀 Download", variant="primary")

            with gr.Accordion("🔧 Advanced Download Options", open=False):
                with gr.Row():
                    # Limit Rate
                    limit_rate = gr.Textbox(
                        label="⏩ Limit Rate (--limit-rate)", 
                        placeholder="e.g., 50K or 4.2M", 
                        lines=1
                    )

                    # Retries
                    retries = gr.Textbox(
                        label="🔄 Retries (--retries)", 
                        placeholder="e.g., 10 or infinite", 
                        lines=1
                    )

                with gr.Row():
                    # Playlist Items
                    playlist_items = gr.Textbox(
                        label="📑 Playlist Items (--playlist-items)", 
                        placeholder="1,2,3 or 1-5", 
                        lines=1
                    )

                    # Minimum Filesize
                    min_filesize = gr.Textbox(
                        label="📏 Min Filesize (--min-filesize)", 
                        placeholder="e.g., 50k or 44.6M", 
                        lines=1
                    )

                    # Maximum Filesize
                    max_filesize = gr.Textbox(
                        label="📐 Max Filesize (--max-filesize)", 
                        placeholder="e.g., 100M", 
                        lines=1
                    )

                with gr.Row():
                    # Download Path
                    download_path = gr.Textbox(
                        label="📂 Download Path (-P)", 
                        placeholder="~/Downloads or /path/to/download", 
                        lines=1
                    )

                    # Output Template
                    output_template = gr.Textbox(
                        label="📝 Output Template (--output)", 
                        placeholder="%(title)s.%(ext)s", 
                        lines=1
                    )

                with gr.Row():
                    # Restrict Filenames
                    restrict_filenames = gr.Checkbox(
                        label="🔒 Restrict Filenames (--restrict-filenames)", 
                        value=False
                    )

                    # No Restrict Filenames
                    no_restrict_filenames = gr.Checkbox(
                        label="🔓 No Restrict Filenames (--no-restrict-filenames)", 
                        value=False
                    )

                with gr.Row():
                    # Custom Arguments
                    custom_args = gr.Textbox(
                        label="⚙️ Additional Custom Arguments", 
                        placeholder="Any additional yt-dlp arguments", 
                        lines=2
                    )

                with gr.Row():
                    # Proxy URL
                    proxy = gr.Textbox(
                        label="🔗 Proxy URL (--proxy)", 
                        placeholder="socks5://127.0.0.1:1080", 
                        lines=1
                    )

                    # Socket Timeout
                    socket_timeout = gr.Number(
                        label="⏲️ Socket Timeout (--socket-timeout)", 
                        value=10
                    )

                    # Source Address
                    source_address = gr.Textbox(
                        label="📡 Source Address (--source-address)", 
                        placeholder="192.168.1.1", 
                        lines=1
                    )

                with gr.Row():
                    # General Options
                    help_chk = gr.Checkbox(
                        label="❓ Show Help (--help)", 
                        value=False
                    )
                    version_chk = gr.Checkbox(
                        label="📄 Show Version (--version)", 
                        value=False
                    )
                    update_chk = gr.Checkbox(
                        label="🔄 Update yt-dlp (--update)", 
                        value=False
                    )
                    ignore_errors_chk = gr.Checkbox(
                        label="⚠️ Ignore Errors (--ignore-errors)", 
                        value=False
                    )
                    abort_on_error_chk = gr.Checkbox(
                        label="🚫 Abort on Error (--abort-on-error)", 
                        value=False
                    )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📜 Download Logs")
                output_logs = gr.Textbox(
                    label="Download Logs", 
                    placeholder="Download output will appear here...", 
                    lines=20
                )
            with gr.Column():
                gr.Markdown("### 🎥 Video Preview")
                video_preview = gr.Video(label="Video Preview")
                gr.Markdown("### 📥 Download Video")
                download_link = gr.File(label="Download Video")

        # Add a note about the temporary download path
        gr.Markdown("""
        ---
        **Note:** If no download path is specified, videos are saved to your system's temporary directory.
        """)

    # Define the event handler
    run_btn.click(
        fn=yt_dlp_interface,
        inputs=[
            # General Options
            help_chk, version_chk, update_chk, ignore_errors_chk, abort_on_error_chk,
            # Network Options
            proxy, socket_timeout, source_address,
            # Video Selection
            playlist_items, min_filesize, max_filesize,
            # Download Options
            limit_rate, retries,
            # Filesystem Options
            download_path, output_template, restrict_filenames, no_restrict_filenames,
            # Post-Processing Options
            extract_audio, video_quality, audio_format, audio_quality,
            # Custom Arguments
            custom_args,
            # URL
            url
        ],
        outputs=[output_logs, video_preview, download_link],
        show_progress=True
    )

# Launch the interface
demo.launch()
