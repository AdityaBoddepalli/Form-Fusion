from app import app

from flask import render_template, request, redirect, url_for, jsonify

from werkzeug.utils import secure_filename

import requests, boto3, os, shutil

@app.route('/')
def landing_page():

    folder_path = './app/static/downloads'

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return render_template('index.html')

def file_validator(filename):
    if not '.' in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1]

    if ext.upper() in app.config['ALLOWED_FILE_EXTENSIONS']:
        return True
    else:
        return False

@app.route('/form', methods=["GET", "POST"])
def form_handler():
    if request.method == 'POST':
        if request.files:

            video1 = request.files['video1']
            video2 = request.files['video2']

            if video1.filename == '' or video2.filename == '':
                print("Videos must have a filename")
                return redirect(request.url)
            
            if not file_validator(video1.filename) and file_validator(video2.filename):
                print("The given file type is unsupported.")
                return redirect(request.url)
            
            else:
                filename1 = secure_filename(video1.filename)
                filename2 = secure_filename(video2.filename)

                video1.save(os.path.join(app.config['VIDEO_UPLOADS'], filename1))
                video2.save(os.path.join(app.config['VIDEO_UPLOADS'], filename2))

        session = boto3.Session(
            aws_access_key_id=app.config['AWS_ACCESS_KEY'],
            aws_secret_access_key=app.config['AWS_SECRET_KEY'],
            region_name='us-east-1'
        )

        s3 = session.client('s3')
        s3.upload_file(f'./app/static/uploads/{filename1}', 'formfusion', 'video.mp4')
        s3.upload_file(f'./app/static/uploads/{filename2}', 'formfusion', 'pro_video.mp4')

        url = app.config['ENDPOINT']

        selected_joints = []
        joints = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

        for i in joints:
           if request.form.get(i) is not None:
            selected_joints.append(int(request.form.get(i)))

        response = requests.post(url, json={'numbers': selected_joints})
        assert response.status_code == 200

        download1_filepath = './app/static/downloads/annotated_video.mp4'
        download2_filepath = './app/static/downloads/annotated_pro_video.mp4'

        s3.download_file('formfusion', 'annotated_video.mp4', download1_filepath)
        s3.download_file('formfusion', 'annotated_pro_video.mp4', download2_filepath)

        response_data = response.json()
        message = response_data['msg']

    return render_template('index.html', message=message)