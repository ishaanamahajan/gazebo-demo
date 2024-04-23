#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import csv
from geometry_msgs.msg import Twist
from math import atan2, sqrt, pi

def read_waypoints(filename):
    waypoints = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            x, y, heading = map(float, row[:3])
            waypoints.append((x, y, heading))
    return waypoints

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    def compute(self, error, delta_time):
        self.integral += error * delta_time
        derivative = (error - self.previous_error) / delta_time
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.previous_error = error
        return output

class WaypointFollower(Node):
    def __init__(self):
        super().__init__('waypoint_follower')
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.waypoints = read_waypoints('path_to_waypoints.csv')
        self.current_waypoint_index = 0
        self.pid_controller = PIDController(1.0, 0.1, 0.05)

    def follow_waypoints(self):
        rate = self.create_rate(10)  # 10 Hz
        while rclpy.ok():
            if self.current_waypoint_index < len(self.waypoints):
                x, y, heading = self.waypoints[self.current_waypoint_index]
                # Implement your method to get current robot position and heading here
                current_x, current_y, current_heading = 0, 0, 0  # Placeholder values

                distance_error = sqrt((x - current_x)**2 + (y - current_y)**2)
                angle_error = atan2(y - current_y, x - current_x) - current_heading

                # Normalize the angle_error to be within [-pi, pi]
                angle_error = (angle_error + pi) % (2 * pi) - pi

                velocity_command = self.pid_controller.compute(distance_error, 1/10.0)
                angular_command = self.pid_controller.compute(angle_error, 1/10.0)

                twist = Twist()
                twist.linear.x = velocity_command
                twist.angular.z = angular_command
                self.publisher.publish(twist)

                if distance_error < 0.1:  # Threshold to consider the waypoint reached
                    self.current_waypoint_index += 1
            else:
                # Stop the robot if all waypoints are reached
                twist = Twist()
                twist.linear.x = 0
                twist.angular.z = 0
                self.publisher.publish(twist)
                break
            rate.sleep()

def main(args=None):
    rclpy.init(args=args)
    waypoint_follower = WaypointFollower()
    waypoint_follower.follow_waypoints()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
