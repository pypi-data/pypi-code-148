import matlab.engine


class bridge:

    """
    A Python to MATLAB bridge for zapit

    Zapit runs in MATLAB, and this class is a bridge to bring key API commands into Python.
    The user sets up the sample in MATLAB, and then uses this class to run the experiment
    in python.


    Attributes:
    eng (matlab.engine): refence to the MATLAB session in which Zapit is running
    hZP : refernce to Zapit API (model) matlab object
    hZPview : refernce to Zapit GUI controller matlab object

    """

    _CONNECTION_OPEN = False  # Set to true if we managed to connect to MATLAB

    def __init__(self):
        """
        Connect to the MATLAB engine
        """

        names = matlab.engine.find_matlab()
        if "zapit" in names:
            print("Attempting MATLAB connection...")
            self.eng = matlab.engine.connect_matlab("zapit")
            self._CONNECTION_OPEN = True
            print("Connected!")

        else:
            print('FAILED TO FIND MATLAB SESSION "zapit"')
            return

        try:
            self.hZP = self.eng.workspace["hZP"]
            self.hZPview = self.eng.workspace["hZPview"]
        except matlab.engine.MatlabExecutionError:
            self.release_matlab()
            msg = """
            Can not find variables hZP and hZPview in the MATLAB session.
            Suggested Solution:
                a. Start (or restart) Zapit
                b. You should see the message "Opened Python Bridge".
                   If not set general.openPythonBridgeOnStart to 1 in the settings file.
                   Then restart Zapit again.
                b. Re-instantiate this class.
            """
            print(msg)

    def __del__(self):
        """Destructor"""
        self.release_matlab()

    def release_matlab(self):
        """Disconnect from matlab engine"""
        try:
            self.eng.workspace["hZP"]  # Fails if we have already quit
            self.eng.quit()
            print("Disconnected from MATLAB")
        except matlab.engine.MatlabExecutionError:
            pass

    def send_samples(
        self,
        conditionNum=-1,
        laserOn=True,
        hardwareTriggered=True,
        logging=True,
        verbose=False,
    ):
        """Send samples to the DAQ"""
        # fmt: off
        condition_num, laser_on = self.eng.sendSamples(self.hZP,
                                                       "conditionNum", -1,
                                                       "laserOn", True,
                                                       "hardwareTriggered", True,
                                                       "logging", True,
                                                       "verbose", False,
                                                       nargout=2)
        # fmt: on

    def stop_opto_stim(self):
        """Stops the optostim"""
        self.eng.stopOptoStim(self.hZP, nargout=0)

    def is_stimConfig_loaded(self):
        """Return true if zapit has a loaded stim config"""
        return self.eng.eval("~isempty(hZP.stimConfig)", nargout=1)

    def num_stim_cond(self):
        """Return the number of stimulus conditions"""
        if self.is_stimConfig_loaded():
            n = self.eng.eval("hZP.stimConfig.numConditions", nargout=1)
        else:
            n = 0

        return n

    def get_experiment_path(self):
        """Get the experiment directory"""
        exp_dir = self.eng.eval("hZP.experimentPath", nargout=1)
        return exp_dir

    def set_experiment_path(self, exp_dir):
        """Set the experiment directory"""
        self.eng.eval("hZP.experimentPath='%s';" % exp_dir, nargout=0)

    def clear_experiment_path(self):
        """Clear the experiment path"""
        self.eng.eval("hZP.clearExperimentPath", nargout=0)
