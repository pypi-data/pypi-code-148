from typing import Callable

import numpy as np
from pyPhases.util.Logger import classLogger
from pyPhasesRecordloader import ChannelsNotPresent, ParseError, RecordSignal, Signal


@classLogger
class Preprocessing:
    stepDefinition: dict = {}
    instance: "Preprocessing" = None

    def addPreprocessingStep(
        self, stepName: str, stepCallable: Callable[[Signal, RecordSignal, dict], None]
    ):
        """Add a new preprocessing step to the preprocessing pipeline

        Args:
            stepName (str): name of the step to be used in the config
            stepCallable (Callable): Callable with the signature (signal: Signal, recordSignal: RecordSignal, channelConfig: dict)
        """
        Preprocessing.stepDefinition[stepName] = stepCallable

    @classmethod
    def setup(cls, config):
        instance = Preprocessing()

        preprocessingConfig = config["preprocessing"]

        instance.targetChannels = preprocessingConfig["targetChannels"]
        instance.stepsByType = preprocessingConfig["signals"]
        instance.forceGapBetweenEvents = preprocessingConfig["forceGapBetweenEvents"]

        cls.instance = instance

    @classmethod
    def get(cls) -> "Preprocessing":
        return cls.instance

    # def __init__(
    # self,
    # config,
    # ) -> None:
    #     self.downloader: Downloader = downloader
    #     self.copyRawDataToLocal = copyRawDataToLocal

    #     self.targetChannels = targetChannels
    #     self.featureChannels = featureChannels
    #     self.labelChannels = labelChannels

    #     self.combineChannels = combineChannels
    #     self.sourceChannels = sourceChannels
    #     self.optionalSignals = optionalSignals

    #     # if the extractor is not supposed to copy the remote record and the downloader is able to read the record
    #     # directly, overwrite the local file path with the remote path
    #     self.filePath = filePathLocal if copyRawDataToLocal or not downloader.canReadRemote else downloader.basePath
    #     self.ignoreClassIndex = ignoreClassIndex
    #     self.recordLoader = recordLoader

    #     self.preprocessingConfig = preprocessingConfig
    #     self.targetFrequency = preprocessingConfig["targetFrequency"]
    #     self.cutSlices = []
    #     self.dontCutSignal = dontCutSignal

    # @classmethod
    # def addPreprocessingStep(cls, name, method):
    #     cls.stepDefinition[name] = method

    # def prepareLabelSignals(self, psgSignal: PSGSignal, eventSignal: dict):
    #     appendingFeatureChannels = []
    #     for fc in self.labelChannels:
    #         labelName = fc["name"]
    #         labelSignalArray = self.prepareLabelSignal(fc, psgSignal, eventSignal)

    #         if "ignoreWake" in fc and fc["ignoreWake"]:
    #             sleepSignal = np.array(eventSignal["sleepStage"])
    #             labelSignalArray[sleepSignal == PSGEventManager.INDEX_WAKE] = self.ignoreClassIndex

    #         signalName = fc["rename"] if "rename" in fc else labelName
    #         featureSignal = Signal(signalName, labelSignalArray, frequency=psgSignal.targetFrequency)
    #         appendingFeatureChannels.append(featureSignal)

    #     return appendingFeatureChannels

    # def prepareLabelSignal(self, fc, psgSignal, eventSignal):
    #     labelName = fc["name"]
    #     labelSignalArray = None
    #     channelCount, signalLength = psgSignal.getShape()

    #     if labelName == "SleepStagesAASM":
    #         stageSignal = np.array(eventSignal["sleepStage"])

    #         # target classification: W, N1, N2, N3, R
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_WAKE] = 0
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_NREM1] = 1
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_NREM2] = 2
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_NREM3] = 3
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_REM] = 4
    #     elif labelName == "Sleeping":
    #         stageSignal = np.array(eventSignal["sleepStage"])

    #         # target classification: Wake, Sleep
    #         labelSignalArray = np.full(len(stageSignal), 0).astype(np.int16)
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_WAKE] = 0
    #         labelSignalArray[stageSignal >= PSGEventManager.INDEX_NREM1] = 1
    #     elif labelName == "SleepStagesWNR":
    #         stageSignal = np.array(eventSignal["sleepStage"])

    #         # target classification: W, N, R
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_WAKE] = 0
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_NREM1] = 1
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_NREM2] = 1
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_NREM3] = 1
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_REM] = 2
    #     elif labelName == "SleepStagesWLDR":
    #         stageSignal = np.array(eventSignal["sleepStage"])

    #         # target classification: W, L, D, R
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_WAKE] = 0
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_NREM1] = 1
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_NREM2] = 1
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_NREM3] = 2
    #         labelSignalArray[stageSignal == PSGEventManager.INDEX_REM] = 3
    #     elif labelName == "SleepApnea":
    #         # [None, obstructive, mixed, central, hypopnea]
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         if "apnea" in eventSignal:
    #             stageSignal = np.array(eventSignal["apnea"])
    #             labelSignalArray[stageSignal == 0] = 0
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_OBSTRUCTIVE] = 1
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_MIXED] = 2
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_CENTRAL] = 3
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_HYPO] = 4

    #         # ignore none sleep labels
    #         # labelSignalArray[sleepSignal == PSGEventManager.INDEX_WAKE] = self.ignoreClassIndex - 1
    #         if any(labelSignalArray == self.ignoreClassIndex):
    #             self.logWarning("there are overlapping apneas in %s" % psgSignal.recordId)
    #         # labelSignalArray[labelSignalArray == (self.ignoreClassIndex - 1)] = self.ignoreClassIndex
    #     elif labelName == "ApneaBin":
    #         # [None, obstructive, mixed, central, hypopnea]
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         if "apnea" in eventSignal:
    #             stageSignal = np.array(eventSignal["apnea"])
    #             labelSignalArray[stageSignal == 0] = 0
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_OBSTRUCTIVE] = 1
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_MIXED] = 1
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_CENTRAL] = 1
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_HYPO] = 1

    #         # ignore none sleep labels
    #         # labelSignalArray[sleepSignal == PSGEventManager.INDEX_WAKE] = self.ignoreClassIndex - 1
    #         if any(labelSignalArray == self.ignoreClassIndex):
    #             self.logWarning("there are overlapping apneas in %s" % psgSignal.recordId)
    #         # labelSignalArray[labelSignalArray == (self.ignoreClassIndex - 1)] = self.ignoreClassIndex
    #     elif labelName == "SleepArousalsRera":
    #         # [None, obstructive, mixed, central, hypopnea]
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         if "arousal" in eventSignal:
    #             stageSignal = np.array(eventSignal["arousal"])
    #             labelSignalArray[stageSignal == 0] = 0
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSAL_RERA] = 1
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSAL] = 2
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSAL_ASDA] = self.ignoreClassIndex
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSAL_CHIN] = self.ignoreClassIndex
    #     elif labelName == "SleepArousals":
    #         # [None, obstructive, mixed, central, hypopnea]
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         if "arousal" in eventSignal:
    #             stageSignal = np.array(eventSignal["arousal"])
    #             labelSignalArray[stageSignal == 0] = 0
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSAL_RERA] = 1
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSAL] = 1
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSAL_ASDA] = 1
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSAL_CHIN] = 1
    #     elif labelName == "SleepArousalsExtended":
    #         # [None, obstructive, mixed, central, hypopnea]
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         if "arousal" in eventSignal:
    #             stageSignal = np.array(eventSignal["arousal"])
    #             labelSignalArray[stageSignal == 0] = 0
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSALEXT_AROUSAL] = 1
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSALEXT_LIMB] = 2
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSALEXT_RERA] = 3
    #     elif labelName == "ApneaLMArousal":
    #         # [None, obstructive, mixed, central, hypopnea]
    #         labelSignalArray = np.full(signalLength, 0).astype(np.int16)

    #         if "limb" in eventSignal:
    #             stageSignal = np.array(eventSignal["limb"])
    #             labelSignalArray[stageSignal & PSGEventManager.INDEX_LEGMOVEMENT_LEFT > 0] = 8
    #             labelSignalArray[stageSignal & PSGEventManager.INDEX_LEGMOVEMENT_RIGHT > 0] = 8
    #             labelSignalArray[stageSignal & PSGEventManager.INDEX_LEGMOVEMENT > 0] = 8

    #         if "apnea" in eventSignal:
    #             stageSignal = np.array(eventSignal["apnea"])
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_OBSTRUCTIVE] = 4
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_MIXED] = 5
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_CENTRAL] = 6
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_APNEA_HYPO] = 7

    #         if "arousal_ext" in eventSignal:
    #             stageSignal = np.array(eventSignal["arousal_ext"])
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSALEXT_AROUSAL] = 1
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSALEXT_LIMB] = 2
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_AROUSALEXT_RERA] = 3

    #     elif labelName == "LegMovementsLeftRightAASM":
    #         # [None, legMovement, PLM]
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         if "limb" in eventSignal:
    #             stageSignal = np.array(eventSignal["limb"])
    #             labelSignalArray = stageSignal  # is not distinct
    #     elif labelName == "LegMovementsAASM":
    #         # [None, legMovement, PLM]
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         if "limb" in eventSignal:
    #             stageSignal = np.array(eventSignal["limb"])
    #             labelSignalArray[stageSignal == 0] = 0
    #             labelSignalArray[stageSignal & PSGEventManager.INDEX_LEGMOVEMENT_LEFT > 0] = 1
    #             labelSignalArray[stageSignal & PSGEventManager.INDEX_LEGMOVEMENT_RIGHT > 0] = 1
    #             labelSignalArray[stageSignal & PSGEventManager.INDEX_LEGMOVEMENT > 0] = 1
    #     elif labelName == "LegMovementsRight":
    #         # [None, legMovement, PLM]
    #         labelSignalArray = np.full(signalLength, self.ignoreClassIndex).astype(np.int16)

    #         if "limb" in eventSignal:
    #             stageSignal = np.array(eventSignal["limb"])
    #             labelSignalArray[stageSignal == PSGEventManager.INDEX_LEGMOVEMENT_RIGHT] = 1
    #     elif labelName == "ChannelFail":
    #         stageSignal = np.array(eventSignal["fail"])
    #         targetSignal = psgSignal.getSignalByName(fc["channel"])
    #         sourceChannelIndex = targetSignal.sourceIndex

    #         labelSignalArray = np.full(signalLength, 0).astype(np.int16)
    #         bitMaskInt = 2**sourceChannelIndex + 1
    #         # labelSignalArray[(stageSignal) > 0] = 1
    #         labelSignalArray[(stageSignal & bitMaskInt) > 0] = 1
    #     elif labelName == "copy":
    #         sourceSignal = psgSignal.getFirstSignalByName(fc["channel"])
    #         stepsByType = self.preprocessingConfig["signals"]
    #         sourceSignal.type = fc["type"] if "type" in fc else None

    #         if sourceSignal.type in stepsByType:
    #             stepNames = stepsByType[sourceSignal.type]
    #             for processStep in stepNames:
    #                 self.parseSignalSteps(sourceSignal, processStep, psgSignal, fc)

    #         labelSignalArray = sourceSignal.signal
    #     else:
    #         raise Exception("Label channel with the name %s is not yet supported" % labelName)

    #     return labelSignalArray

    # @staticmethod
    # def prepareEventsFor(df, labelName):
    #     em = PSGEventManager()
    #     if labelName == "LegMovementsAASM" or labelName == "ApneaLMArousal":
    #         Extractor.prepareEventsFor(df, "SleepApnea")
    #         Extractor.prepareEventsFor(df, "SleepArousalsExtended" if labelName == "ApneaLMArousal" else "SleepArousals")
    #         em.dfAppendGroups(
    #             df,
    #             "limb",
    #             "sleepStage",
    #             newGroupName="sleepStage-15",
    #             offsetStart=-15.1,
    #             fixedDuration=15.2,
    #         )
    #         em.dfAppendGroups(
    #             df,
    #             "limb",
    #             "apnea",
    #             newGroupName="apnea",
    #             offsetStart=-0.5,
    #             offsetEnd=0.5,
    #         )
    #         em.dfAppendGroups(
    #             df,
    #             "limb",
    #             "arousal",
    #             newGroupName="arousal",
    #             offsetStart=-0.5,
    #             offsetEnd=0.5,
    #         )

    #         removeQuery = (
    #             "(group == 'limb' and (`sleepStage-15` == 'W' or apnea != '' or arousal.str.contains('arousal_rera')))"
    #         )
    #         rem = df.query(removeQuery, engine="python")
    #         df.drop(rem.index, inplace=True)

    #     elif labelName in ["SleepArousalsExtended", "SleepArousals"]:
    #         em.dfAppendGroups(
    #             df,
    #             "arousal",
    #             "sleepStage",
    #             newGroupName="sleepStage-15",
    #             offsetStart=-15.1,
    #             fixedDuration=15.1,
    #         )

    #         em.dfAppendGroups(df, "arousal", "apnea")
    #         removeQuery = "(name == 'arousal' and `sleepStage-15` == 'W')"
    #         rem = df.query(removeQuery)
    #         df.drop(rem.index, inplace=True)

    #         if labelName == "SleepArousalsExtended":
    #             em.dfAppendGroups(
    #                 df,
    #                 "arousal",
    #                 "limb",
    #                 newGroupName="limb-arousal",
    #                 offsetStart=-0.6,
    #                 offsetEnd=0.6,
    #             )
    #             em.dfAppendGroups(
    #                 df,
    #                 "arousal",
    #                 "sleepStage",
    #                 newGroupName="woke-arousal",
    #                 offsetStart=-0.5,
    #                 offsetEnd=15.1,
    #             )
    #             df.loc[df.query("name == 'arousal' and `limb-arousal` != ''").index, "name"] = "arousal_limb"
    #             df.loc[df.query("name == 'arousal'").index, "name"] = "arousal_none"
    #             df.loc[df.query("name == 'arousal_rera'").index, "name"] = "arousal_rera_man"

    #     elif labelName == "SleepApnea":
    #         Extractor.prepareEventsFor(df, "SpO2Events")
    #         Extractor.prepareEventsFor(df, "SleepArousals")

    #         em.dfAppendGroups(
    #             df,
    #             "apnea",
    #             "sleepStage",
    #             newGroupName="sleepStageStart15",
    #             offsetStart=-15.1,
    #             fixedDuration=15.1,
    #         )

    #         arousalOffset = 5
    #         em.dfAppendGroups(
    #             df,
    #             "apnea",
    #             "arousal",
    #             newGroupName="arousal",
    #             offsetStart=0,
    #             offsetEnd=arousalOffset,
    #         )

    #         desatOffset = 10
    #         em.dfAppendGroups(
    #             df,
    #             "apnea",
    #             "spo2",
    #             newGroupName="desaturation",
    #             offsetStart=0,
    #             offsetEnd=desatOffset,
    #         )

    #         removeQuery = "(group == 'apnea' and manual == False  and (duration < 10 or sleepStageStart15 == 'W' or (name == 'resp_hypopnea' and arousal != 'arousal' and desaturation == '')))"
    #         rem = df.query(removeQuery)
    #         df.drop(rem.index, inplace=True)
    #     elif labelName == "SpO2Events":

    #         em.dfAppendGroups(
    #             df,
    #             "spo2",
    #             "sleepStage",
    #             newGroupName="sleepStage-15",
    #             offsetStart=-15.1,
    #             fixedDuration=15.2,
    #         )

    #         df["o2diff"] = df.apply(
    #             lambda row: (
    #                 (float(row["data"]["O2Before"]) - float(row["data"]["O2Min"]))
    #                 if "O2Min" in row["data"] and "O2Before" in row["data"]
    #                 else None
    #             ),
    #             axis=1,
    #         )
    #         removeQuery = "(group == 'spo2' and manual == False and (o2diff < 3 or (`sleepStage-15` == 'W')))"
    #         rem = df.query(removeQuery, engine="python")

    #         df.drop(rem.index, inplace=True)
    #     else:
    #         Logger.log("Labelname %s has no event preprocessing" % labelName, "Extractor", LogLevel.ERROR)

    # def prepareEvents(self, events):
    #     em = PSGEventManager()
    #     df = em.getDataframeFromEvents(events)
    #     for fc in self.labelChannels:
    #         labelName = fc["name"]
    #         if self.preprocessingConfig["useTSMEventPreprocessing"]:
    #             Extractor.prepareEventsFor(df, labelName)

    #         if labelName == "SleepArousals":
    #             if "cutEvents" in self.preprocessingConfig:
    #                 eventPadding = self.preprocessingConfig["cutEvents"]
    #                 arousals = df.query("group == 'arousal'")
    #                 currentCut = [0, None]
    #                 for arousal in arousals.iloc:
    #                     start = arousal.start - eventPadding
    #                     end = arousal.end + eventPadding

    #                     if currentCut[0] <= start:
    #                         currentCut[1] = start
    #                         self.cutSlices.append(currentCut)

    #                     currentCut = [end, None]
    #             if "extendEvents" in self.preprocessingConfig and self.preprocessingConfig["extendEvents"] is not None:
    #                 addBefore, addAfter = self.preprocessingConfig["extendEvents"]
    #                 arousals = df.query("group == 'arousal'")
    #                 df.loc[arousals.index, "start"] -= addBefore
    #                 df.loc[arousals.index, "end"] += addAfter
    #                 df.loc[arousals.index, "duration"] += addAfter + addBefore

    #         pass

    #     return df

    # def prepareFeatureSignals(self, psgSignal: PSGSignal, eventSignal, record):

    #     appendingFeatureChannels = []
    #     for fc in self.featureChannels:
    #         featureName = fc["name"]
    #         featureSignalArray = None
    #         channelCount, signalLength = psgSignal.getShape()

    #         if featureName == "YasaSpindleDetect":
    #             import yasa

    #             channels = fc["channels"]
    #             featureSignalArray = np.full(signalLength, 0).astype(np.int16)

    #             for channelNames in channels:
    #                 signal = psgSignal.getFirstSignalByName(channelNames)
    #                 sp = yasa.spindles_detect(signal.signal, signal.frequency)
    #                 mask = sp.get_mask()

    #                 maskSignal = Signal(name="mask spindle", signal=mask, frequency=signal.frequency)
    #                 maskSignal.resample(psgSignal.targetFrequency, simple=True, antialiaseFIR=False)

    #                 featureSignalArray += maskSignal.signal
    #         elif featureName[0:12] == "swaEpochwise":
    #             from scipy.ndimage.filters import uniform_filter1d

    #             channels = fc["channels"]
    #             featureSignalArray = np.full(signalLength, np.nan).astype(np.float64)

    #             for channelNames in channels:
    #                 signal = psgSignal.getFirstSignalByName(channelNames)
    #                 power_5s = signal.windowedBandpower(lower=1, upper=4.5, windowsize=5 * signal.frequency)
    #                 power_epoch_mean = uniform_filter1d(power_5s, size=6, mode="mirror")[3::6]
    #                 # filter according to felix implementation
    #                 filterFactor = 3
    #                 factor = np.insert(
    #                     (filterFactor * power_epoch_mean[0:-1] < power_epoch_mean[1:]) * (filterFactor - 1) + 1, 0, 1
    #                 )
    #                 power_epoch_mean = power_epoch_mean / factor
    #                 # end filter
    #                 power = np.tile(power_epoch_mean, (30 * psgSignal.targetFrequency, 1))
    #                 power = np.reshape(power, (30 * psgSignal.targetFrequency * power_epoch_mean.size,), order="F")

    #                 powerSignal = Signal(name="swa_epochwise", signal=power, frequency=psgSignal.targetFrequency)

    #                 featureSignalArray[0 : min(powerSignal.signal.size, signalLength)] = powerSignal.signal[
    #                     : min(powerSignal.signal.size, signalLength)
    #                 ]

    #         elif featureName == "Tachogram":

    #             channels = fc["channels"]
    #             featureSignalArray = np.full(psgSignal.shape[1], np.nan).astype(np.float64)
    #             for channelNames in channels:
    #                 signal = psgSignal.getFirstSignalByName(channelNames)
    #                 timeseries = TimeseriesSignal(signal)
    #                 timeseries.recordId = psgSignal.recordId
    #                 timeseries.rri()
    #                 featureSignalArray = timeseries.resampleAtFrequency(featureSignalArray.shape[0], psgSignal.targetFrequency)
    #         elif (featureName == "breathTachogram") | (featureName == "breathTachogram2"):
    #             channels = fc["channels"]
    #             featureSignalArray = np.full(psgSignal.shape[1], np.nan).astype(np.float64)
    #             for channelNames in channels:
    #                 signal = psgSignal.getFirstSignalByName(channelNames)
    #                 timeseries = TimeseriesSignal(signal)
    #                 timeseries.recordId = psgSignal.recordId
    #                 timeseries.bbi()
    #                 featureSignalArray = timeseries.resampleAtFrequency(featureSignalArray.shape[0], psgSignal.targetFrequency)

    #         elif featureName == "EpochIndex":
    #             windowSize = fc["windowSize"]
    #             normalizeFactor = fc["factor"]
    #             factor = windowSize * psgSignal.targetFrequency
    #             windowCount = math.ceil(signalLength / factor)
    #             arangeArray = np.arange(0, windowCount).astype(np.int16)
    #             featureSignalArray = (np.repeat(arangeArray, factor) / normalizeFactor)[:signalLength]
    #         elif featureName == "EpochCyclic":
    #             featureSignalArray = np.full(signalLength, 0).astype(np.int16)
    #             windowSize = fc["windowSize"]
    #             cycleLength = fc["length"]
    #             factor = windowSize * psgSignal.targetFrequency
    #             windowCount = math.ceil(signalLength / factor)
    #             arangeArray = np.arange(0, windowCount).astype(np.int16)
    #             featureSignalArray = [np.cos(np.pi * arangeArray / cycleLength)]
    #             featureSignalArray = np.repeat(featureSignalArray, factor)[:signalLength]
    #         elif featureName == "LabelChannel":
    #             featureSignalArray = self.prepareLabelSignal(fc["labelConfig"], psgSignal, eventSignal)
    #         else:
    #             raise Exception("Feature channel with the name %s is not yet supported" % featureName)

    #         signalName = fc["rename"] if "rename" in fc else featureName
    #         featureSignal = Signal(signalName, featureSignalArray, frequency=psgSignal.targetFrequency)
    #         appendingFeatureChannels.append(featureSignal)

    #     return appendingFeatureChannels

    # def cut(self, signal: PSGSignal, startOffset, endOffset=None):
    #     slices = np.array(self.cutSlices, dtype=np.int32)
    #     slices -= int(startOffset)
    #     smoothCuts = self.preprocessingConfig["smoothCuts"] if "smoothCuts" in self.preprocessingConfig else 0

    #     for i, s in enumerate(slices):
    #         checkEnd = endOffset is None or s[0] < endOffset
    #         if s[1] > 0 and checkEnd:
    #             s[0] = max(s[0], 0)
    #             sliceLength = s[1] - s[0]
    #             if smoothCuts > 1:
    #                 signalLength = signal.signals[0].signal.shape[0]
    #                 diff = signalLength + sliceLength
    #                 s[0] += diff % smoothCuts

    #             signal.signalCut(s[0], s[1])
    #             sliceLength = s[1] - s[0]
    #             slices[(i + 1) :, :] -= sliceLength

    # def offset(self, signal: PSGSignal, startAt=0, stopAt=None):
    #     signal.signalOffset(startAt, stopAt)

    # def getSignalQualityFromDB(self, recordId, channelName):
    #     db = RecordDB.getNew()
    #     quality = db.getSignalQuality(recordId, channelName)
    #     db.close()
    #     return quality

    def parseSignalSteps(
        self, signal: Signal, stepName, psgSignal: RecordSignal, channelConfig={}
    ):
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
                raise Exception(
                    "alice position only supports 0, 3, 6, 9, 12 as values ... fix here :-)"
                )

            signal.signal[signal.signal == 0] = 1
            signal.signal[signal.signal == 3] = 5
            signal.signal[signal.signal == 6] = 2
            signal.signal[signal.signal == 9] = 4
            signal.signal[signal.signal == 12] = 3
        elif stepName == "positionDomino":
            uniquePositions = set(np.unique(signal.signal))
            checkValues = set(uniquePositions) - set([1, 2, 3, 4, 5, 6])
            if len(checkValues) > 0:
                raise Exception(
                    "domino position only supports 1, 2, 3, 4, 5, 6 as values ... fix here :-)"
                )

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
                raise Exception(
                    "domino position only supports 0, 1, 2, 3 as values ... fix here :-)"
                )

            signal.signal += 10  # overwrite protection
            signal.signal[signal.signal == 10] = 5
            signal.signal[signal.signal == 11] = 3
            signal.signal[signal.signal == 12] = 2
            signal.signal[signal.signal == 13] = 4
        elif stepName == "positionMESA":
            uniquePositions = set(np.unique(signal.signal))
            # Right, Back, Left, Front, Upright (derived from the profusion xml, not sure if the mapping is actually correct)
            checkValues = set(uniquePositions) - set([0, 1, 2, 3, 4])
            if len(checkValues) > 0:
                raise Exception(
                    "domino position only supports 0, 1, 2, 3, 4 as values ... fix here :-)"
                )

            signal.signal += 10  # overwrite protection
            signal.signal[signal.signal == 10] = 5
            signal.signal[signal.signal == 11] = 2
            signal.signal[signal.signal == 12] = 3
            signal.signal[signal.signal == 13] = 4
            signal.signal[signal.signal == 14] = 1
        elif stepName == "rr2hr":
            timeseries = TimeseriesSignal(signal)
            timeseries.rr2hr()
            signal.signal = timeseries.resampleAtFrequency(
                signal.signal.shape[0], signal.frequency
            )
        elif stepName in Preprocessing.stepDefinition:
            Preprocessing.stepDefinition[stepName](signal, psgSignal, channelConfig)
        else:
            raise Exception(
                "The Preprocessing step '%s' is not yet supported" % stepName
            )

    def preprocessingSignal(self, psgSignal: RecordSignal):
        self.preprocessingSignal(psgSignal, self.stepsByType)

    def preprocessSignalByType(
        self, psgSignal: RecordSignal, stepsByType, targetFrequency
    ):
        psgSignal.targetFrequency = targetFrequency
        for signal in psgSignal.signals:
            cName = signal.name
            if cName in psgSignal.signalNames:
                signal = psgSignal.getSignalByName(cName)
                type = signal.typeStr

                if type in stepsByType:
                    stepNames = stepsByType[type]

                    for processStep in stepNames:
                        self.parseSignalSteps(signal, processStep, psgSignal, signal)
                elif type is not None:
                    self.logError(
                        "Signaltype %s for signal %s has no preprocessing steps (defined in preprocessing.signals.[type])"
                        % (signal.type, signal.name)
                    )
            else:
                if cName not in self.optionalSignals and not signal["generated"]:
                    self.logError(
                        "Missing channel %s for %s" % (cName, signal.recordId)
                    )
                    raise ChannelsNotPresent(cName, signal.recordId)

    # def extractRecordAndAnnotations(self, recordName):
    #     return self.extractRecord(recordName, True)

    # def extractRecord(self, recordName, extractAnnotations=False, returnRawSignal=False):
    #     rl = self.recordLoader
    #     rl.filePath = self.filePath

    #     exist = rl.exist(recordName)
    #     if extractAnnotations:
    #         exist = exist and rl.existAnnotation(recordName)

    #     if not exist:
    #         if self.copyRawDataToLocal:
    #             self.downloader.copySingleRecord(recordName, self.filePath)
    #         else:
    #             raise Exception("Coudn't load record '%s'" % (recordName))

    #     try:
    #         rl.sourceChannels = self.sourceChannels
    #         psgSignal = rl.getSignal(recordName)
    #     except ParseError:
    #         self.logError("Recordname %s couldn't be parsed, try to copy sourcefile again" % (recordName))
    #         self.downloader.copySingleRecord(recordName, self.filePath, force=True)
    #         psgSignal = rl.getSignal(recordName)

    #     firstSleep = None
    #     lastSleep = None

    #     forceGapBetweenEvents = self.preprocessingConfig["forceGapBetweenEvents"]
    #     if extractAnnotations:
    #         shape = psgSignal.getShape()
    #         if rl.exportsEventArray:
    #             events = rl.getEventList(recordName)
    #             events = self.prepareEvents(events)

    #             sleepEvents = events.query('group == "sleepStage" and name != "W"')

    #             if len(sleepEvents) > 0:
    #                 firstSleep = sleepEvents.iloc[0].start
    #                 lastSleep = sleepEvents.iloc[-1].end

    #             annotationEventArray = PSGEventManager().getEventSignalFromDF(
    #                 events,
    #                 shape[1],
    #                 self.targetFrequency,
    #                 forceGapBetweenEvents=forceGapBetweenEvents,
    #             )
    #         else:
    #             # default returns an signal array
    #             annotationEventArray = rl.getEventArray(
    #                 recordName,
    #                 shape[1],
    #                 self.targetFrequency,
    #             )

    #         labelSignals = self.prepareLabelSignals(psgSignal, annotationEventArray)
    #         psgSignal.addLabelSignals(labelSignals)

    #     self.combine(psgSignal)

    #     featureSignals = self.prepareFeatureSignals(psgSignal, annotationEventArray, recordName)
    #     psgSignal.addSignals(featureSignals)

    #     if self.dontCutSignal:
    #         offsetStart, offsetEnd = [0, None]
    #     elif self.preprocessingConfig["cutFirstAndLastWake"] and firstSleep > 0:
    #         offsetStart, offsetEnd = [firstSleep, lastSleep]
    #     else:
    #         offsetStart, offsetEnd = [rl.lightOff, rl.lightOn]

    #     self.offset(psgSignal, startAt=offsetStart, stopAt=offsetEnd)

    #     if returnRawSignal:
    #         return psgSignal

    #     self.signalProcessing(psgSignal)

    #     self.cut(psgSignal, offsetStart, offsetEnd)

    #     annotationArray = None
    #     if len(self.labelChannels) > 0:
    #         annotationArray = psgSignal.getAnnotationArray() if extractAnnotations else None

    #     signalArray = psgSignal.getSignalArray(self.targetChannels)

    #     return signalArray, annotationArray

    # @staticmethod
    # def fixedRecordLength(dataArray, sampleDataLimit, position="left", fillValue=0):

    #     if position not in ["center", "left"]:
    #         raise Exception("Position %s is not yet supported" % position)

    #     if dataArray.shape[0] < sampleDataLimit:
    #         # Value Pad
    #         neededLength = sampleDataLimit
    #         dataLength = dataArray.shape[0]
    #         fullData = np.full((neededLength, dataArray.shape[1]), fillValue, dtype=dataArray.dtype)
    #         startAt = 0
    #         if position == "center":
    #             center = math.floor(neededLength / 2)
    #             startAt = center - math.floor(dataLength / 2)
    #         endAt = startAt + dataLength

    #         fullData[startAt:endAt, ::] = dataArray
    #         dataArray = fullData

    #     elif dataArray.shape[0] > sampleDataLimit:
    #         # Chop
    #         dataArray = dataArray[0:sampleDataLimit, ::]

    #     return dataArray

    # def proceessSingleRecord(self, recordId, useRaw=False):
    #     rl = self.recordLoader
    #     rl.filePath = self.filePath
    #     hasAnnotation = rl.existAnnotation(recordId)

    #     return self.extractRecord(recordId, extractAnnotations=hasAnnotation, returnRawSignal=useRaw), hasAnnotation
