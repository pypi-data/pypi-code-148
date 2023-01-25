
def _get_value_by_response(a):
    measurement = a[-(9 + 1 + 3 + 4):]  # remove escape \r\n
    if measurement == '':
        return None  # measurement error
    try:
        val = float(measurement)
    except ValueError:
        raise Exception(f'invalid measurement value "{measurement}"')
    return val


class Fluke_PM6666:
    """Fluke PM6666 frequency counter"""

    from PyAR488.PyAR488 import AR488

    _functions = {
        'FREQ_A': 'FREQ A',  # channel A frequency
        'FREQ_B': 'FREQ B',  # channel B frequency
        'FREQ_C': 'FREQ C',  # channel C frequency ( if present )
        'PERIOD A': 'PER A',  # channel A period
        'DT_AB': 'TIME A,B',  # time interval between A trig abd B trig
        'DT_BA': 'TIME B,A',  # time interval between B trig abd A trig
        'TOT_A_GATE_B': 'TOTG A,B',  # total A pulses gated by B
        'TOT_B_GATE_A': 'TOTG B,A',  # total B pulses gated by A
        'TOT_A_SS_B': 'TOTS A,B',  # total A pulses started and stopped by B
        'TOT_B_SS_A': 'TOTS B,A',  # total B pulses started and stopped by A
        'TOT_A_BUS': 'TOTM A',  # total A pulses gated bus gate open/close
        'TOT_B_BUS': 'TOTM B',  # total B pulses gated bus gate open/close
        'RATIO_AB': 'RATIO A,B',  # number of A pulses  / number of B pulses
        'RATIO_BA': 'RATIO B,A',  # number of B pulses  / number of A pulses
        'RATIO_CA': 'RATIO C,A',  # number of C pulses  / number of A pulses
        'RATIO_CB': 'RATIO C,B',  # number of C pulses  / number of B pulses
        'VMAX_A': 'VMAX A',  # positive peak voltage on input A
        'VMIN_A': 'VMIN A',  # negative peak voltage on input A
        'VMAX_B': 'VMAX B',  # positive peak voltage on input B
        'VMIN_B': 'VMIN B'  # negative peak voltage on input B
    }
    _inputs = {
        'A': 'INPA',
        'B': 'INPB',
    }
    _trigger_slope = {
        '+': 'TRGSLP POS',  # triggering on positive slope
        '-': 'TRGSLP NEG',  # triggering on negative slope
    }
    _trigger = {
        'FREE_RUN': 'FRON ON',  # free running
        'TRIGGED': 'TRIG ON'  # selects triggered mode
    }
    _channel_coupling = {
        'AC': 'COUPL AC',
        'DC': 'COUPL DC',
    }

    def __init__(self, interface: AR488, address: int,  name='Fluke_PM6666'):
        self.address = address
        self.name = name
        self.interface = interface
        # configure the instrument to EOT char CR+LF for compatibility reason
        self._write('SPR 255')
        self.current_function = self._query('FNC?')

    def _write(self, message: str):
        """internal function to send a message on the GPIB bus.
        Since the interface must be on the same address of the instrument, every time a write function in called the address is checked by the AR488 and if different changed to the correct one"""
        self.interface.address(self.address)
        self.interface.bus_write(message)

    def _read(self):
        """internal function to read a message on the GPIB bus.
        Since the interface must be on the same address of the instrument, every time a write function in called the address is checked by the AR488 and if different changed to the correct one"""
        self.interface.address(self.address)
        return self.interface.bus_read()

    def _query(self, message, response_payload=False, decode=True):
        """internal function to ask data from the instrument.
        Since the interface must be on the same address of the instrument, every time a write function in called the address is checked by the AR488 and if different changed to the correct one"""
        self.interface.address(self.address)
        return self.interface.query(message, response_payload, decode)

    # commands
    def set_function(self, function):
        """set measurement function, functions available :\n
        'FREQ_A'      -> channel A frequency,\n
        'FREQ_B'      -> channel B frequency,\n
        'FREQ_C'      -> channel C frequency ( if present ),\n
        'PERIOD A'    -> channel A period,\n
        'DT_AB'       -> time interval between A trig abd B trig,\n
        'DT_BA'       -> time interval between B trig abd A trig,\n
        'TOT_A_GATE_B'-> total A pulses gated by B,\n
        'TOT_B_GATE_A'-> total B pulses gated by A,\n
        'TOT_A_SS_B'  -> total A pulses started and stopped by B,\n
        'TOT_B_SS_A'  -> total B pulses started and stopped by A,\n
        'TOT_A_BUS'   -> total A pulses gated bus gate open/close,\n
        'TOT_B_BUS'   -> total B pulses gated bus gate open/close,\n
        'RATIO_AB'    -> number of A pulses  / number of B pulses,\n
        'RATIO_BA'    -> number of B pulses  / number of A pulses,\n
        'RATIO_CA'    -> number of C pulses  / number of A pulses,\n
        'RATIO_CB'    -> number of C pulses  / number of B pulses,\n
        'VMAX_A'      -> positive peak voltage on input A,\n
        'VMIN_A'      -> negative peak voltage on input A,\n
        'VMAX_B'      -> positive peak voltage on input B,\n
        'VMIN_B'      -> negative peak voltage on input B"""
        if function in self._functions.keys():
            self._write(self._functions[function])
            self.current_function = self._functions[function]
        else:
            raise Exception(f'invalid function {function}')

    def get_measure(self):
        """get measurement from counter"""
        # TIME   0004.32426E-3

        response = self._read()
        print(response)
        val = _get_value_by_response(response)
        print(f'first try -> {val}')
        if val is None:
            # retry
            response = self._read()
            print(response)
            val = _get_value_by_response(response)
            print(f'second try -> {val}')
            if val is None:
                raise Exception(
                    'no reponse from device when reading measurement')
        return val

    def set_channel_coupling(self, channel, coupling='AC'):
        """set channel coupling, available counplings: 'AC' , 'DC'"""
        if channel not in self._inputs.keys():
            raise Exception(f'invalid channel {channel}')
        if coupling not in self._channel_coupling.keys():
            raise Exception(f'invalid channel coupling {coupling}')
        self._write(self._inputs[channel])
        self._write(self._channel_coupling[coupling])

    def set_trigger(self, mode:str, slope='+', level='AUTO'):
        """set trigger settings :
        mode :'FREE_RUN' or 'TRIGGED'
        slope : '+' or '-', 
        level : triger voltage level"""
        if mode not in self._trigger.keys():
            raise Exception(f'invalid trigger {mode}')
        if slope not in self._trigger_slope.keys():
            raise Exception(f'invalid slope {slope}')
        if type(level) == str and level == 'AUTO':
            self._write('AUTO ON')
        elif type(level) == float or type(level) == int:
            level = float(level)
            if not -5.1 < level < 5.1:
                raise Exception(f'invalid trigger level {level}')
        else:
            raise Exception('invalid trigger level')
        self._write(self._trigger[mode])
        self._write(self._trigger_slope[slope])
        self._write(f'TRGLVL {level}')

    def set_measurement_time(self, time):
        """set measurement time, 0.01 -> 10s or 0 = single shot """
        time = float(time)
        if 0.01 <= time <= 10 or time == 0:
            self._write(f'MTIME {time}')
        else:
            raise Exception(f'invalid time "{time}"')

    def gate_open(self):
        """open gate for measurement"""
        self._write('GATE OPEN')

    def gate_close(self):
        """close gate for measurement"""
        self._write('GATE CLOSE')
