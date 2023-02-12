from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
import requests, boto3, botocore, os, time

site = Blueprint('site', __name__, template_folder='app/templates')

@site.route('/')
def landing_page():
    return render_template('index.html')

@site.route('/form', methods=["GET"])
def form_handler():
    if request.method == 'GET':

        session = boto3.Session(
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
            region_name='us-east-1'
        )

        #s3 = session.client('s3')
        #s3.upload_fileobj(video, 'formfusion', 'video.mp4')
        #s3.upload_fileobj(pro_video, 'formfusion', 'pro_video.mp4')

        s3 = session.client('s3')
        s3.upload_file('./app/static/images/video.mp4', 'formfusion', 'video.mp4')
        s3.upload_file('./app/static/images/pro_video.mp4', 'formfusion', 'pro_video.mp4')

        url = 'https://6df4-2600-1000-b01e-5091-dc3f-30cd-9218-358e.ngrok.io/formfusion'

        selected_joints = []
        for k, v in request.args.items():
            selected_joints.append(int(k))

        response = requests.post(url, json={'numbers': selected_joints})
        print(selected_joints)
        print(response.status_code)
        assert response.status_code == 200

        time.sleep(15)

        s3.download_file('formfusion', 'annotated_video.mp4', './app/static/images/annotated_video.mp4')
        s3.download_file('formfusion', 'annotated_pro_video.mp4', './app/static/images/annotated_pro_video.mp4')

    return render_template('index.html')
