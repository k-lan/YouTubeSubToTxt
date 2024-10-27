import yt_dlp
import os
import sys
from vtt2txt import convert_vtt_to_text

class YouTubeSubtitleScraper:
    def __init__(self, channel_url, output_dir="subtitles"):
        self.channel_url = channel_url
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Configure yt-dlp options with VTT format (YouTube's native subtitle format)
        self.ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitlesformat': 'vtt',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }

    def get_channel_videos(self):
        """Get all video URLs from the channel"""
        try:
            # Get the channel's video playlist URL
            channel_playlist = f"{self.channel_url}/videos"
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                playlist_info = ydl.extract_info(channel_playlist, download=False)
                videos = []
                
                if 'entries' in playlist_info:
                    for entry in playlist_info['entries']:
                        if entry and isinstance(entry, dict) and 'id' in entry:
                            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                            videos.append(video_url)
                            print(f"Found video: {entry.get('title', 'Unknown Title')}")
                
                return videos
        except Exception as e:
            print(f"Error getting channel videos: {str(e)}")
            return []

    def download_subtitles(self, video_url):
        """Download subtitles for a single video"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                video_info = ydl.extract_info(video_url, download=False)
                video_title = video_info.get('title', 'unknown')
                video_id = video_info.get('id', 'unknown')
                
                # Configure options for subtitle download
                subtitle_opts = {
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitlesformat': 'vtt',
                    'skip_download': True,
                    'outtmpl': f'{self.output_dir}/{video_id}',
                }
                
                with yt_dlp.YoutubeDL(subtitle_opts) as ydl_subs:
                    ydl_subs.download([video_url])
                
                return video_title, video_id
        except Exception as e:
            print(f"Error downloading subtitles for {video_url}: {str(e)}")
            return None, None

    def process_channel(self):
        videos = self.get_channel_videos()[:3]  # Limit to 3 videos for testing
        print(f"Found {len(videos)} videos (limited to 3 for testing)")
        
        # Create a single output file for all subtitles
        combined_output = f"{self.output_dir}/all_subtitles.txt"
        vtt_files_to_delete = []
        
        with open(combined_output, 'w', encoding='utf-8') as combined_file:
            for video_url in videos:
                try:
                    video_title, video_id = self.download_subtitles(video_url)
                    if video_title and video_id:
                        # Look for the downloaded subtitle file with .vtt extension
                        vtt_file = f"{self.output_dir}/{video_id}.en.vtt"
                        if os.path.exists(vtt_file):
                            text = convert_vtt_to_text(vtt_file)
                            
                            combined_file.write(f"\n\n{'='*50}\n")
                            combined_file.write(f"Title: {video_title}\n")
                            combined_file.write(f"{'='*50}\n\n")
                            combined_file.write(text)
                            
                            # Add VTT file to deletion list
                            vtt_files_to_delete.append(vtt_file)
                            print(f"Processed: {video_title}")
                        else:
                            print(f"No subtitles found for: {video_title}")
                except Exception as e:
                    print(f"Skipping video {video_url} due to error: {str(e)}")
                    continue
        
        # Clean up VTT files
        for vtt_file in vtt_files_to_delete:
            try:
                os.remove(vtt_file)
                print(f"Deleted: {vtt_file}")
            except Exception as e:
                print(f"Error deleting {vtt_file}: {str(e)}")
        
        print(f"\nAll subtitles have been combined into: {combined_output}")

def main():
    if len(sys.argv) != 2 or not sys.argv[1].startswith('https://www.youtube.com/@'):
        print('Usage: python youtube_subtitle_scraper.py https://www.youtube.com/@channelname')
        sys.exit(1)
        
    scraper = YouTubeSubtitleScraper(sys.argv[1])
    scraper.process_channel()

if __name__ == "__main__":
    main()
