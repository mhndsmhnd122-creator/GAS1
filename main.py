import os
import subprocess
from googleapiclient.discovery import build
# ... (نفس كود الرفع السابق) ...

# قراءة البيانات من الـ GitHub Actions
m3u8_url = os.environ.get('M3U8_URL')
duration = os.environ.get('DURATION')

# تنفيذ أمر FFmpeg
ffmpeg_cmd = ['ffmpeg', '-y', '-i', m3u8_url, '-t', duration, '-c', 'copy', 'recording.mp4']
subprocess.run(ffmpeg_cmd)

# رفع الملف للدرايف ...
