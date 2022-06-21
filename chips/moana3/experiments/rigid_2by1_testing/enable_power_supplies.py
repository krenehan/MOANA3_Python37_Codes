# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:01:11 2020

The purpose of this script is to turn on power supplies on the motherboard to verify their operation.
Note that jumpers on the boards need to be set correctly for this to be an effective test.

@author: Kevin Renehan
"""

# =============================================================================
# Includes
# =============================================================================
from includes import *


# =============================================================================
# Setup
# =============================================================================

# In order for any LDOs to be enabled, the "DVDD from Opal Kelly" and "VDC from Opal Kelly" jumpers should be plugged in
# Ensure this is the case before proceeding

# -------------------------------------------------------
# HVDD Source - Can come from HVDD LDO, or from FPGA
# To select HVDD from FPGA, connect jumper that says "HVDD from Opal Kelly" (default)
# To select HVDD from LDO, connect jumper that says "HVDD from LDO"
# These jumpers should not be plugged in at the same time
enable_hvdd_ldo_supply = True

# -------------------------------------------------------
# VRST Source - Can come from VRST LDO, or by shorting VRST to HVDD
# To select VRST from HVDD, connect jumper that says "Short VRST to HVDD"
# To select VRST from LDO, connect jumper that says "VRST from LDO"
# These jumpers should not be plugged in at the same time
enable_vrst_ldo_supply = False

# -------------------------------------------------------
# CATH Source - Comes from SPAD CATH SM
# To select VDD from SM, connect jumper that says "SPAD CATH from SM" (default)
enable_cath_switchmode_supply = False

# -------------------------------------------------------
# SPAD CATH Source - Comes from SPAD CATH SM on the Cathode Boost Module (attachment board on motherboard)
# To select SPAD CATH from the SPAD CATH SM supply, connect jumper that says "Enable" and "Connect Filt"



# =============================================================================
# Equipment Setup
# =============================================================================
# Waiting time (between scans)
config_wait = 0.0
read_wait   = 0.2
equip_wait  = 0.5
ldo_wait = 0.5

# Equipment
func_gen        = None
supply_main     = None
supply_aux      = None


try:
    # =============================================================================
    # Platform Setup
    # =============================================================================
    dut = test_platform.TestPlatform("moana3")
    dut.init_fpga(bitfile_path = paths.bitfile_path)
    time.sleep(1)
    
    
    # =============================================================================
    # Power Setup - Initialize power supplies
    # =============================================================================
    # Status bit to prevent overlap
    hvdd_supply_set = False
    vrst_supply_set = False
    cath_supply_set = False
        
    # HVDD LDO Supply
    if enable_hvdd_ldo_supply:
        dut.enable_hvdd_ldo_supply()
        time.sleep(ldo_wait)
        hvdd_supply_set = True
        
    # VRST LDO Supply
    if enable_vrst_ldo_supply:
        dut.enable_vrst_ldo_supply()
        time.sleep(ldo_wait)
        vrst_supply_set = True
        
    # Cathode SM Supply
    if enable_cath_switchmode_supply:
        dut.enable_cath_sm_supply()
        time.sleep(ldo_wait)
        cath_supply_set = True
        
    # Check VRST
    dut.check_vrst_high()
        
    # Check vdd_sm
    dut.check_vdd_sm_supply()
        
    # Prompt
    total = hvdd_supply_set + vrst_supply_set + cath_supply_set
    if total:
        
        s = ""
        if hvdd_supply_set:
            s = s + "HVDD & "
        if vrst_supply_set:
            s = s + "VRST & "
        if cath_supply_set:
            s = s + "CATH & "
            
        # Remove last &
        s = s = s[0:len(s)-2]
        
        # Finish
        if total > 1:
            s = s + "supplies enabled"
        else:
            s = s + "supply enabled"
        
        # Wait a few minutes
        print(s)
        print("Halting for 5 minutes")
        print("Verify supply voltages")
        print("Ctrl-C to exit")
        for i in range(0, 3000):
            time.sleep(0.1)
            
    else:
        
        # No supplies set
        print("No supplies set")
    

finally:
    # Disable power supplies
    dut.disable_hvdd_ldo_supply()
    dut.disable_vrst_ldo_supply()
    dut.disable_cath_sm_supply()
            
    # Close FPGA
    print("Closing FPGA")
    dut.fpga_interface.xem.Close()
    
    print("Done")
