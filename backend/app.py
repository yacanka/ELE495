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
controller = ArmController()
sessionName = None
objectDict = {}

startPoints = [
    
    [60,95,30,150,10,110],
    [90,95,30,150,30,110],
    [120,95,30,150,50,110]
]
# 80, 96, 160, 50, 50, 110
destPoints = {
    "banana": [20,80,50,150,5,110],
    "corn": [150,50,13,140,13,150],
    "mouse": [90,85,13,140,13,150],
    "toilet": [90,85,13,140,13,150],
    "carrot": [90,85,13,140,13,150]
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
    objectType = detector.Detect()
    objectLabel = detector.getLabels(objectType)

    # Vision
    # detect_object_color()

    if objectLabel in objectDict:
        objectDict[objectLabel] += 1
    else:
        objectDict[objectLabel] = 1

    region = detector.getImageLocation()
    print(f"Region: {region}")
    angle_list = startPoints[region]
    controller.setPositions(angle_list)
    sleep(1)
    angle_list[1] = 50 
    controller.setPositions(angle_list)
    sleep(1)
    angle_list[0] = 180
    controller.setPositions(angle_list)
    sleep(1)
    angle_list[5] = 110
    controller.setPositions(angle_list)
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
