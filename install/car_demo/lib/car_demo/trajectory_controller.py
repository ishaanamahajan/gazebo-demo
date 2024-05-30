#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from prius_msgs.msg import Control
import math

class TrajectoryController(Node):
    def __init__(self):
        super().__init__('trajectory_controller')
        
        # Create a publisher to the /prius/control topic
        self.pub = self.create_publisher(Control, '/prius/control', 10)
        
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
        self.end_time = self.start_time + self.duration

    def publish_command(self, throttle, steering):
        control_msg = Control()
        control_msg.throttle = throttle
        control_msg.steer = steering
        control_msg.brake = 0.0
        control_msg.shift_gears = Control.NO_COMMAND
        self.pub.publish(control_msg)

    def straight_line(self):
        while self.get_clock().now().seconds_nanoseconds()[0] < self.end_time:
            self.publish_command(1.0, 0.0)

    def circle(self):
        while self.get_clock().now().seconds_nanoseconds()[0] < self.end_time:
            self.publish_command(1.0, 0.5)  # Adjust the steering angle for the circle

    def half_sine(self):
        while self.get_clock().now().seconds_nanoseconds()[0] < self.end_time:
            elapsed = self.get_clock().now().seconds_nanoseconds()[0] - self.start_time
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
