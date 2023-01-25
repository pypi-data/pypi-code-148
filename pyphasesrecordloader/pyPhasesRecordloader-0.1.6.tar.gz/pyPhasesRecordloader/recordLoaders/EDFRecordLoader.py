# from datetime import datetime
import pyedflib

from ..RecordSignal import RecordSignal
from ..Signal import Signal
from ..RecordLoader import ChannelsNotPresent, ParseError, RecordLoader
# from teleschlafmedizin.model.recordManager.RecordMeta import Channel, Patient, Record, RecordChannel


class EDFRecordLoader(RecordLoader):
    def __init__(self, filePath, targetSignals, targetSignalTypes, optionalSignals=[], combineChannels=[]) -> None:
        super().__init__(
            filePath=filePath,
            targetSignals=targetSignals,
            targetSignalTypes=targetSignalTypes,
            optionalSignals=optionalSignals,
            combineChannels=combineChannels,
        )
        self.annotations = []
        self.channelMap = {}

    def getSignal(self, recordName):
        edfFile = self.getFilePathSignal(recordName)
        signal = self.loadSignal(edfFile)
        signal.recordId = recordName
        return signal

    def getAnnotationTimeByName(self, name):
        for time, n in zip(self.annotations[0], self.annotations[2]):
            if n == name:
                return time

        return None

    def loadSignal(self, edfFile, annotations=False):
        recordSignal = RecordSignal()

        try:
            self.log("Read EDF %s" % edfFile)
            f = pyedflib.EdfReader(edfFile)
        except Exception as ex:
            raise ParseError("Failed to read EDF File %s: %s" % (edfFile, str(ex)))

        n = f.signals_in_file
        targetSignals = self.targetSignals if annotations == False else self.annotationSignal
        if len(targetSignals) == 0:
            raise Exception(
                "The RecordLoader has no target signals to extract, please specificy 'sourceSignals' with the name of the channels"
            )

        if f.annotations_in_file > 0:
            self.annotations = f.readAnnotations()

        expectedSignals = len(targetSignals)
        addedSignals = []
        ignoredChannels = []

        for i in range(n):
            signalArray = f.readSignal(i, digital=self.useDigitalSignals)
            header = f.getSignalHeader(i)
            channelLabel = header["label"]
            self.channelMap[channelLabel] = i
            if channelLabel in targetSignals:
                signal = Signal(channelLabel, signalArray, frequency=header["sample_rate"])
                signal.typeStr = self.getSignalTypeStrFromDict(signal.name)
                signal.setSignalTypeFromTypeStr()
                signal.isDigital = self.useDigitalSignals
                signal.digitalMin = header["digital_min"]
                signal.digitalMax = header["digital_max"]
                signal.physicalMin = header["physical_min"]
                signal.physicalMax = header["physical_max"]
                signal.dimension = header["dimension"]
                signal.sourceIndex = i
                signal.prefilter = header["prefilter"]
                recordSignal.addSignal(signal, channelLabel)
                addedSignals.append(channelLabel)
            else:
                ignoredChannels.append(channelLabel)

        self.log("Added %i signals, ignored: %s" % (len(addedSignals), ignoredChannels))
        if len(addedSignals) < expectedSignals:
            missingchannels = set(self.targetSignals) - set(addedSignals) - set(self.optionalSignals)
            if len(missingchannels) > 0:
                raise ChannelsNotPresent(missingchannels, edfFile)

        return recordSignal

    # def fillRecordFromEdf(self, record, edfFile):
    #     edf = pyedflib.EdfReader(edfFile)
    #     signalHeaders = edf.getSignalHeaders()

    #     record.dataCount = edf.datarecords_in_file
    #     record.start = edf.getStartdatetime()

    #     for i in range(len(signalHeaders)):
    #         head = signalHeaders[i]
    #         channel = Channel()
    #         recordChannel = RecordChannel()

    #         channel.name = head["label"]
    #         channel.dimension = head["dimension"]
    #         channel.min = head["physical_min"]
    #         channel.max = head["physical_max"]
    #         recordChannel.transducer = head["transducer"]
    #         recordChannel.frequency = head["sample_rate"]
    #         recordChannel.prefilter = head["prefilter"]

    #         signalArray = edf.readSignal(i)
    #         signal = Signal(channel.name, signalArray, frequency=recordChannel.frequency)
    #         signal.dimension = channel.dimension
    #         signal.typeStr = self.getSignalTypeStrFromDict(signal.name)
    #         signal.checkSignalQuality()
    #         recordChannel.quality = signal.quality

    #         recordChannel.Channel = channel
    #         record.recordChannels.append(recordChannel)

    #     patient = Patient()
    #     header = edf.getHeader()
    #     patient.gender = header["gender"]
    #     try:
    #         birthday = datetime.strptime(header["birthdate"], "%d %b %Y")
    #         patient.birthyear = birthday.year
    #     except Exception:
    #         pass

    #     record.Patient = patient

    # def getRecordFromEdf(self, recordName) -> Record:
    #     record = Record()
    #     edfFile = self.getFilePathSignal(recordName)
    #     self.fillRecordFromEdf(record, edfFile)
    #     return record
