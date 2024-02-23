from ArmController import ArmController

arm = ArmController()

print('If you would like to exit, just type the "x" then hit the enter\n\n')
exit = False
while not exit:
    servo_pin = str(input('Which servo motor do you want to change?\n:'))
    if servo_pin.lower() == 'x':
        exit = True
        continue

    angle = str(input('Which angle do you want to change the' + servo_pin + '\n:'))
    if angle.lower() == 'x':
        exit = True
        continue

    try:
        servo_pin = int(servo_pin)
        angle = int(angle)
    except:
        print('These are not an integer')
        print('Inappropriate value|s\n Please try again\n')
        continue
    
    print('Servo Pin:', servo_pin,"Angle:", angle, "\n")
    if servo_pin < 0 or servo_pin > 15 or angle < 0 or angle > 180:
        print('Inappropriate value|s\n Please try again\n')
        continue

    arm.setPosition(servo_pin, angle)
