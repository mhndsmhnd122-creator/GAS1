import os
import subprocess
from flask import Flask, render_template, request, jsonify
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# إعدادات جوجل درايف
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def upload_to_drive(file_path, folder_id):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype='video/mp4')
    service.files().create(body=file_metadata, media_body=media).execute()

@app.route('/start-recording', methods=['POST'])
def start_recording():
    m3u8_url = request.form.get('m3u8_url')
    duration = request.form.get('duration', '300')
    output_name = request.form.get('output_name', 'recording.mp4')
    drive_folder = request.form.get('drive_folder')
    
    output_path = os.path.join(DOWNLOAD_FOLDER, output_name)
    
    # أمر FFmpeg
    ffmpeg_cmd = ['ffmpeg', '-y', '-i', m3u8_url, '-t', str(duration), '-c', 'copy', output_path]
    
    # تشغيل التسجيل
    subprocess.run(ffmpeg_cmd)
    
    # بعد الانتهاء، نرفع للدرايف إذا كان المجلد موجوداً
    if drive_folder:
        upload_to_drive(output_path, drive_folder)
        
    return jsonify({'status': 'success', 'message': 'تم التسجيل والرفع للدرايف بنجاح!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
