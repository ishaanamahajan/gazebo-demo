#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped
import math

class TrajectoryController(Node):
    def __init__(self):
        super().__init__('trajectory_controller')
        
        # Create a publisher to the /car_demo/ackermann_cmd topic
        self.pub = self.create_publisher(AckermannDriveStamped, '/car_demo/ackermann_cmd', 10)
        
        # Declare and get parameters
        self.declare_parameter('mode', 'straight')
        self.declare_parameter('duration', 10)
        self.mode = self.get_parameter('mode').get_parameter_value().string_value
        self.duration = self.get_parameter('duration').get_parameter_value().integer_value

        # Set the loop rate
        self.timer_period = 0.1  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # Variables for trajectory timing
        self.start_time = self.get_clock().now().seconds_nanoseconds()[0]

    def publish_command(self, speed, steering_angle):
        drive_msg = AckermannDriveStamped()
        drive_msg.header.stamp = self.get_clock().now().to_msg()
        drive_msg.drive.speed = speed
        drive_msg.drive.steering_angle = steering_angle
        self.pub.publish(drive_msg)

    def straight_line(self):
        end_time = self.start_time + self.duration
        while self.get_clock().now().seconds_nanoseconds()[0] < end_time:
            self.publish_command(1.0, 0.0)

    def circle(self):
        end_time = self.start_time + self.duration
        while self.get_clock().now().seconds_nanoseconds()[0] < end_time:
            self.publish_command(1.0, 0.5)  # Adjust the steering angle for the circle

    def half_sine(self):
        end_time = self.start_time + self.duration
        while self.get_clock().now().seconds_nanoseconds()[0] < end_time:
            elapsed = self.get_clock().now().seconds_nanoseconds()[0]
            steering_angle = math.sin(elapsed) * 0.5  # Adjust the amplitude for desired effect
            self.publish_command(1.0, steering_angle)

    def run(self):
        if self.mode == 'straight':
            self.get_logger().info("Running straight line trajectory")
            self.straight_line()
        elif self.mode == 'circle':
            self.get_logger().info("Running circle trajectory")
            self.circle()
        elif self.mode == 'half_sine':
            self.get_logger().info("Running half sine trajectory")
            self.half_sine()
        else:
            self.get_logger().warn("Unknown mode. Available modes: straight, circle, half_sine")

    def timer_callback(self):
        self.run()
        self.timer.cancel()  # Cancel the timer after running the selected trajectory

def main(args=None):
    rclpy.init(args=args)
    controller = TrajectoryController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
