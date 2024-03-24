# from Detection import Detection
from detector import detect_object_color, detect_object_position

# detector = Detection()
# cv = detector.save_image()
name = "my_image_0.jpg"
print(f"Color: {detect_object_color(name)}")
centerX, centerY, x, y, w, h = detect_object_position(name, False)
print(f"Center: ({centerX}, {centerY})")
print(f"Position: ({x}, {y})")
print(f"Width x height: {w} x {h}")

