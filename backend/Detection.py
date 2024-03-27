from jetson_inference import detectNet
from jetson_utils import (videoSource, videoOutput, cudaAllocMapped, cudaConvertColor, cudaDeviceSynchronize, cudaToNumpy)
import cv2 
class Detection:
    def __init__(self):
        self.net = detectNet("ssd-mobilenet-v2")
        self.camera = videoSource("csi://0")    
        self.display = videoOutput("file://frame.jpg")
        return
    
    def detect(self):
        detecs = [0] * 90 
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
      
    def save_image(self):
        if self.display.IsStreaming():
            img = self.camera.Capture()
            self.display.Render(img)
            return "frame.jpg"

            '''
            bgr_img = cudaAllocMapped(width=self.camera.GetWidth(),
                              height=self.camera.GetHeight(),
		    				  format='bgr8')
            cudaConvertColor(rgb_img, bgr_img)
            cudaDeviceSynchronize()
            cv_img = cudaToNumpy(bgr_img)
            print(cv_img)
            '''     


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


            