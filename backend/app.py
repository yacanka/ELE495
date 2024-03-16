from flask import Flask, send_from_directory, Response, jsonify, render_template, request
from database import Database
from vision import vision_types
import jsonpickle
import sys
#from ArmController import ArmController
from time import sleep
#from Recognition import Recognition


app = Flask(__name__)
#controller = ArmController()
#detector = Recognition()
sessionName = None
objectDict = {}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'Created by YcK'


@app.route('/fruits')
def fruits():
    data = [
        {'name': 'apple', 'picked': 2, 'left': 1},
        {'name': 'orange', 'picked': 3, 'left': 0},
        {'name': 'banana', 'picked': 1, 'left': 2},
        {'name': 'quince', 'picked': 3, 'left': 0},
        {'name': 'pomegranate', 'picked': 3, 'left': 0}
    ]
    objectList = [{'name': key, 'picked': int(value)} for key, value in objectDict.items()]
    print(objectList)
    return jsonify(objectList)

@app.route('/servos', methods=['POST'])
def set_angles():
    dict = request.json.get('angles')
    del dict['base']
    angle_list = list(map(int, list(dict.values())))
    #controller.setPositions(angle_list)
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
    #objectType = detector.Detect()
    #objectLabel = detector.getLabels(objectType)

    #if objectLabel in objectDict:
    #    objectDict[objectLabel] += 1
    #else:
    #    objectDict[objectLabel] = 1
    #print(f"{objectLabel} label value: {objectDict[objectLabel]}")

    angle_list = [90,85,13,140,13,150]
    #controller.setPositions(angle_list)
    sleep(1)
    angle_list[1] = 50 
    #controller.setPositions(angle_list)
    sleep(1)
    angle_list[0] = 50
    #controller.setPositions(angle_list)
    sleep(1)
    angle_list[5] = 110
    #controller.setPositions(angle_list)
    #db.update_session(sessionName, "Success", "Found object: " + objectLabel)
    sessionName = None
    return jsonify({"message": "Session finished successfully"})


@app.route('/sessions/<string:id>', methods=['DELETE'])
def delete_session(id):
    db = Database()
    db.delete_session(id)
    return jsonify({"message": "Deleted successfully"})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
