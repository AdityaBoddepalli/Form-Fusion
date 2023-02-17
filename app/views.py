from app import app

from flask import render_template, request, redirect, url_for, jsonify

from werkzeug.utils import secure_filename

import requests, boto3, botocore, os, time

@app.route('/')
def landing_page():
    print('test')
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

            print("Videos have been saved successfully.")

        session = boto3.Session(
            aws_access_key_id=app.config['AWS_ACCESS_KEY'],
            aws_secret_access_key=app.config['AWS_SECRET_KEY'],
            region_name='us-east-1'
        )

        s3 = session.client('s3')
        s3.upload_file(f'./app/static/uploads/{filename1}', 'formfusion', 'video.mp4')
        s3.upload_file(f'./app/static/uploads/{filename2}', 'formfusion', 'pro_video.mp4')

        url = 'https://6df4-2600-1000-b01e-5091-dc3f-30cd-9218-358e.ngrok.io/formfusion'

        selected_joints = []
        joints = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

        for i in joints:
           if request.form.get(i) is not None:
            selected_joints.append(int(request.form.get(i)))

        print(selected_joints)

        response = requests.post(url, json={'numbers': selected_joints})
        print(selected_joints)
        print(response.status_code)
        assert response.status_code == 200

        time.sleep(15)

        s3.download_file('formfusion', 'annotated_video.mp4', './app/static/images/annotated_video.mp4')
        s3.download_file('formfusion', 'annotated_pro_video.mp4', './app/static/images/annotated_pro_video.mp4')

    return render_template('index.html')