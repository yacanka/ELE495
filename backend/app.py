from flask import Flask, send_from_directory, Response, jsonify, render_template, request
from database import Database
from vision import vision_types
import jsonpickle
import sys
from ArmController import ArmController
from time import sleep
from Recognition import Recognition

#sys.path.append(r'../vision')
#from vision.detector import detect_object_color, detect_object_position

app = Flask(__name__)
detector = Recognition()
detector.Detect()
controller = ArmController()
sessionName = None
objectDict = {}

defaultPositions = [30, 40, 0 ,130, 0, 110]

startPoints = [
    [60,95,30,150,10,110],
    [95,60,0,130,15,110],
    [120,95,30,150,50,110]
]
# 80, 96, 160, 50, 50, 110
destPoints = {
    "banana": [5,70,45,150,5,110],
    "corn": [40,100,50,110,15,150],
    "mouse,": [150,100,50,110,5,110],
    "toilet paper": [130,90,30,70,5,110],
    "carrot": [170,80,50,150,5,110],
    "unknown": [170,80,50,150,5,110]
}

scenerios = {
    "toilet paper": [
        [90,40,30,130,0,110],
        [90,60,50,160,0,110],
        [90,60,50,160,0,110],
        [90,85,40,160,0,110],
        [90,85,40,160,0,165],
        [90,50,30,70,0,165],
        [130,90,30,70,0,165],
        [130,90,30,70,0,110]
    ],
    "corn": [
        [85,40,30,130,15,110],
        [85,70,10,130,15,110],
        [85,70,10,130,15,160],
        [85,70,70,130,15,160],
        [40,70,70,130,15,160],
        [40,70,40,100,15,160],
        [40,85,40,100,15,160],
        [40,85,40,100,15,110],
    ],
    "sunglasses": [
        [85,40,30,150,90,110],
        [85,80,20,150,90,110],
        [85,80,20,150,90,175],
        [85,80,70,150,90,175],
        [85,80,70,90,90,175],
        [135,80,70,90,90,175],
        [135,80,50,90,90,175],
        [135,80,50,140,30,110],
    ],
    "water bottle": [
        [85,40,30,130,15,110],
        [85,40,10,150,15,110],
        [85,70,10,150,15,110],
        [85,70,10,150,15,150],
        [85,70,50,150,15,150],
        [160,70,50,150,15,110],
    ],
    "bell pepper": [
        [85,40,30,130,15,110],
        [85,55,20,125,15,110],
        [85,70,10,125,15,110],
        [85,70,10,125,15,155],
        [85,70,50,150,15,155],
        [20,70,40,100,15,155],
        [20,70,50,150,15,110],
    ],
    "lemon": [
        [85,40,30,130,15,110],
        [85,55,20,125,15,110],
        [85,70,10,140,15,110],
        [85,70,10,140,15,155],
        [85,70,50,140,15,155],
        [40,85,50,100,15,155],
        [40,85,50,100,15,110],
    ],
    "unknown": [
        [85,40,30,130,15,110],
        [85,40,30,130,60,110],
        [85,40,30,130,15,110],
        [85,40,30,130,60,110],
    ]
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'Created by YcK'


@app.route('/fruits')
def fruits():
    objectList = [{'name': key, 'picked': int(value)} for key, value in objectDict.items()]
    print(objectList)
    return jsonify(objectList)

@app.route('/servos', methods=['POST'])
def set_angles():
    dict = request.json.get('angles')
    del dict['base']
    angle_list = list(map(int, list(dict.values())))
    controller.setPositions(angle_list)
    return jsonify({"message": "Set successfully"})
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'static/favicon.ico', mimetype='image/x-icon')


@app.route('/vision_types')
def get_vision_types():
    return jsonpickle.encode(list(vision_types.keys()))


@app.route('/video_feed', methods=['GET'])
def video_feed():
    stream_type = request.args.get('type', 'normal')
    print(stream_type)
    stream_model = vision_types[stream_type]
    return Response(stream_model(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/sessions')
def history():
    db = Database()
    return jsonify(db.get_all_session())


@app.route('/sessions', methods=['POST'])
def create_session():
    global sessionName
    if sessionName != None:
        return jsonify({"message": "Session already exists"})
    db = Database()
    sessionName = request.json.get('name')
    db.create_session(sessionName)
    
    # Model
    controller.setDefaultPositions()
    objectType = detector.Detect()
    objectLabel = detector.getLabels(objectType)
    if objectLabel in scenerios:
        print(f"{objectLabel} bulundu.")
    else:
        print(f"{objectLabel} objesi bilinmiyor.")
        objectLabel = "unknown"

    # Vision
    # detect_object_color()

    if objectLabel in objectDict:
        objectDict[objectLabel] += 1
    else:
        objectDict[objectLabel] = 1

    region = detector.getImageLocation()
    print(f"Region: {region}")
    controller.move(scenerios[objectLabel])
    db.update_session(sessionName, "Success", "Found object: " + objectLabel)
    sessionName = None
    return "Session finished successfully"


@app.route('/sessions/<string:id>', methods=['DELETE'])
def delete_session(id):
    db = Database()
    db.delete_session(id)
    return jsonify({"message": "Deleted successfully"})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
