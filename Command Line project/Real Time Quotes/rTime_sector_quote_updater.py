##UPDATES sector_rTime google sheet

# IMPORTS #
import pyEX as p

import time

import pandas as pd
import numpy as np
import datetime as dt
from copy import copy

import google_sheets_api as sheet


def update_sector_rTime():
    print("updating sector_rTime sheet....")
    sectorPerformance = p.sectorPerformanceDF() #all sectors
    techSector = sectorPerformance.iloc[9] #tech sector
    
    timestamp = techSector[0] #time date
    performance = techSector[1] #change
    
    sheet.sector_rTime.append_row([str(timestamp),performance])#send to google

