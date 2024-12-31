import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from .blimp_lift import BlimpLift

class BlimpMotionZ(BlimpLift):
    """
    Class for simulating blimp motion in the z-axis, inheriting from BlimpLift.
    """
    def __init__(self, payload_grams, helium_liters, bladder_fill_volume=0, VARIABLE_CHAMBER_SIZE=14):
        super().__init__(payload_grams, helium_liters, bladder_fill_volume, VARIABLE_CHAMBER_SIZE)
    
    def simulate_motion(self, csv_path, total_time=60, dt=0.1):
        """
        Simulates the blimp's motion over time using time-series temperature and altitude data.
        
        Args:
            csv_path (str): Path to the CSV file containing temperature and altitude data.
            total_time (float): Total simulation time in seconds.
            dt (float): Time step in seconds.
            
        Returns:
            dict: Contains time, position, speed, and acceleration data.
        """
        # Read the time-series data from the CSV
        data = pd.read_csv(csv_path)
        altitudes = data['altitude'].values
        temperatures = data['temperature'].values
        
        # Time steps
        time_points = np.arange(0, total_time, dt)
        
        # Initialize simulation variables
        position = 0
        speed = 0
        altitude_index = 0
        
        position_history = []
        speed_history = []
        acceleration_history = []
        time_history = []
        
        for t in time_points:
            # Update the temperature and altitude based on position
            if altitude_index < len(altitudes) - 1 and position >= altitudes[altitude_index + 1]:
                altitude_index += 1
            
            current_temperature = temperatures[altitude_index]
            current_altitude = position  # Current position is treated as altitude
            
            # Calculate net lift force
            net_lift_force, _ = self.calculate_lift(current_temperature, current_altitude)
            
            # Calculate air and helium densities
            air_density, helium_density = self.calculate_densities(current_temperature, current_altitude)
            
            # Calculate total mass of the blimp
            total_mass = self.payload_kg + (self.main_helium_volume / 1000 * helium_density)
            
            # Acceleration = Force / Mass
            acceleration = net_lift_force / total_mass
            
            # Update speed and position
            speed += acceleration * dt
            position += speed * dt
            
            # Store simulation data
            position_history.append(position)
            speed_history.append(speed)
            acceleration_history.append(acceleration)
            time_history.append(t)
        
        return {
            "time": time_history,
            "position": position_history,
            "speed": speed_history,
            "acceleration": acceleration_history,
        }
    
    def plot_results(self, simulation_results):
        """
        Plots the simulation results for position, speed, and acceleration.
        
        Args:
            simulation_results (dict): Results from the simulation.
        """
        time = simulation_results['time']
        position = simulation_results['position']
        speed = simulation_results['speed']
        acceleration = simulation_results['acceleration']
        
        # Plot position, speed, and acceleration vs time
        plt.figure(figsize=(10, 8))
        
        # Position
        plt.subplot(3, 1, 1)
        plt.plot(time, position, label="Position (m)", color="blue")
        plt.xlabel("Time (s)")
        plt.ylabel("Position (m)")
        plt.title("Position vs Time")
        plt.grid()
        
        # Speed
        plt.subplot(3, 1, 2)
        plt.plot(time, speed, label="Speed (m/s)", color="green")
        plt.xlabel("Time (s)")
        plt.ylabel("Speed (m/s)")
        plt.title("Speed vs Time")
        plt.grid()
        
        # Acceleration
        plt.subplot(3, 1, 3)
        plt.plot(time, acceleration, label="Acceleration (m/s²)", color="red")
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (m/s²)")
        plt.title("Acceleration vs Time")
        plt.grid()
        
        plt.tight_layout()
        plt.show()


