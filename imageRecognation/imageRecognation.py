from Recognation import Recognation

det = Recognation()
while "x" != str(input()):
    x = det.Detect()
    print("initialization completed!\n")
    label = det.getLabels(x)
    print(str(x), ":" + str(label))
    location = det.getImageLocation()
    print(location)
