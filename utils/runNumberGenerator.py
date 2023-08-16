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
   where 0: 65; ...; 8: 85

<3>: azimuth: 0-9
   where 0: 0; ...; 8: 360

<4>: empty (0)

<5>: shower variation

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
                             (0,65.0) : 0,
                             (65.1,67.5) : 1,
                             (67.6,70.0) : 2,
                             (70.1, 72.5) : 3,
                             (72.6,75.0) : 4,
                             (75.1,77.5) : 5,
                             (77.6, 80.0) : 6,
                             (80.1,82.5) : 7,
                             (82.6,85.0) : 8,
                             (85.1,90) : 9,
                            }
        
        
        self.azimuthDict = {
                             (0.0, 44.9)  : 0,
                             (45, 89.9) : 1,
                             (90.0, 134.9) : 2,
                             (135.0, 179.9): 3,
                             (180.0, 224.9): 4,
                             (225.0, 269.9): 5,
                             (270.0, 314.9): 6,
                             (315.0, 360): 7,
                             (-0.1, -180) : 8,
                             (-180.1, -360) : 9,
                                    }
        
        # TODO: update for more particles
        self.primaryDict = {
                            14:   0,      # Protons (H) - get ID 0
                            5626: 1,      # Iron (Fe) - get ID 1
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
    