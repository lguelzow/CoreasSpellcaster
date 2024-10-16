#!/usr/bin/env python3
# author: Jelena

import numpy as np

"""
This class is used to generate runNumbers according to this structure:

RunNumber: <012345>

<0>: proton - 0; iron - 1

<1>: energy: x.0-x.9
   where 0: x.0  (log GeV) - corresponds to E18eV

<2>: zenith: 0-9
    in ranges (see below)

<3>: azimuth: 0-9
    in ranges (see below)

<4>: empty (0)

<5>: shower variation: 0-9

*********

@author: Jelena
@date: June 2023

"""

class runNumberGenerator:
    """
    This class has functions that are used to create the runNumber in SimulationMaker.py.
        
    Dictionaries:
        energies:       the array binned in energies for the simulation
        zenith:         the zenith angle
        azimuth:        the azimuth angle
        primary:        the primary particle
    
    """
    def __init__(self):

        self.zenithDict = {
                             (0,65.09) : 0,
                             (65.1,67.59) : 1,
                             (67.6,70.09) : 2,
                             (70.1, 72.59) : 3,
                             (72.6,75.09) : 4,
                             (75.1,77.59) : 5,
                             (77.6, 80.09) : 6,
                             (80.1,82.59) : 7,
                             (82.6,85.09) : 8,
                             (85.1,90) : 9,
                            }
        
        
        self.azimuthDict = {
                             (0.0, 44.99)  : 0,
                             (45, 89.99) : 1,
                             (90.0, 134.99) : 2,
                             (135.0, 179.99): 3,
                             (180.0, 224.99): 4,
                             (225.0, 269.99): 5,
                             (270.0, 314.99): 6,
                             (315.0, 360): 7,
                             (-0.1, -180) : 8,
                             (-180.1, -360) : 9,
                                    }
        
        # TODO: update for more particles
        self.primaryDict = {
                            14:   0,      # Protons (H) - get ID 0
                            5626: 1,      # Iron (Fe) - get ID 1
                                    }


        self.energyDict = {
                             (7.0,7.9) : 0,
                             (8.0,8.9) : 1,
                             (9.0,9.9) : 2,
                             (10.0,10.9) : 3,
                             (11.0,11.9) : 4,
                             (12.0,12.9) : 5,
                            }


    def getZenithID(self, zenith_angle):
        for (lower, upper), category in self.zenithDict.items():
            if lower <= zenith_angle <= upper:
                return category
        raise ValueError("Zenith angle not found in any runNumber category")

    

    
    def getAzimuthID(self, azimuth_angle):
        for (lower, upper), category in self.azimuthDict.items():
            if lower <= azimuth_angle <= upper:
                return category
        raise ValueError("Azimuth angle not found in any runNumber category")
    


    def getPrimaryID(self, primary_particle):
        return self.primaryDict[primary_particle]
    
    def getEnergyID(self, log10_E1):
        for (lower, upper), category in self.energyDict.items():
            if lower <= log10_E1 <= upper:
                return category
        raise ValueError("Energy not found in any runNumber category")
    