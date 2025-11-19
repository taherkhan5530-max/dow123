import yt_dlp
import sys
import os


# --- Helper Functions ---

def download_fb_video(url: str):
    """
    Downloads a Facebook video using the yt-dlp library.

    Args:
        url (str): The URL of the Facebook video to download.
    """
    print(f"\nAttempting to download video from URL: {url}")

    # Define the directory where the video will be saved (current working directory)
    output_template = os.path.join(os.getcwd(), "%(title)s.%(ext)s")

    # Options for yt-dlp
    ydl_opts = {
        # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        # Tries to get the best quality MP4 video and audio, then merges them.
        'format': 'best',

        # Output template: saves the file with its title and extension in the current folder.
        'outtmpl': output_template,

        # Ignore errors if the video is already downloaded
        'ignoreerrors': True,

        # Log download progress
        'progress_hooks': [
            lambda d: print(f"Status: {d['status']}. Total bytes: {d.get('total_bytes_str', 'N/A')}") if d[
                                                                                                             'status'] == 'downloading' else None],

        # Verbose mode for debugging (uncomment for detailed logs)
        # 'verbose': True,

        # Authentication settings - necessary for private or restricted videos.
        # Uncomment and fill in if you need to download private videos.
        # 'username': 'YOUR_FACEBOOK_EMAIL_OR_PHONE',
        # 'password': 'YOUR_FACEBOOK_PASSWORD',
    }

    try:
        # Use the YoutubeDL context manager
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # yt-dlp handles the extraction and downloading automatically
            info = ydl.extract_info(url, download=True)

            if info:
                # Get the actual filename created by yt-dlp
                # If a single video was downloaded, use its filename
                if 'entries' in info:  # Playlist/multi-video download
                    video_title = info['entries'][0].get('title', 'Video')
                    ext = info['entries'][0].get('ext', 'mp4')
                else:  # Single video download
                    video_title = info.get('title', 'Video')
                    ext = info.get('ext', 'mp4')

                print(f"\n✅ Download complete! Saved as: {video_title}.{ext}")
                print(f"File location: {os.path.join(os.getcwd(), video_title)}.{ext}")
            else:
                print("\n⚠️ Download finished, but could not retrieve detailed file info.")

    except Exception as e:
        print(f"\n❌ An error occurred during download: {e}")
        print("This could be due to an invalid URL, a private video (try adding credentials), or a network issue.")


# --- Main Execution Block ---

if __name__ == "__main__":

    print("--- Facebook Video Downloader (using yt-dlp) ---")

    # Check for the required library
    try:
        import yt_dlp
    except ImportError:
        print("\nFATAL ERROR: The 'yt-dlp' library is not installed.")
        print("Please install it using: pip install yt-dlp")
        sys.exit(1)

    # Get the URL from the user
    video_url = input("Please enter the full Facebook video URL: ").strip()

    if video_url:
        download_fb_video(video_url)
    else:
        print("No URL provided. Exiting.")

    print("\n----------------------------------------------------")