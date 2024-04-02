import math
import numpy as np

class RobotLocalization3D:
    def __init__(self):
        # [x, y, z]
        self.position = np.array([0.0, 0.0, 0.0])
        # [roll, pitch, yaw]
        self.orientation = np.array([0.0, 0.0, 0.0])

    def update_position(self, linear_acceleration, angular_velocity, dt):
        # update orientation
        roll, pitch, yaw = self.orientation
        roll += angular_velocity[0] * dt
        pitch += angular_velocity[1] * dt
        yaw += angular_velocity[2] * dt

        # rotation matrix
        rotation_matrix = np.array([
            [math.cos(yaw)*math.cos(pitch), -math.sin(yaw)*math.cos(roll)+math.cos(yaw)*math.sin(pitch)*math.sin(roll), math.sin(yaw)*math.sin(roll)+math.cos(yaw)*math.sin(pitch)*math.cos(roll)],
            [math.sin(yaw)*math.cos(pitch), math.cos(yaw)*math.cos(roll)+math.sin(yaw)*math.sin(pitch)*math.sin(roll), -math.cos(yaw)*math.sin(roll)+math.sin(yaw)*math.sin(pitch)*math.cos(roll)],
            [-math.sin(pitch), math.cos(pitch)*math.sin(roll), math.cos(pitch)*math.cos(roll)]
        ])

        acceleration = np.array([linear_acceleration[0], linear_acceleration[1], linear_acceleration[2]])
        displacement = np.dot(rotation_matrix, acceleration) * dt
        self.position += displacement

        # restrict the orientation to [-pi, pi]
        self.orientation = np.array([self._normalize_angle(angle) for angle in [roll, pitch, yaw]])

    def _normalize_angle(self, angle):
        return (angle + math.pi) % (2 * math.pi) - math.pi

# example
robot = RobotLocalization3D()
# set initial position and orientation
linear_velocity = np.array([1.0, 0.0, 0.0])
angular_velocity = np.array([0.0, 0.0, 0.1])
dt = 1
# update
robot.update_position(linear_velocity, angular_velocity, dt)

print("position:", robot.position)
print("orientation", robot.orientation)
