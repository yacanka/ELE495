import math

def inverse_kinematics(x, y, z, roll, pitch, yaw):
    # Robot arm lengths
    l1 = 1.0
    l2 = 1.0
    l3 = 1.0
    l4 = 1.0
    l5 = 1.0
    l6 = 1.0

    # Axis angles
    theta2 = math.acos((x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2))

    theta1 = math.atan2(y, x) - math.atan2((l2 * math.sin(theta2)), (l1 + l2 * math.cos(theta2)))

    d = (x**2 + y**2 + (z - l1)**2 - l2**2 - l3**2) / (2 * l2 * l3)
    theta3 = math.atan2(math.sqrt(1 - d**2), d)

    theta4 = math.atan2((z - l1 - l2 * math.cos(theta2)) / l3, (l2 * math.sin(theta2)) / l3)

    theta5 = math.atan2((l2 * math.cos(theta2) + l3 * math.cos(theta3) - z + l1), (l3 * math.sin(theta3)))

    theta6 = math.radians(yaw)

    return math.degrees(theta1), math.degrees(theta2), math.degrees(theta3), math.degrees(theta4), math.degrees(theta5), math.degrees(theta6)

# Target location and orientation
target_x = 1.5
target_y = 0.5
target_z = 1.0
target_roll = 30.0  # Roll angle
target_pitch = 45.0  # Pitch angle
target_yaw = 60.0  # Yaw angle

# Inverse kinematic calculation
joint_angles = inverse_kinematics(target_x, target_y, target_z, target_roll, target_pitch, target_yaw)

# Result
print("Joint Angles (degrees):", joint_angles)
