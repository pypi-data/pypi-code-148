# SWLS Resonant Converter
list_soft_interlocks = []

list_hard_interlocks = [
    "Load Overcurrent",
    "DCLink Overvoltage",
    "DCLink Undervoltage",
]

bsmp = {
    "ps_alarms": {"addr": 33, "format": "I", "size": 4, "egu": ""},
    "i_load": {"addr": 34, "format": "f", "size": 4, "egu": "A"},
    "v_dclink": {"addr": 35, "format": "f", "size": 4, "egu": "V"},
    "i_load_error": {"addr": 36, "format": "f", "size": 4, "egu": "A"},
    "freq_modulated": {"addr": 37, "format": "f", "size": 4, "egu": "Hz"},
    "freq_modulated_ff": {"addr": 38, "format": "f", "size": 4, "egu": "Hz"},
}