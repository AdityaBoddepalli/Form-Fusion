import json
import cv2
import mediapipe as mp
import boto3
import math

def get_access_keys():
    with open("secrets.json") as f:
        secrets = json.load(f)

    access_key_id = secrets["AWS_ACCESS_KEY_ID"]
    secret_access_key = secrets["AWS_SECRET_ACCESS_KEY"]

    return access_key_id, secret_access_key


access_key_id, secret_access_key = get_access_keys()

line_dict = {
    1: [13, 11, 23],
    2: [14, 12, 24],
    3: [11, 13, 15],
    4: [12, 14, 16],
    5: [11, 23, 25],
    6: [12, 24, 26],
    7: [23, 25, 27],
    8: [24, 26, 28],
    9: [25, 27, 29],
    10: [26, 29, 30]
}

code_dict = {
    1: "SL",
    2: "SR",
    3: "EL",
    4: 'ER',
    5: "HL",
    6: "HR",
    7: "KL",
    8: "KR",
    9: "AL",
    10: "AR"
}

feedback_dict = {
    1: [0,0,0,0],
    2: [0,0,0,0],
    3: [0,0,0,0],
    4: [0,0,0,0],
    5: [0,0,0,0],
    6: [0,0,0,0],
    7: [0,0,0,0],
    8: [0,0,0,0],
    9: [0,0,0,0],
    10: [0,0,0,0]
}

body_part_dict = {
    1: "Left Shoulder",
    2: "Right Shoulder",
    3: "Left Elbow",
    4: "Right Elbow",
    5: "Left Hip",
    6: "Right Hip",
    7: "Left Knee",
    8: "Right Knee",
    9: "Left Ankle",
    10: "Right Ankle"
}

def find_angle(x1, y1, x2, y2, x3, y3):
    # Find the slope of the first line segment
    m1 = (y2 - y1) / (x2 - x1)

    # Find the slope of the second line segment
    m2 = (y3 - y2) / (x3 - x2)

    # Find the angle between the two lines in radians
    angle = math.atan2(m2 - m1, 1 + m1 * m2)

    # Convert the angle from radians to degrees
    angle = angle * 180 / math.pi

    return angle


def mp_script(numbers: list[int]):
    session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name='us-east-1'
    )

    s3 = session.client('s3')

    s3.download_file('formfusion', 'video.mp4', './video.mp4')
    s3.download_file('formfusion', 'pro_video.mp4', './pro_video.mp4')
    # s3 =  session.resource('s3').Bucket('formfusion').download_file('IMG_7360.mp4', './video.mp4')

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    pose = mp_pose.Pose(min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)

    # First video
    vid = cv2.VideoCapture('./video.mp4')

    if vid.isOpened() == False:
        print("Couldnt open the image")
        raise TypeError

    frame_width = int(vid.get(3))
    frame_height = int(vid.get(4))

    out_filename = 'annotated_video.mp4'
    out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(
            'H', '2', '6', '4'), 10, (frame_width, frame_height))

    n1 = True
    while vid.isOpened():
        ret, image = vid.read()
        if not ret:
            break

        # Convert the image to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Estimate the poses in the image
        results = pose.process(image)


        # Draw the landmarks
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # print(results.pose_landmarks)
        y_offset = 0
        for number in numbers:
            list = line_dict[number]
            one = list[0]
            two = list[1]
            three = list[2]
            one_cord = results.pose_landmarks.landmark[one]
            two_cord = results.pose_landmarks.landmark[two]
            three_cord = results.pose_landmarks.landmark[three]
            x1, y1 = one_cord.x * frame_width, one_cord.y * frame_height
            x2, y2 = two_cord.x * frame_width, two_cord.y * frame_height
            x3, y3 = three_cord.x * frame_width, three_cord.y * frame_height

            angle = round(find_angle(x1, y1, x2, y2, x3, y3), 2)

            #update the feedback
            fb_list = feedback_dict[number]
            if n1:
                fb_list[0] = angle
                fb_list[1] = angle
            else:
                if angle < fb_list[0]:
                    fb_list[0] = angle
                if angle > fb_list[1]:
                    fb_list[1] = angle

            msg = code_dict[number] + str(angle)

            # Draw the number on the image
            cv2.putText(image, msg, (30, 30 + y_offset),
                         cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2, cv2.LINE_4)
            y_offset += 30
        n1 = False

            
        # Convert the image back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        out.write(image)


    vid.release()
    out.release()

    # Video 2
    vid2 = cv2.VideoCapture('./video.mp4')

    if vid2.isOpened() == False:
        print("Couldnt open the image")
        raise TypeError

    frame_width2 = int(vid2.get(3))
    frame_height2 = int(vid2.get(4))

    out2_filename = 'annotated_pro_video.mp4'
    out2 = cv2.VideoWriter(out2_filename, cv2.VideoWriter_fourcc(
            'H', '2', '6', '4'), 10, (frame_width2, frame_height2))

    n2 = True
    while vid2.isOpened():
        ret2, image2 = vid2.read()
        if not ret2:
            break

        # Convert the image to RGB
        image2 = cv2.cvtColor(cv2.flip(image2, 1), cv2.COLOR_BGR2RGB)
        image2.flags.writeable = False

        # Estimate the poses in the image
        results2 = pose.process(image2)


        # Draw the landmarks
        mp_drawing.draw_landmarks(
            image2, results2.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # print(results.pose_landmarks)
        y_offset2 = 0
        for number in numbers:
            list = line_dict[number]
            one = list[0]
            two = list[1]
            three = list[2]
            one_cord = results2.pose_landmarks.landmark[one]
            two_cord = results2.pose_landmarks.landmark[two]
            three_cord = results2.pose_landmarks.landmark[three]
            x1, y1 = one_cord.x * frame_width, one_cord.y * frame_height
            x2, y2 = two_cord.x * frame_width, two_cord.y * frame_height
            x3, y3 = three_cord.x * frame_width, three_cord.y * frame_height

            angle2 = round(find_angle(x1, y1, x2, y2, x3, y3), 2)

            fb_list = feedback_dict[number]
            if n2:
                fb_list[2] = angle2
                fb_list[3] = angle2
            else:
                if angle2 < fb_list[2]:
                    fb_list[2] = angle2
                if angle2 > fb_list[3]:
                    fb_list[3] = angle2

            msg = code_dict[number] + str(angle2)

            # Draw the number on the image
            cv2.putText(image2, msg, (30, 30 + y_offset2),
                         cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2, cv2.LINE_4)
            y_offset2 += 30
        n2 = False

            
        # Convert the image back to BGR
        image2.flags.writeable = True
        image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR)
        out2.write(image2)



    pose.close()
    vid2.release()
    out2.release()


    # s3.delete_object(Bucket='formfusion', Key='IMG_7360.mp4')
    s3.upload_file('./annotated_video.mp4', 'formfusion', 'annotated_video.mp4')
    s3.upload_file('./annotated_pro_video.mp4', 'formfusion', 'annotated_pro_video.mp4')

    return

def get_message(numbers: list[int]):
    toRet = ""
    for number in numbers:
        body_joint = body_part_dict[number]
        fb_vals = feedback_dict[number]
        your_min = str(fb_vals[0])
        your_max = str(fb_vals[1])
        pro_min = str(fb_vals[2])
        pro_max = str(fb_vals[3])
        sentence = f'For your {body_joint} you go from {your_min} to {your_max} and they go from {pro_min} to {pro_max}. '
        toRet += sentence
    return toRet
