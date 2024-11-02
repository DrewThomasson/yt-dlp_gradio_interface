# 🎥 yt-dlp Gradio Interface

A sleek and user-friendly web interface built with Gradio for downloading videos and audio from YouTube and other platforms using `yt-dlp`. Easily configure download options, select desired quality and format, preview downloads, and obtain direct download links—all from your browser!

<img width="1166" alt="Screenshot 2024-11-02 at 12 25 18 AM" src="https://github.com/user-attachments/assets/32bfdba0-9456-4e0b-9f85-d9af0959708f">
<img width="1166" alt="Screenshot 2024-11-02 at 12 25 30 AM" src="https://github.com/user-attachments/assets/27e96282-2107-48b0-baa2-dd376079e15b">

## 📌 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Advanced Options](#advanced-options)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Intuitive Interface:** Clean and modern design with easy navigation.
- **Video & Audio Downloads:** Choose to download entire videos or extract audio in various formats.
- **Quality Selection:** Select from common video resolutions (e.g., 240p, 720p, 1080p) to match your preferences.
- **Format Selection:** Choose your desired output format (e.g., mp4, mkv, webm).
- **Real-Time Logs:** Monitor download progress and logs in real-time.
- **Video Preview:** Preview downloaded videos directly within the browser.
- **Direct Download Links:** Easily download your media files with a single click.
- **Advanced Configuration:** Access comprehensive `yt-dlp` options for customized downloads.
- **Custom Arguments:** Input additional `yt-dlp` arguments for advanced users.

## 📋 Prerequisites

Before running the application, ensure you have the following installed on your system:

1. **Python 3.7+**  
   [Download Python](https://www.python.org/downloads/)

2. **yt-dlp**  
   Install via pip:
   ```bash
   pip install yt-dlp
   ```

3. **Gradio**  
   Install via pip:
   ```bash
   pip install gradio
   ```

4. **FFmpeg** (Required for some `yt-dlp` features)  
   - **Windows:** [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your system's PATH.
   - **macOS:** Install via Homebrew:
     ```bash
     brew install ffmpeg
     ```
   - **Linux:** Install via your distribution's package manager. For Debian/Ubuntu:
     ```bash
     sudo apt-get install ffmpeg
     ```

## 🚀 Installation

1. **Clone the Repository**  
   Navigate to your desired directory and clone the repository:
   ```bash
   git clone https://github.com/yourusername/yt-dlp-gradio-interface.git
   ```

2. **Navigate to the Project Directory**
   ```bash
   cd yt-dlp-gradio-interface
   ```

3. **Install Required Python Packages**  
   It's recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   *If you don't have a `requirements.txt`, install the necessary packages manually:*
   ```bash
   pip install yt-dlp gradio
   ```

## 🖥️ Usage

1. **Run the Application**  
   Execute the `app.py` script:
   ```bash
   python app.py
   ```

2. **Access the Interface**  
   Once the application is running, Gradio will provide a local URL (e.g., `http://127.0.0.1:7860`). Open this URL in your web browser to access the yt-dlp interface.

## ⚙️ Configuration

### **Download Tab**

- **📎 Video URL(s):**  
  Enter one or multiple video URLs separated by spaces.

- **🎞️ Video Quality:**  
  Select the desired video resolution (e.g., 240p, 720p, 1080p).

- **📁 Output Format:**  
  Choose the desired output video format (e.g., mp4, mkv, webm).

- **🎵 Extract Audio (--extract-audio):**  
  Check this box if you want to extract audio from the video.

  - **🎶 Audio Format (--audio-format):**  
    Select the desired audio format (e.g., mp3, aac).

  - **🎚️ Audio Quality (--audio-quality):**  
    Adjust the audio quality slider (0 = best, 10 = worst).

- **🚀 Download Button:**  
  Click to start the download process.

### **🔧 Advanced Download Options (Accordion)**

- **⏩ Limit Rate (--limit-rate):**  
  Set the maximum download rate (e.g., 50K, 4.2M).

- **🔄 Retries (--retries):**  
  Specify the number of retries (e.g., 10 or `infinite`).

- **📑 Playlist Items (--playlist-items):**  
  If downloading from a playlist, specify which items to download (e.g., `1,2,3` or `1-5`).

- **📏 Min Filesize (--min-filesize):**  
  Set the minimum file size (e.g., `50k`, `44.6M`).

- **📐 Max Filesize (--max-filesize):**  
  Set the maximum file size (e.g., `100M`).

- **📂 Download Path (-P):**  
  Specify where to save the downloaded files. If left blank, defaults to the system's temporary directory.

- **📝 Output Template (--output):**  
  Define the naming convention for downloaded files using `yt-dlp`'s template syntax (e.g., `%(title)s.%(ext)s`).

- **🔒 Restrict Filenames (--restrict-filenames):**  
  Restrict filenames to ASCII characters and avoid special characters.

- **🔓 No Restrict Filenames (--no-restrict-filenames):**  
  Allow Unicode characters and special characters in filenames.

- **⚙️ Additional Custom Arguments:**  
  Input any additional `yt-dlp` arguments as needed.

- **🌐 Network Options:**

  - **🔗 Proxy URL (--proxy):**  
    Specify a proxy if required.

  - **⏲️ Socket Timeout (--socket-timeout):**  
    Set the socket timeout duration.

  - **📡 Source Address (--source-address):**  
    Define the client-side IP address to bind to.

- **⚙️ General Options:**

  - **❓ Show Help (--help):**  
    Display `yt-dlp` help information.

  - **📄 Show Version (--version):**  
    Display the `yt-dlp` version.

  - **🔄 Update yt-dlp (--update):**  
    Update `yt-dlp` to the latest version.

  - **⚠️ Ignore Errors (--ignore-errors):**  
    Continue downloading even if errors occur.

  - **🚫 Abort on Error (--abort-on-error):**  
    Stop downloading if an error occurs.

## 🛠️ Advanced Options

- **🎶 Extract Audio:**  
  Choose to extract audio from the video and select the desired format and quality.

- **📁 Output Format:**  
  Select the desired video format from a dropdown menu.

- **🎞️ Video Quality:**  
  Select from common video resolutions to match your preferences.

- **Custom Arguments:**  
  For advanced users, input any additional `yt-dlp` arguments not covered by the interface.

## 🐛 Troubleshooting

- **IsADirectoryError:**  
  *Error Message:*  
  ```
  IsADirectoryError: [Errno 21] Is a directory: '/var/folders/.../T/TemporaryItems'
  ```
  *Solution:*  
  Ensure that the download path does not contain subdirectories that could be mistaken for media files. The script has been updated to filter out directories and select only valid media files based on their extensions.

- **No Video Preview or Download Link:**  
  *Cause:*  
  The download might have failed, or the media file wasn't correctly identified.
  *Solution:*  
  Check the download logs for errors and ensure that the selected video quality and format are supported by the source video.

- **Permission Issues:**  
  *Cause:*  
  The application doesn't have write permissions to the specified download directory.
  *Solution:*  
  Choose a directory where you have write permissions or adjust the permissions accordingly.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
