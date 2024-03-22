from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import cv2
import numpy as np
class Detection:
    def __init__(self):
        self.net = detectNet("ssd-mobilenet-v2")
        self.camera = videoSource("csi://0")         
        return
    
    def detect(self):
        detecs = [0] * 90 
        self.display = videoOutput("file://my_image_%i.jpg")  
        for i in range(16):
            img = self.camera.Capture()
            if img is None:
                continue
            
            self.detections = self.net.Detect(img)
            
            for detected in self.detections:
                x = detected.ClassID 
                detecs[x] += 1
              
            self.display.Render(img)
            self.display.SetStatus("Object Detection | Network {:.0f} FPS".format(self.net.GetNetworkFPS()))
            
        for j in range(90):
            if detecs[j] > 8:
                return j
        return 0
    
    def getImageLocation(self):
        img = cv2.imread("my_image_7.jpg",cv2.COLOR_BGR2GRAY)
        blurred1 = cv2.GaussianBlur(img, (5, 5), 0)
        edges1 = cv2.Canny(blurred1,70,90)

        (cnts, _) = cv2.findContours(edges1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        coins = edges1.copy()
        cv2.drawContours(coins, cnts, -1, (255, 0, 0), 2)

        height, width = coins.shape
        cutting_point1 = width // 3
        cutting_point2 = (width // 3) * 2

        left_area = coins[:, :cutting_point1]
        mid_area = coins[:, cutting_point1:cutting_point2]
        right_area = coins[:, cutting_point2:]
        
        sums = np.array([np.sum(left_area), np.sum(mid_area), np.sum(right_area)])
        max_sum_index = np.argmax(sums)
    
        output_path = "/home/jetson/my-detection/loc.jpg"
        cv2.imwrite(output_path,coins)
        return max_sum_index

    def getLabel(self, classID):
        labels = ["unlabeled", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
          "traffic light", "fire hydrant", "street sign", "stop sign", "parking meter", "bench", "bird", "cat",
          "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "hat", "backpack", "umbrella",
          "shoe", "eye glasses", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", 
          "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "plate",
          "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
          "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "mirror",
          "dining table", "window", "desk", "toilet", "door", "tv", "laptop", "mouse", "remote", "keyboard",
          "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "blender", "book", "clock", 
          "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
        return labels[classID]
