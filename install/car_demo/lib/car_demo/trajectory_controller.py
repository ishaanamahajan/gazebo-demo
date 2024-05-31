#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from prius_msgs.msg import Control
import math
import time

class TrajectoryController(Node):
    def __init__(self):
        super().__init__('trajectory_controller')
        
        # Create a publisher to the /prius/control topic
        self.pub = self.create_publisher(Control, '/prius/control', 10)
        
        # Declare and get parameters
        self.declare_parameter('mode', 'straight')
        self.declare_parameter('duration', 10)  # This will only be used for the straight line trajectory
        self.mode = self.get_parameter('mode').get_parameter_value().string_value
        self.duration = self.get_parameter('duration').get_parameter_value().integer_value

        # Desired velocity
        self.desired_velocity = 2.0  # m/s
        
        # Throttle value for achieving the desired velocity (needs fine-tuning)
        self.throttle_value = 0.8  # Adjust this value based on your vehicle model
        
        # Set the loop rate
        self.timer_period = 0.1  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # Variables for trajectory timing
        self.start_time = self.get_clock().now().seconds_nanoseconds()[0]
        self.end_time = self.start_time + self.duration

        # Half sine phase durations (calculated based on required behavior)
        self.half_sine_phase_duration = 5  # 5 seconds for each phase: left, straight, right

    def publish_command(self, throttle, steering):
        control_msg = Control()
        control_msg.throttle = throttle
        control_msg.steer = steering
        control_msg.brake = 0.0
        control_msg.shift_gears = Control.NO_COMMAND
        self.pub.publish(control_msg)

    def straight_line(self):
        while self.get_clock().now().seconds_nanoseconds()[0] < self.end_time:
            self.publish_command(self.throttle_value, 0.0)
            time.sleep(0.1)

    def circle(self):
        while rclpy.ok():
            self.publish_command(self.throttle_value, -0.5)  # Adjust the steering angle for the right turn circle
            time.sleep(0.1)  # Sleep for a short duration to allow continuous publishing

    def half_sine(self):
        phase_start_time = self.get_clock().now().seconds_nanoseconds()[0]
        
        # Phase 1: Steer left
        while self.get_clock().now().seconds_nanoseconds()[0] < phase_start_time + self.half_sine_phase_duration:
            self.publish_command(self.throttle_value, 0.5)  # Adjust the steering angle for left turn
            time.sleep(0.1)
        
        # Phase 2: Go straight
        phase_start_time += self.half_sine_phase_duration
        while self.get_clock().now().seconds_nanoseconds()[0] < phase_start_time + self.half_sine_phase_duration:
            self.publish_command(self.throttle_value, 0.0)  # Straight
            time.sleep(0.1)
        
        # Phase 3: Steer right
        phase_start_time += self.half_sine_phase_duration
        while self.get_clock().now().seconds_nanoseconds()[0] < phase_start_time + self.half_sine_phase_duration:
            self.publish_command(self.throttle_value, -0.5)  # Adjust the steering angle for right turn
            time.sleep(0.1)

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
