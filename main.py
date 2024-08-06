from flask import Flask, render_template, request
import os
from mutagen.mp4 import MP4
import random
import string

app = Flask('app')
UPLOAD_FOLDER = 'lectures/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def add_metadata_to_mp4(file_path, custom_metadata):
    video = MP4(file_path)

    for key, value in custom_metadata.items():
        video[key] = value

    video.save()

def get_custom_metadata(file_path):
    video = MP4(file_path)

    # 사용자 정의 메타데이터 가져오기
    custom_metadata = {}
    for key in video.keys():
        custom_metadata[key] = video[key]

    return custom_metadata

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(6))
        title = request.files["videoname"]
        lecturename = request.files["lecturename"]
        teachername = request.files["teachername"]
        file_path = os.path.join(UPLOAD_FOLDER, f"{code}.mp4")
        file.save(file_path)
        add_metadata_to_mp4(file_path, {"videoname": title, "lecturename": lecturename, "teachername": teachername})
        return '1'
    except:
        return '0'

if __name__ == '__main__':
    app.run()

app.run(host='0.0.0.0', port=80, debug=True)
