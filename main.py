import os
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# مجلد حفظ الفيديوهات المؤقت
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-recording', methods=['POST'])
def start_recording():
    data = request.form
    m3u8_url = data.get('m3u8_url')
    duration = data.get('duration', '300')
    output_name = data.get('output_name', 'recording.mp4')
    drive_folder = data.get('drive_folder', '')
    
    if not m3u8_url:
        return jsonify({'error': 'رابط البث مطلوب!'}), 400

    output_path = os.path.join(DOWNLOAD_FOLDER, output_name)
    
    # أمر FFmpeg لسحب البث وتسجيله بالمدة المحددة
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', m3u8_url,
        '-t', str(duration),
        '-c', 'copy',
        output_path
    ]
    
    # تشغيل العملية في الخلفية (Background) لتجنب تعليق الموقع
    try:
        subprocess.Popen(ffmpeg_cmd)
        return jsonify({
            'status': 'success',
            'message': f'تم بدء التسجيل بنجاح وسيتم حفظه باسم: {output_name}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
