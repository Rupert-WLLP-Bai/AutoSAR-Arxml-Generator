# BS2_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Queued | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------ | ------------------------------ | --------- |
| BS2_CP         | DataSync_CP      | OTSend    | 20ms      | CS        | 6      | TimeOT                         | Structure |
| BS2_CP         | SHM_CP           | OTSend    | 20ms      | CS        | 6      | TimeOT                         | Structure |
| BS2_CP         | DGW2             | OTSend    | 20ms      | CS        | 6      | TimeOT                         | Structure |
| BS2_CP         | VSCP             | OTSend    | 20ms      | CS        | 6      | TimeOT                         | Structure |
| BS2_CP         | SS_CP            | OTSend    | 20ms      | CS        | 6      | TimeOT                         | Structure |
| BS2_CP         | VSS_CP           | OTSend    | 20ms      | CS        | 6      | TimeOT                         | Structure |
| BS2_CP         | DataSync_CP      | WTSend    | 20ms      | CS        | 6      | TimeWT                         | Structure |
| BS2_CP         | SHM_CP           | WTSend    | 20ms      | CS        | 6      | TimeWT                         | Structure |
| BS2_CP         | DGW2             | WTSend    | 20ms      | CS        | 6      | TimeWT                         | Structure |
| BS2_CP         | VSCP             | WTSend    | 20ms      | CS        | 6      | TimeWT                         | Structure |
| BS2_CP         | SS_CP            | WTSend    | 20ms      | CS        | 6      | TimeWT                         | Structure |
| BS2_CP         | VSS_CP           | WTSend    | 20ms      | CS        | 6      | TimeWT                         | Structure |

# WSM

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| WSM            | DataSync_CP      | 20ms      | 20ms      | SR        | WsmSyncSoc                     | Array     |
| WSM            | DataSync_CP      | 20ms      | 20ms      | SR        | WsmSyncOther                   | Array     |
| WSM            | SHM_CP           | 20ms      | 20ms      | SR        | M_Fault                        | Array     |

# VSCP

| Sender /Server | Receiver /Client  | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ----------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| VSCP           | MffMonitor_CP     | 10ms      | 20ms      | SR        | VscpFunctionModeInfo           | Structure |
| VSCP           | MffMonitor_CP     | 10ms      | 20ms      | SR        | VscpAebInfo                    | Structure |
| VSCP           | MffMonitor_CP     | 10ms      | 20ms      | SR        | VscpAdasInfo                   | Structure |
| VSCP           | MffMonitor_CP     | 10ms      | 20ms      | SR        | VscpInfo                       | Structure |
| VSCP           | MRM_CP            | 10ms      | 20ms      | SR        | VscpInfo                       | Structure |
| VSCP           | PncSafetyCheck_CP | 10ms      | 10ms      | SR        | VscpInfo                       | Structure |
| VSCP           | DGW2              | 10ms      | 10ms      | SR        | AEB                            | Structure |
| VSCP           | DGW2              | 10ms      | 10ms      | SR        | APA                            | Structure |
| VSCP           | DGW2              | 10ms      | 10ms      | SR        | LAT                            | Structure |
| VSCP           | DGW2              | 10ms      | 10ms      | SR        | LONG                           | Structure |
| VSCP           | DGW2              | 10ms      | 10ms      | SR        | LightControl                   | Structure |
| VSCP           | DGW2              | 10ms      | 10ms      | SR        | Control_Reserve                | Structure |
| VSCP           | DGW2              | 10ms      | 10ms      | SR        | CPAP                           | Array     |
| VSCP           | SHM_CP            | 10ms      | 20ms      | SR        | M_Fault                        | Array     |
| VSCP           | DataSync_CP       | 10ms      | 20ms      | SR        | VscpInfo                       | Structure |

# SHM_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| SHM_CP         | DataSync_CP      | 20ms      | 20ms      | SR        | Mcu_Fault_Table                | Array     |
| SHM_CP         | DataSync_CP      | 20ms      | 20ms      | SR        | Send_Fault_Table               | Array     |
| SHM_CP         | VSCP             | 20ms      | 20ms      | SR        | M_Fault                        | Array     |
| SHM_CP         | MffMonitor_CP    | 20ms      | 20ms      | SR        | M_Fault                        | Array     |
| SHM_CP         | WSM              | 20ms      | 20ms      | SR        | M_Fault                        | Array     |
| SHM_CP         | MffAEBMonitor_CP | 20ms      | 20ms      | SR        | M_Fault                        | Array     |

# PS_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| PS_CP          | MffPS_CP         | 100ms     | 100ms     | SR        | PsResult                       | Structure |
| PS_CP          | VSCP             | 10ms      | 10ms      | SR        | PsCtrlCmd                      | Structure |

# PncSafetyCheck_CP

| Sender /Server    | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| ----------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| PncSafetyCheck_CP | MRM_CP           | 20ms      | 20ms      | SR        | SafeTraj                       | Structure |
| PncSafetyCheck_CP | MRM_CP           | 20ms      | 20ms      | SR        | SafeCheck                      | Structure |
| PncSafetyCheck_CP | VSCP             | 20ms      | 10ms      | SR        | SafeCheck                      | Structure |

# PA_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| PA_CP          | MffPA_CP         | 100ms     | 100ms     | SR        | USSRT                          | Structure |

# MRM_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| MRM_CP         | VSCP             | 20ms      | 20ms      | SR        | MrmState                       | Value     |
| MRM_CP         | VSCP             | 20ms      | 20ms      | SR        | MrmCtrlCmd                     | Structure |

# MffPS_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| MffPS_CP       | SHM_CP           | 20ms      | 20ms      | SR        | M_Fault                        | Array     |
| MffPS_CP       | PS_CP            | 100ms     | 100ms     | SR        | MffPs                          | Structure |

# MffPA_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| MffPA_CP       | HS_CP            | 100ms     | 100ms     | SR        | ParkingStatusInfo              | Structure |
| MffPA_CP       | HS_CP            | 100ms     | 100ms     | SR        | SettingResponse                | Structure |

# MffMonitor_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| MffMonitor_CP  | VSCP             | 20ms      | 20ms      | SR        | MffMntCmd                      | Structure |
| MffMonitor_CP  | DataSync_CP      | 20ms      | 20ms      | SR        | MffMntInfo                     | Structure |
| MffMonitor_CP  | SHM_CP           | 20ms      | 20ms      | SR        | M_Fault                        | Array     |

# MffAEBMonitor_CP

| Sender /Server   | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| ---------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| MffAEBMonitor_CP | VSCP             | 20ms      | 10ms      | SR        | MffAebReq                      | Structure |
| MffAEBMonitor_CP | MffMonitor_CP    | 20ms      | 10ms      | SR        | MffAebReq                      | Structure |

# MffADAS_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| MffADAS_CP     | VSCP             | 20ms      | 10ms      | SR        | MffAebReq                      | Structure |
| MffADAS_CP     | HS_CP            | 20ms      | 20ms      | SR        | MffAebReq                      | Structure |

# MEB_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| MEB_CP         | MffADAS_CP       | 20ms      | 20ms      | SR        | MebReq                         | Structure |

# HS_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| HS_CP          | MffPA_CP         | 100ms     | 100ms     | SR        | VehicleBodyInfo                | Structure |
| HS_CP          | MffPA_CP         | 100ms     | 100ms     | SR        | SettingRequest                 | Structure |
| HS_CP          | MffPA_CP         | 100ms     | 100ms     | SR        | ParkingInteractionRequest      | Structure |
| HS_CP          | MffPS_CP         | 100ms     | 100ms     | SR        | HmiKey                         | Structure |
| HS_CP          | MffADAS_CP       | 100ms     | 20ms      | SR        | HmiKey                         | Structure |
| HS_CP          | DGW2             | 100ms     | 100ms     | SR        | RawDataHSCP2DGW2               | Array     |

# DS_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| DS_CP          | DGW2             | 20ms      | R_Event   | SR        | CalibReq                       | Structure |

# DGW2

| Sender /Server | Receiver /Client  | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ----------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| DGW2           | WSM               | 20ms      | 20ms      | SR        | WsmSig                         | Array     |
| DGW2           | SHM_CP            | 20ms      | 20ms      | SR        | ShmSig                         | Array     |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_2F                         | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_32                         | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_3A                         | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_3B                         | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_48                         | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_54                         | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_E2                         | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_262                        | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_267                        | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_270                        | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_27B                        | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Can_58E                        | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | Receive_Reserve                | Structure |
| DGW2           | VSCP              | 10ms      | 10ms      | SR        | APCP                           | Structure |
| DGW2           | PncSafetyCheck_CP | 10ms      | 10ms      | SR        | APCP                           | Structure |
| DGW2           | DS_CP             | 20ms      | 20ms      | SR        | CalibResult                    | Structure |
| DGW2           | VSS_CP            | 20ms      | 20ms      | SR        | SignalArray                    | Array     |
| DGW2           | SS_CP             | 10ms      | 10ms      | SR        | Can_Imu                        | Array     |
| DGW2           | SS_CP             | 20ms      | 20ms      | SR        | Can_Uss                        | Array     |
| DGW2           | SS_CP             | 100ms     | 100ms     | SR        | RawGnss                        | Array     |
| DGW2           | SS_CP             | 20ms      | 20ms      | SR        | RawRadarDat155                 | Array     |
| DGW2           | SS_CP             | 20ms      | 20ms      | SR        | RawRadarDat156                 | Array     |
| DGW2           | SS_CP             | 20ms      | 20ms      | SR        | RawRadarDat180                 | Array     |
| DGW2           | SS_CP             | 20ms      | 20ms      | SR        | RawRadarDat181                 | Array     |
| DGW2           | SS_CP             | 20ms      | 20ms      | SR        | RawRadarDat182                 | Array     |
| DGW2           | SS_CP             | 20ms      | 20ms      | SR        | RawRadarDat183                 | Array     |
| DGW2           | SS_CP             | 20ms      | 20ms      | SR        | RawRadarDat184                 | Array     |
| DGW2           | HS_CP             | 20ms      | 20ms      | SR        | RawDataDGW2HSCP                | Array     |
| DGW2           | HS_CP             | 20ms      | 20ms      | SR        | RawDataHSAP2DGW2HSCP           | Array     |

# VSS_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| VSS_CP         | MEB_CP           | 20ms      | 20ms      | SR        | ChassisReport                  | Structure |
| VSS_CP         | MRM_CP           | 20ms      | 20ms      | SR        | ChassisReport                  | Structure |
| VSS_CP         | DDPF_CP          | 20ms      | 20ms      | SR        | WheelReport                    | Structure |
| VSS_CP         | DDPF_CP          | 20ms      | 20ms      | SR        | ChassisReport                  | Structure |
| VSS_CP         | MffMonitor_CP    | 20ms      | 20ms      | SR        | ChassisReport                  | Structure |
| VSS_CP         | MffMonitor_CP    | 20ms      | 20ms      | SR        | BodyReport                     | Structure |
| VSS_CP         | MffMonitor_CP    | 20ms      | 20ms      | SR        | EscState                       | Value     |
| VSS_CP         | MffAEBMonitor_CP | 20ms      | 20ms      | SR        | TPIM                           | Structure |
| VSS_CP         | MffAEBMonitor_CP | 20ms      | 20ms      | SR        | BodyReport                     | Structure |
| VSS_CP         | MffAEBMonitor_CP | 20ms      | 20ms      | SR        | ChassisReport                  | Structure |
| VSS_CP         | MffAEBMonitor_CP | 20ms      | 20ms      | SR        | WheelReport                    | Structure |
| VSS_CP         | MffAEBMonitor_CP | 20ms      | 20ms      | SR        | ESP                            | Structure |
| VSS_CP         | MffAEBMonitor_CP | 20ms      | 20ms      | SR        | EBCM                           | Structure |
| VSS_CP         | MffPS_CP         | 20ms      | 20ms      | SR        | BodyReport                     | Structure |
| VSS_CP         | MffPA_CP         | 20ms      | 20ms      | SR        | BodyReport                     | Structure |
| VSS_CP         | MffPA_CP         | 20ms      | 20ms      | SR        | ChassisReport                  | Structure |
| VSS_CP         | MffADAS_CP       | 20ms      | 20ms      | SR        | BodyReport                     | Structure |
| VSS_CP         | MffADAS_CP       | 20ms      | 20ms      | SR        | WheelReport                    | Structure |
| VSS_CP         | MffADAS_CP       | 20ms      | 20ms      | SR        | ChassisReport                  | Structure |
| VSS_CP         | VSCP             | 20ms      | 20ms      | SR        | Vehicle_Resp                   | Structure |

# SS_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| SS_CP          | PA_CP            | 20ms      | 20ms      | SR        | UltrasonicPackageInput         | Structure |
| SS_CP          | MEB_CP           | 20ms      | 20ms      | SR        | UltrasonicPackageInput         | Structure |
| SS_CP          | DDPF_CP          | 100ms     | 100ms     | SR        | MLAGnss                        | Structure |
| SS_CP          | DDPF_CP          | 10ms      | 10ms      | SR        | MLAImu                         | Structure |
| SS_CP          | MEB_CP           | 20ms      | 20ms      | SR        | UltrasonicPackageInput         | Structure |
| SS_CP          | MEB_CP           | 20ms      | 20ms      | SR        | RadarPerceptionResultFront     | Structure |
| SS_CP          | MEB_CP           | 20ms      | 20ms      | SR        | RadarPerceptionResultRr        | Structure |
| SS_CP          | MEB_CP           | 20ms      | 20ms      | SR        | RadarPerceptionResultRc        | Structure |
| SS_CP          | MEB_CP           | 20ms      | 20ms      | SR        | RadarPerceptionResultLr        | Structure |
| SS_CP          | MEB_CP           | 20ms      | 20ms      | SR        | RadarPerceptionResultLc        | Structure |
| SS_CP          | MEB_CP           | 20ms      | 20ms      | SR        | RadarPerceptionResultLeftTail  | Structure |
| SS_CP          | MEB_CP           | 20ms      | 20ms      | SR        | RadarPerceptionResultRightTail | Structure |
| SS_CP          | AEB_OF_CP        | 20ms      | 20ms      | SR        | RadarPerceptionResultFront     | Structure |
| SS_CP          | AEB_OF_CP        | 20ms      | 20ms      | SR        | RadarPerceptionResultRr        | Structure |
| SS_CP          | AEB_OF_CP        | 20ms      | 20ms      | SR        | RadarPerceptionResultRc        | Structure |
| SS_CP          | AEB_OF_CP        | 20ms      | 20ms      | SR        | RadarPerceptionResultLr        | Structure |
| SS_CP          | AEB_OF_CP        | 20ms      | 20ms      | SR        | RadarPerceptionResultLc        | Structure |
| SS_CP          | AEB_OF_CP        | 20ms      | 20ms      | SR        | RadarPerceptionResultLeftTail  | Structure |
| SS_CP          | AEB_OF_CP        | 20ms      | 20ms      | SR        | RadarPerceptionResultRightTail | Structure |

# DDPF_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| DDPF_CP        | MEB_CP           | 20ms      | 20ms      | SR        | DdpfOut                        | Structure |
| DDPF_CP        | MffADAS_CP       | 20ms      | 20ms      | SR        | DdpfOut                        | Structure |
| DDPF_CP        | MRM_CP           | 20ms      | 20ms      | SR        | DdpfOut                        | Structure |
| DDPF_CP        | PA_CP            | 20ms      | 20ms      | SR        | DdpfOut                        | Structure |
| DDPF_CP        | PS_CP            | 20ms      | 20ms      | SR        | DdpfOut                        | Structure |
| DDPF_CP        | MffAEBMonitor_CP | 20ms      | 20ms      | SR        | DdpfOut                        | Structure |
| DDPF_CP        | MffPS_CP         | 20ms      | 20ms      | SR        | DdpfOut                        | Structure |
| DDPF_CP        | MffMonitor_CP    | 20ms      | 20ms      | SR        | DdpfOut                        | Structure |
| DDPF_CP        | MffPA_CP         | 20ms      | 20ms      | SR        | DdpfOut                        | Structure |

# DataSync_CP

| Sender /Server | Receiver /Client  | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ----------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| DataSync_CP    | MffAEBMonitor_CP  | 20ms      | 20ms      | SR        | SocMpfModule                   | Structure |
| DataSync_CP    | MffADAS_CP        | 20ms      | 20ms      | SR        | SocMpfModule                   | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MdFuncInfo                     | Structure |
| DataSync_CP    | PncSafetyCheck_CP | 20ms      | 20ms      | SR        | PosErrAccum                    | Structure |
| DataSync_CP    | WSM               | 20ms      | 20ms      | SR        | SocSyncWsm                     | Array     |
| DataSync_CP    | WSM               | 20ms      | 20ms      | SR        | OtherSyncWsm                   | Array     |
| DataSync_CP    | AEB_OF_CP         | 20ms      | 20ms      | SR        | FusionAebObject                | Structure |
| DataSync_CP    | MEB_CP            | 20ms      | 20ms      | SR        | FTP                            | Structure |
| DataSync_CP    | PncSafetyCheck_CP | 20ms      | 20ms      | SR        | EgoPoseA                       | Structure |
| DataSync_CP    | PncSafetyCheck_CP | 20ms      | 20ms      | SR        | EgoPoseB                       | Structure |
| DataSync_CP    | MffPS_CP          | 20ms      | 20ms      | SR        | MffAebReq                      | Structure |
| DataSync_CP    | PncSafetyCheck_CP | 20ms      | 20ms      | SR        | DynamicSafetyCheckResultB      | Structure |
| DataSync_CP    | PncSafetyCheck_CP | 20ms      | 20ms      | SR        | DynamicSafetyCheckResultA      | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | FuncModeStateA                 | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | FuncModeStateB                 | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffOddInfo                     | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffPlanningRequestInfo         | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffWorldModelRequestInfo       | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffControlRequestInfo          | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffLocalizationRequestInfo     | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffPredictionRequestInfo       | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffVehicleRequestInfo          | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffPlanningResponseInfo        | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffWorldModelResponseInfo      | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffControlResponseInfo         | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffLocalizationResponseInfo    | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffPredictionResponseInfo      | Structure |
| DataSync_CP    | MffMonitor_CP     | 20ms      | 20ms      | SR        | MffVehicleResponseInfo         | Structure |
| DataSync_CP    | MffADAS_CP        | 20ms      | 20ms      | SR        | MdFuncInfo                     | Structure |
| DataSync_CP    | MffAEBMonitor_CP  | 20ms      | 20ms      | SR        | MdFuncInfo                     | Structure |
| DataSync_CP    | MffAEBMonitor_CP  | 20ms      | 20ms      | SR        | MffAebReq                      | Structure |
| DataSync_CP    | SHM_CP            | 20ms      | 20ms      | SR        | Soc_Fault_Table                | Array     |
| DataSync_CP    | SHM_CP            | 20ms      | 20ms      | SR        | Recv_Fault_Table               | Array     |
| DataSync_CP    | MffADAS_CP        | 20ms      | 20ms      | SR        | SocReady                       | Structure |
| DataSync_CP    | MffPS_CP          | 20ms      | 20ms      | SR        | SocReady                       | Structure |
| DataSync_CP    | MffPA_CP          | 20ms      | 20ms      | SR        | SocReady                       | Structure |

# AEB_OF_CP

| Sender /Server | Receiver /Client | S_Trigger | R_Trigger | Port type | Element(Structure/Array/Value) | Data type |
| -------------- | ---------------- | --------- | --------- | --------- | ------------------------------ | --------- |
| AEB_OF_CP      | MffAEBMonitor_CP | 20ms      | 20ms      | SR        | AebOFResult                    | Structure |
