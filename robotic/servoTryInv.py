from ArmController import ArmController
from kinematic import inverse_kinematics

arm = ArmController()

print('If you would like to exit, just type the "x" then hit the enter\n\n')
exit = False
while not exit:
    
    points = str(input('Which point do you want to change the x, y, z, roll, pitch, yaw\n:'))
    if points.lower() == 'x':
        exit = True
        continue

    pointList = points.split()
    if len(pointList) != 6:
        print("there must be 6 values\n")
        continue

    angles = inverse_kinematics(float(pointList[0]), float(pointList[1]), float(pointList[2]),
                      float(pointList[3]), float(pointList[4]), float(pointList[5]))
    print(angles)
    for i in range(6):
        if angles[i] < 0 or angles[i] > 180:
            print("angles values are inappropriate!\n")
            exit = True
            break
        arm.setPosition(i, int(angles[i]))
    if exit:
        exit = False
        continue
