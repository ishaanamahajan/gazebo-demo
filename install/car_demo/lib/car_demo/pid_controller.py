#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import csv
from math import atan2, sqrt, pi
from prius_msgs.msg import PID  # Import the custom PID message

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
        self.control_publisher = self.create_publisher(PID, 'control_cmd', 10)
        self.waypoints = read_waypoints('lot17_sinsquare.csv')
        self.current_waypoint_index = 0
        self.pid_controller = PIDController(1.0, 0.1, 0.05)  # Might need adjustment

    def follow_waypoints(self):
        rate = self.create_rate(10)  # 10 Hz
        while rclpy.ok():
            if self.current_waypoint_index < len(self.waypoints):
                x, y, heading = self.waypoints[self.current_waypoint_index]
                # Placeholder values for simulation, replace with actual values
                current_x, current_y, current_heading = 0, 0, 0  

                distance_error = sqrt((x - current_x)**2 + (y - current_y)**2)
                angle_error = atan2(y - current_y, x - current_x) - current_heading
                angle_error = (angle_error + pi) % (2 * pi) - pi  # Normalize error

                # Convert PID output to control commands
                throttle = self.pid_controller.compute(distance_error, 1/10.0)  # Example conversion
                steering_angle = self.pid_controller.compute(angle_error, 1/10.0)  # Example conversion

                pid_message = PID()
                pid_message.steering_angle = steering_angle
                pid_message.throttle = throttle
                self.control_publisher.publish(pid_message)

                if distance_error < 0.1:  # Check if waypoint is reached
                    self.current_waypoint_index += 1
            else:
                # Stop the vehicle once all waypoints are reached
                self.control_publisher.publish(PID(steering_angle=0.0, throttle=0.0))
                break
            rate.sleep()

def main(args=None):
    rclpy.init(args=args)
    waypoint_follower = WaypointFollower()
    waypoint_follower.follow_waypoints()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
