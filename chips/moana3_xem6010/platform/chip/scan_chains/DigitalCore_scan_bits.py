#-------------------------------------------------------------------------------------------
# This file was auto generated with the command:
# scan-to-python.pl scan_defines/DigitalCore_scan_bits.cfg DigitalCore_scan_bits.py
# Config file contents:
#                          Field Name       Dir     Width      Mult
#-------------------------------------------------------------------------------------------
#                          TDCDCBoost         W         1         8
#                           TDCStatus         R         1         8
#                       TDCFineOutRaw         R         8         8
#                        TDCCoarseOut         R         7         8
#                       DynamicPacket         R        17         1
#     PattResetControlledByTriggerExt         W         1         1
#                  PattResetExtEnable         W         1         1
#                         MeasPerPatt         W        24         1
#                     MeasCountEnable         W         1         1
#                 VCSELEnableWithScan         W         1         1
#         VCSELEnableControlledByScan         W         1         1
#                    VCSELWave1Enable         W         1         1
#                    VCSELWave2Enable         W         1         1
#                      TDCStartSelect         W         1         8
#                       TDCStopSelect         W         1         8
#                          TDCDisable         W         1         8
#                          SPADEnable         W         1        64
#                 DynamicConfigEnable         W         1         1
#                      TestPattEnable         W         1         1
#                          TestDataIn         W        10         1
#              TxDataExtRequestEnable         W         1         1
#                      TimeOffsetWord         W        10         1
#                    SubtractorBypass         W         1         1
#                           ClkBypass         W         1         1
#                             ClkFlip         W         1         1
#       DriverDLLWordControlledByScan         W         1         1
#                       DriverDLLWord         W         5         1
#          AQCDLLWordControlledByScan         W         1         1
#                    AQCDLLCoarseWord         W         4         1
#                      AQCDLLFineWord         W         3         1
#                    AQCDLLFinestWord         W         1         1
#
# Scan Chain Module Name = DigitalCore_scan_bits
# Scanchain Length = 313
#-------------------------------------------------------------------------------------------

from numpy import binary_repr

#-------------------------------------------------------------------------------------------
#    Class DigitalCore_scan_bits
#-------------------------------------------------------------------------------------------
class DigitalCore_scan_bits:

    #-----------------------------------------------------------------------------------
    #    Constructor
    #-----------------------------------------------------------------------------------
    def __init__(self, \
        TDCDCBoost                           = '0' * 8     , \
        TDCStatus                            = '0' * 8     , \
        TDCFineOutRaw                        = '0' * 64    , \
        TDCCoarseOut                         = '0' * 56    , \
        DynamicPacket                        = '0' * 17    , \
        PattResetControlledByTriggerExt      = '0' * 1     , \
        PattResetExtEnable                   = '0' * 1     , \
        MeasPerPatt                          = '0' * 24    , \
        MeasCountEnable                      = '0' * 1     , \
        VCSELEnableWithScan                  = '0' * 1     , \
        VCSELEnableControlledByScan          = '0' * 1     , \
        VCSELWave1Enable                     = '0' * 1     , \
        VCSELWave2Enable                     = '0' * 1     , \
        TDCStartSelect                       = '0' * 8     , \
        TDCStopSelect                        = '0' * 8     , \
        TDCDisable                           = '0' * 8     , \
        SPADEnable                           = '0' * 64    , \
        DynamicConfigEnable                  = '0' * 1     , \
        TestPattEnable                       = '0' * 1     , \
        TestDataIn                           = '0' * 10    , \
        TxDataExtRequestEnable               = '0' * 1     , \
        TimeOffsetWord                       = '0' * 10    , \
        SubtractorBypass                     = '0' * 1     , \
        ClkBypass                            = '0' * 1     , \
        ClkFlip                              = '0' * 1     , \
        DriverDLLWordControlledByScan        = '0' * 1     , \
        DriverDLLWord                        = '0' * 5     , \
        AQCDLLWordControlledByScan           = '0' * 1     , \
        AQCDLLCoarseWord                     = '0' * 4     , \
        AQCDLLFineWord                       = '0' * 3     , \
        AQCDLLFinestWord                     = '0' * 1     , \
        filler                               = '0' * 0     ):

        self.filler                               = filler
        self.TDCDCBoost                           = TDCDCBoost
        self.TDCStatus                            = TDCStatus
        self.TDCFineOutRaw                        = TDCFineOutRaw
        self.TDCCoarseOut                         = TDCCoarseOut
        self.DynamicPacket                        = DynamicPacket
        self.PattResetControlledByTriggerExt      = PattResetControlledByTriggerExt
        self.PattResetExtEnable                   = PattResetExtEnable
        self.MeasPerPatt                          = MeasPerPatt
        self.MeasCountEnable                      = MeasCountEnable
        self.VCSELEnableWithScan                  = VCSELEnableWithScan
        self.VCSELEnableControlledByScan          = VCSELEnableControlledByScan
        self.VCSELWave1Enable                     = VCSELWave1Enable
        self.VCSELWave2Enable                     = VCSELWave2Enable
        self.TDCStartSelect                       = TDCStartSelect
        self.TDCStopSelect                        = TDCStopSelect
        self.TDCDisable                           = TDCDisable
        self.SPADEnable                           = SPADEnable
        self.DynamicConfigEnable                  = DynamicConfigEnable
        self.TestPattEnable                       = TestPattEnable
        self.TestDataIn                           = TestDataIn
        self.TxDataExtRequestEnable               = TxDataExtRequestEnable
        self.TimeOffsetWord                       = TimeOffsetWord
        self.SubtractorBypass                     = SubtractorBypass
        self.ClkBypass                            = ClkBypass
        self.ClkFlip                              = ClkFlip
        self.DriverDLLWordControlledByScan        = DriverDLLWordControlledByScan
        self.DriverDLLWord                        = DriverDLLWord
        self.AQCDLLWordControlledByScan           = AQCDLLWordControlledByScan
        self.AQCDLLCoarseWord                     = AQCDLLCoarseWord
        self.AQCDLLFineWord                       = AQCDLLFineWord
        self.AQCDLLFinestWord                     = AQCDLLFinestWord
        
    #-----------------------------------------------------------------------------------
    
    #-----------------------------------------------------------------------------------
    #    Get scan chain length
    #-----------------------------------------------------------------------------------
    def length(self): 
        return 313

    @staticmethod
    def length_static(): 
        return 313

    #-----------------------------------------------------------------------------------
    
    #-----------------------------------------------------------------------------------
    #    Construct bits from class
    #-----------------------------------------------------------------------------------
    def to_bits(self): 
        
        bits = self.filler
        bits += self.AQCDLLFinestWord
        bits += self.AQCDLLFineWord
        bits += self.AQCDLLCoarseWord
        bits += self.AQCDLLWordControlledByScan
        bits += self.DriverDLLWord
        bits += self.DriverDLLWordControlledByScan
        bits += self.ClkFlip
        bits += self.ClkBypass
        bits += self.SubtractorBypass
        bits += self.TimeOffsetWord
        bits += self.TxDataExtRequestEnable
        bits += self.TestDataIn
        bits += self.TestPattEnable
        bits += self.DynamicConfigEnable
        bits += self.SPADEnable
        bits += self.TDCDisable
        bits += self.TDCStopSelect
        bits += self.TDCStartSelect
        bits += self.VCSELWave2Enable
        bits += self.VCSELWave1Enable
        bits += self.VCSELEnableControlledByScan
        bits += self.VCSELEnableWithScan
        bits += self.MeasCountEnable
        bits += self.MeasPerPatt
        bits += self.PattResetExtEnable
        bits += self.PattResetControlledByTriggerExt
        bits += self.DynamicPacket
        bits += self.TDCCoarseOut
        bits += self.TDCFineOutRaw
        bits += self.TDCStatus
        bits += self.TDCDCBoost
        
        # Output check
        if len(bits) != self.length():
            raise ValueError("Error, expecting 313 bits, got " + str(len(bits)) + "!")
        
        # Return output
        return(bits)
        
    #-----------------------------------------------------------------------------------
    
    #-----------------------------------------------------------------------------------
    #    Construct class from bits
    #-----------------------------------------------------------------------------------
    @classmethod
    def from_bits(cls, bits): 
        
        # Check length of bits
        if len(bits) != 313:
            raise ValueError("Error, expecting 313 bits, got " + str(len(bits)) + "!")
        
        # Create class
        return cls( \
            AQCDLLFinestWord                     = bits[     0:1     ], \
            AQCDLLFineWord                       = bits[     1:4     ], \
            AQCDLLCoarseWord                     = bits[     4:8     ], \
            AQCDLLWordControlledByScan           = bits[     8:9     ], \
            DriverDLLWord                        = bits[     9:14    ], \
            DriverDLLWordControlledByScan        = bits[    14:15    ], \
            ClkFlip                              = bits[    15:16    ], \
            ClkBypass                            = bits[    16:17    ], \
            SubtractorBypass                     = bits[    17:18    ], \
            TimeOffsetWord                       = bits[    18:28    ], \
            TxDataExtRequestEnable               = bits[    28:29    ], \
            TestDataIn                           = bits[    29:39    ], \
            TestPattEnable                       = bits[    39:40    ], \
            DynamicConfigEnable                  = bits[    40:41    ], \
            SPADEnable                           = bits[    41:105   ], \
            TDCDisable                           = bits[   105:113   ], \
            TDCStopSelect                        = bits[   113:121   ], \
            TDCStartSelect                       = bits[   121:129   ], \
            VCSELWave2Enable                     = bits[   129:130   ], \
            VCSELWave1Enable                     = bits[   130:131   ], \
            VCSELEnableControlledByScan          = bits[   131:132   ], \
            VCSELEnableWithScan                  = bits[   132:133   ], \
            MeasCountEnable                      = bits[   133:134   ], \
            MeasPerPatt                          = bits[   134:158   ], \
            PattResetExtEnable                   = bits[   158:159   ], \
            PattResetControlledByTriggerExt      = bits[   159:160   ], \
            DynamicPacket                        = bits[   160:177   ], \
            TDCCoarseOut                         = bits[   177:233   ], \
            TDCFineOutRaw                        = bits[   233:297   ], \
            TDCStatus                            = bits[   297:305   ], \
            TDCDCBoost                           = bits[   305:313   ], \
            filler                               = '0' * 0)
            
    #-----------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------------------
