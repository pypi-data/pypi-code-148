
from pyPhases.util.Logger import classLogger

from pyPhasesRecordLoader import RecordSignal, Signal


class ParseError(Exception):
    pass


class AnnotationException(Exception):
    path = []
    name = ""

    def __init__(self, path):
        self.path = path
        self.name = path[-1]
        super().__init__(self.getMessage())


class AnnotationNotFound(AnnotationException):
    def getMessage(self):
        return "Annotation was not found in the XML file: %s" % (self.path + [self.name])


class AnnotationInvalid(AnnotationException):
    def getMessage(self):
        return "Annotation is invalid: %s" % (self.path)


class ChannelsNotPresent(Exception):
    channels = []

    def __init__(self, channels, recordid="Unknown"):
        msg = "Channels of record %s where not present: %s" % (recordid, channels)
        super().__init__(msg)
        self.channels = channels


@classLogger
class Preprocessing:

    def __init__(self, config) -> None:
        self.config = config
        
    def preprocessRecordSignal(self, psgSignal: RecordSignal, type=None):
        
        self.signalProcessing(psgSignal)
        
    def signalProcessing(self, psgSignal: RecordSignal):

        stepsByType = self.preprocessingConfig["signals"]

        for channel in self.sourceChannels:
            cName = channel["name"]
            if cName in psgSignal.signalNames:
                signal = psgSignal.getSignalByName(cName)
                signal.type = channel["type"] if "type" in channel else None

                if signal.type in stepsByType:
                    stepNames = stepsByType[signal.type]

                    for processStep in stepNames:
                        self.parseSignalSteps(signal, processStep, psgSignal, channel)
                elif signal.type is not None:
                    self.logError(
                        "Signaltype %s for signal %s has no preprocessing steps (defined in preprocessing.signals.[type])"
                        % (signal.type, signal.name)
                    )
            else:
                if cName not in self.optionalSignals and not channel["generated"]:
                    self.logError("Missing channel %s for %s" % (cName, signal.recordId))
                    raise ChannelsNotPresent(cName, signal.recordId)

    def parseSignalSteps(self, signal: Signal, stepName, psgSignal: RecordSignal, channelConfig={}):
        signal.processHistory.append(stepName)
        if stepName == "resampleFIR":
            signal.resample(psgSignal.targetFrequency, antialiaseFIR=True)
        elif stepName == "resampleFIRSimple":
            signal.resample(psgSignal.targetFrequency, simple=True, antialiaseFIR=True)
        elif stepName == "resample":
            signal.resample(psgSignal.targetFrequency, antialiaseFIR=False)
        elif stepName == "resampleSimple":
            signal.resample(psgSignal.targetFrequency, simple=True, antialiaseFIR=False)
        elif stepName == "normalizePercentage":
            signal.simpleNormalize(0, 100)
        elif stepName == "normalize":
            signal.simpleNormalize()
        elif stepName == "tanh":
            signal.tanh()
        elif stepName == "sigmoid":
            signal.sigmoid()
        elif stepName == "normalize01":
            signal.simpleNormalize(0, 1, cut=False)
        elif stepName == "normalize1":
            signal.simpleNormalize(-1, 1, cut=False)
        elif stepName == "scale":
            signal.scale()
        elif stepName == "fftConvolutionECG":
            # Normalize by removing the mean and the rms in an 2 second rolling window, using fftconvolve for computational efficiency
            kernel_size = (2 * signal.frequency) + 1
            signal.fftConvolution(kernel_size)
        elif stepName == "fftConvolutionECG6":
            # Normalize by removing the mean and the rms in an 6 second rolling window, using fftconvolve for computational efficiency
            kernel_size = (6 * signal.frequency) + 1
            signal.fftConvolution(kernel_size)
        elif stepName == "fftConvolution":
            # Normalize by removing the mean and the rms in an 18 minute rolling window, using fftconvolve for computational efficiency
            # 18 minute window is used because because baseline breathing is established in 2 minute window according to AASM standards.
            # Normalizing over 18 minutes ensure a 90% overlap between the beginning and end of the baseline window
            kernel_size = (18 * 60 * signal.frequency) + 1
            signal.fftConvolution(kernel_size)
        elif stepName == "notchFilter":
            signal.notchFilter()
        elif stepName == "fixedSize":
            fc = channelConfig["size"]
            signal.fixedSize(fc)
        # normalize Positions to: [None=0, Up=1, Supine=2, Left=3, Prone=4, Right=5]
        elif stepName == "positionAlice":
            uniquePositions = set(np.unique(signal.signal))
            checkValues = set(uniquePositions) - set([0, 3, 6, 9, 12])
            if len(checkValues) > 0:
                raise Exception("alice position only supports 0, 3, 6, 9, 12 as values ... fix here :-)")

            signal.signal[signal.signal == 0] = 1
            signal.signal[signal.signal == 3] = 5
            signal.signal[signal.signal == 6] = 2
            signal.signal[signal.signal == 9] = 4
            signal.signal[signal.signal == 12] = 3
        elif stepName == "positionDomino":
            uniquePositions = set(np.unique(signal.signal))
            checkValues = set(uniquePositions) - set([1, 2, 3, 4, 5, 6])
            if len(checkValues) > 0:
                raise Exception("domino position only supports 1, 2, 3, 4, 5, 6 as values ... fix here :-)")

            signal.signal[signal.signal == 1] = 4
            signal.signal[signal.signal == 2] = 1
            signal.signal[signal.signal == 3] = 3
            signal.signal[signal.signal == 4] = 5
            signal.signal[signal.signal == 5] = 1
            signal.signal[signal.signal == 6] = 2
        # normalize Positions to: [None=0, Up=1, Supine=2, Left=3, Prone=4, Right=5]
        elif stepName == "positionSHHS":
            uniquePositions = set(np.unique(signal.signal))
            # RIGHT, LEFT, BACK, FRONT (derived from the profusion xml, not sure if the mapping is actually correct)
            checkValues = set(uniquePositions) - set([0, 1, 2, 3])
            if len(checkValues) > 0:
                raise Exception("domino position only supports 0, 1, 2, 3 as values ... fix here :-)")

            signal.signal += 10 # overwrite protection
            signal.signal[signal.signal == 10] = 5
            signal.signal[signal.signal == 11] = 3
            signal.signal[signal.signal == 12] = 2
            signal.signal[signal.signal == 13] = 4
        elif stepName == "positionMESA":
            uniquePositions = set(np.unique(signal.signal))
            # Right, Back, Left, Front, Upright (derived from the profusion xml, not sure if the mapping is actually correct)
            checkValues = set(uniquePositions) - set([0, 1, 2, 3, 4])
            if len(checkValues) > 0:
                raise Exception("domino position only supports 0, 1, 2, 3, 4 as values ... fix here :-)")

            signal.signal += 10 # overwrite protection
            signal.signal[signal.signal == 10] = 5
            signal.signal[signal.signal == 11] = 2
            signal.signal[signal.signal == 12] = 3
            signal.signal[signal.signal == 13] = 4
            signal.signal[signal.signal == 14] = 1
        elif stepName == "rr2hr":
            timeseries = TimeseriesSignal(signal)
            timeseries.rr2hr()
            signal.signal = timeseries.resampleAtFrequency(signal.signal.shape[0], signal.frequency)
        else:
            raise Exception("The Preprocessing step '%s' is not yet supported" % stepName)
