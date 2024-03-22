from Detection import Detection

det = Detection()
while "x" != str(input()):
    x = det.detect()
    label = det.getLabel(x)
    print(label)
