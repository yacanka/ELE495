import base64
import os
import numpy as np
import time
import cv2

camera_number = 1

# YOLO Variables
abs_path_labels = "models/yolo/coco.names"
abs_path_weights = "models/yolo/yolov3.weights"
abs_path_config = "models/yolo/yolov3.cfg"
confidence_thres = 0.5
non_max_thres = 0.3

def normal_socket():
    camera = cv2.VideoCapture(camera_number)
    while True:
        success, frame = camera.read()

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield frame

def normal():
    print("Start")
    camera = cv2.VideoCapture(camera_number)
    while True:
        success, frame = camera.read()

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def yolo_classifier():
    # load the COCO class labels our YOLO model was trained on
    labelsPath = os.path.sep.join([abs_path_labels])
    LABELS = open(labelsPath).read().strip().split("\n")
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                               dtype="uint8")
    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([abs_path_weights])
    print("[INFO] Found weights")
    configPath = os.path.sep.join([abs_path_config])
    print("[INFO] Found configuration file")
    # load our YOLO object detector trained on COCO dataset (80 classes)
    # and determine only the *output* layer names that we need from YOLO
    print("[INFO] Loading YOLO")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    cap = cv2.VideoCapture(camera_number)
    if (cap.isOpened() == False):
        print("[ERROR] Could not load video")
    else:
        # Set height & width of video
        ret, frame = cap.read()
        (H, W) = frame.shape[:2]
        fps = cap.get(5)
        print('Frames per second : ', fps, 'FPS')
    while cap.isOpened():
        ret, frame = cap.read()
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not ret:
            print("[WARNING] Frame is lost")
            continue
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)
        boxes = []
        confidences = []
        classIDs = []
        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > confidence_thres:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(
            boxes, confidences, confidence_thres, non_max_thres)
        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                # draw a bounding box rectangle and label on the frame
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                                           confidences[i])
                cv2.putText(frame, text, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


vision_types = {
    'normal': normal,
    'cascade': cascade_classifier,
    'yolo': yolo_classifier
}
