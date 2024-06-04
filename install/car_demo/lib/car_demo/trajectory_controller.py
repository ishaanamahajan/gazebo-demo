#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from prius_msgs.msg import Control
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
        self.throttle_value = 2.0  # Adjust this value based on your vehicle model
        
        # Set the loop rate
        self.timer_period = 0.1  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # Variables for trajectory timing
        self.start_time = self.get_clock().now().seconds_nanoseconds()[0]
        self.end_time = self.start_time + self.duration

        # Half sine phase durations
        self.initial_straight_duration = 5  # seconds for initial straight motion
        self.turn_duration = 6  # seconds for each half of the semi-circle

    def publish_command(self, throttle, steering):
        control_msg = Control()
        control_msg.throttle = throttle
        control_msg.steer = steering
        control_msg.brake = 0.0
        control_msg.shift_gears = Control.FORWARD
        self.pub.publish(control_msg)
        self.get_logger().info(f"Published command: throttle={throttle}, steer={steering}")

    def straight_line(self):
        while self.get_clock().now().seconds_nanoseconds()[0] < self.end_time:
            self.publish_command(self.throttle_value, 0.0)
            time.sleep(0.1)

    def circle(self):
        while rclpy.ok():
            self.publish_command(self.throttle_value, -0.5)  # Adjust the steering angle for the right turn circle
            time.sleep(0.1)  # Sleep for a short duration to allow continuous publishing

    def half_sine(self):
        current_time = self.get_clock().now().seconds_nanoseconds()[0]

        # Initial straight motion
        phase_end_time = current_time + self.initial_straight_duration
        while self.get_clock().now().seconds_nanoseconds()[0] < phase_end_time:
            self.publish_command(self.throttle_value, 0.0)
            time.sleep(0.1)

        # Phase 1: Steer left to create the first half of the semi-circle
        current_time = self.get_clock().now().seconds_nanoseconds()[0]
        phase_end_time = current_time + self.turn_duration
        while self.get_clock().now().seconds_nanoseconds()[0] < phase_end_time:
            self.publish_command(self.throttle_value, 0.3)  # Adjust the steering angle for left turn
            time.sleep(0.1)

        phase_end_time = current_time + self.initial_straight_duration
        while self.get_clock().now().seconds_nanoseconds()[0] < phase_end_time:
            self.publish_command(self.throttle_value, 0.0)
            time.sleep(0.1)

        # Phase 2: Steer right to create the second half of the semi-circle
        current_time = self.get_clock().now().seconds_nanoseconds()[0]
        phase_end_time = current_time + self.turn_duration
        while self.get_clock().now().seconds_nanoseconds()[0] < phase_end_time:
            self.publish_command(self.throttle_value, -0.3)  # Adjust the steering angle for right turn
            time.sleep(0.1)

    def run(self):
        time.sleep(5)

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
