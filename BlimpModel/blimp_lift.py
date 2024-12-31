import math
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

class BlimpLift:
    def __init__(self, payload_grams, helium_liters, bladder_fill_volume=0, VARIABLE_CHAMBER_SIZE=14):
        """
        Initialize blimp with given specifications
        
        Args:
            payload_grams: Weight of payload in grams
            helium_liters: Main helium volume in liters
            bladder_fill_volume: Amount of air in the VARIABLE_CHAMBER_SIZE variable chamber (0-VARIABLE_CHAMBER_SIZE L)
            VARIABLE_CHAMBER_SIZE: Maximum volume of the variable chamber in liters
        """ 
        self.VARIABLE_CHAMBER_SIZE = VARIABLE_CHAMBER_SIZE  # Liters
        self.payload_kg = payload_grams / 1000
        self.main_helium_volume = helium_liters
        
        # Validate and set internal helium volume
        if 0 <= bladder_fill_volume <= self.VARIABLE_CHAMBER_SIZE:
            self.bladder_fill_volume = bladder_fill_volume
        else:
            raise ValueError(f"Internal helium volume must be between 0 and {self.VARIABLE_CHAMBER_SIZE} liters")
            
    def get_pressure_at_altitude(self, altitude):
        """Calculate atmospheric pressure at given altitude"""
        P0 = 101325  # Sea level pressure (Pa)
        M = 0.02896968  # Molar mass of air (kg/mol)
        g = 9.80665  # Gravity (m/s²)
        R0 = 8.31446  # Gas constant (J/(mol·K))
        T0 = 288.15  # Standard temperature (K)
        
        return P0 * math.exp((-g * M * altitude) / (R0 * T0))
    
    def calculate_densities(self, temperature_c, altitude=0):
        """Calculate air and helium densities at given conditions"""
        T = temperature_c + 273.15  # Convert to Kelvin
        P = self.get_pressure_at_altitude(altitude)
        R = 8.31446  # Gas constant
        
        # Calculate densities using ideal gas law
        air_density = (P * 0.02896968) / (R * T)  # kg/m³
        helium_density = (P * 0.004002602) / (R * T)  # kg/m³
        
        return air_density, helium_density
    
    def calculate_lift(self, temperature_c, altitude=0):
        """
        Calculate net lift force in Newtons
        
        Args:
            temperature_c: Temperature in Celsius
            altitude: Altitude in meters
            
        Returns:
            tuple: (net_lift_force_N, lift_margin_kg)
        """
        air_density, helium_density = self.calculate_densities(temperature_c, altitude)
        g = 9.81  # m/s²
        
        # Convert liters to m³
        main_volume_m3 = self.main_helium_volume / 1000
        internal_air_m3 = self.bladder_fill_volume / 1000
        
        # Calculate masses of gases
        helium_mass = helium_density * main_volume_m3  # helium mass won't change by filling
        air_mass = air_density * internal_air_m3
        
        buoyant_force = air_density * main_volume_m3 * g
        
        # Calculate weight force
        weight_force = (helium_mass + air_mass + self.payload_kg) * g
        
        # Calculate net lift
        net_lift = buoyant_force - weight_force
        lift_margin_kg = net_lift / g
    
        return net_lift, lift_margin_kg
