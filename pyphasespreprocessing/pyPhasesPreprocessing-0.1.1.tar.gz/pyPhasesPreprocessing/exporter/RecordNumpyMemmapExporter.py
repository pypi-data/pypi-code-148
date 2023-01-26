import gc
import multiprocessing as mltp
import queue
import shutil
from pathlib import Path

import numpy as np
from pyPhases.Data import DataNotFound
from pyPhases.exporter.DataExporter import DataExporter


def loadRecords(extractedDataPaths, options, recordIndices=None, sliceLength=slice(None)):
    arrayList = []
    for size, dataPath in extractedDataPaths:
        if size is not None:
            options["shape"] = (options["shape"][0], options["shape"][1], size)

        try:
            arrayList.append(np.memmap(dataPath, **options)[recordIndices, sliceLength, :])
        except ValueError:
            raise DataNotFound("Memmap file for RecordNumpyMemmapExporter not found: %s" % dataPath)

    return np.concatenate(arrayList, axis=2)




def fillBatchQueue(extractedDataPaths, options, resultQueue=None, resultSize=30, batchLengths=None, startFromBatch=0, recordSlices=None):

    fixedSize = options["shape"][1] if batchLengths is None else None

    def flatten(arr):
        return [item for sublist in arr for item in sublist]

    def reduceByRecordSlices(arr):
        if recordSlices:
            records = [arr[sl] for sl in recordSlices]
            arr = flatten(records)
        return arr


    def getNumbersOfRecordsInBatch():
        return len(batchLengths) if fixedSize is None else options["shape"][0]

    def getBatchLengths():
        return batchLengths

    def recordPositionStart(index):
        l = getBatchLengths()
        return sum(l[0:index])

    def recordPositionEnd(index):
        l = getBatchLengths()
        return sum(l[0:(index+1)])

    def getRecordsFromTo(start, stop=None):
        """ get all available records from a slice
        """
        if stop is None:
            stop = getNumbersOfRecordsInBatch()

        # get position in Batch
        recordCount = stop - start
        if fixedSize:
            s = slice(None)
            recordSlice = np.arange(recordCount) + start
        else:
            s = slice(recordPositionStart(start), recordPositionEnd(stop))
            recordSlice = [0]
        array = loadRecords(extractedDataPaths, options, recordSlice, s)

        if fixedSize is None:
            ret = []
            tailoredLength = reduceByRecordSlices(getBatchLengths())
            for i in range(recordCount):
                recordStart = sum(tailoredLength[0:i])
                recordStop = recordStart + tailoredLength[i]
                ret.append(array[0, recordStart:recordStop, :])
            return ret
        else:
            return list(array)

    def getRecordsFromSlice(s):
        return getRecordsFromTo(s.start, s.stop)

    def getRecordsFromSlices(slices):
        return [r for s in slices for r in getRecordsFromSlice(s)]

    if options["shape"][0] == 0:
        raise Exception(
            "There neeeds to at least on record expected by the np stream exporter, but expected shape is %s"
            % str(options["shape"])
        )

    if recordSlices is None:
        recordSlices = [slice(0, None)]

    if resultQueue is None:
        return getRecordsFromSlices(recordSlices)
    else:
        while True:
            recordsInBatch = 0
            res = []

            # iterate over all recordSlices
            allRecordsInBatch = getNumbersOfRecordsInBatch()
            skipFirstBatches = startFromBatch
            for s in recordSlices:
                sliceStop = allRecordsInBatch if s.stop is None else s.stop
                currentSlice = slice(s.start, sliceStop)
                recordsInSlice = sliceStop - s.start

                # iterate over all possible batches within the record slice
                while recordsInBatch + recordsInSlice >= resultSize:
                    currentSlice = slice(currentSlice.start, currentSlice.start + resultSize - recordsInBatch)
                    if skipFirstBatches <= 0:
                        res += getRecordsFromSlice(currentSlice)
                        resultQueue.put(res)
                    skipFirstBatches -= 1
                    res = []
                    recordsInBatch = 0
                    currentSlice = slice(currentSlice.stop, sliceStop)
                    recordsInSlice = currentSlice.stop - currentSlice.start

                # save all remaining recods for the next slice
                if recordsInSlice > 0:
                    if skipFirstBatches <= 0:
                        res += getRecordsFromSlice(currentSlice)
                    recordsInBatch += recordsInSlice

            # return an un-full batch, if there still records remain
            if recordsInBatch > 0:
                if skipFirstBatches <= 0:
                    resultQueue.put(res)
                skipFirstBatches -= 1

class RecordNumpyMemmapExporter(DataExporter):
    """Asynchrone np exporter"""

    includesStorage = True
    batchFillProcess = None

    def initialOptions(self):
        return {
            "basePath": "data/",
            "multiProcesssing": False,
            "batchTimeout": 10,
            "batchSize": 30,
            "memmap": {},
            "combine": None,
            "recordSlices": None,
        }
        
    def getShapeFilePath(self, dataId):
        return self.getPath(dataId) + "-shape.npy"

    def saveFromArrayList(self, dataId, arrayList):
        """fills the array from a list of 2-dimensional arrays"""
        array = np.concatenate(arrayList)
        array = np.expand_dims(array, 0)
        memmap = self.stream(dataId, {"dtype": "float32", "mode": "w+", "shape": array.shape})
        memmap[:, :, :] = array
        memmap.flush()
        del memmap
        
        lengths = [r.shape[0] for r in arrayList]        
        shape = np.array([lengths, array.shape], dtype="object")
        np.save(self.getShapeFilePath(dataId), shape)
        self.log("saved %s: %s" % (dataId, str(shape)))
        self.finishStream(dataId)


    def checkType(self, type):
        return type == np.memmap

    def getPath(self, dataId):
        return self.getOption("basePath") + dataId

    def stream(self, dataId, options):
        return np.memmap(self.getPath(dataId + "-tmp"), **options)

    def finishStream(self, dataId, options={}):
        path = self.getPath(dataId)
        return shutil.move(path + "-tmp", path)

    def exists(self, dataId, options={}):
        return Path(self.getPath(dataId)).is_file()

    def read(self, dataId, options):

        if "combine" in options:
            sizes, names = zip(*options["combine"])
        else:
            sizes = [None]
            names = [dataId]

        for dId in names:
            if not self.exists(dId):
                raise DataNotFound("Data with id %s nof found" % dId)

        # if no memmap is specified the has to handle the import later
        if "memmap" not in options or "shape" not in options["memmap"]:
            for dId in names:
                shapePath = self.getShapeFilePath(dataId)
                if Path(shapePath).exists():
                    lengths, shape = np.load(shapePath, allow_pickle=True)
                    if "memmap" not in options:
                        options["memmap"] = {}
                        
                    options["lengths"] = lengths
                    options["memmap"]["shape"] = shape
        
        if "dtype" not in options["memmap"]:
            options["memmap"]["dtype"] = "float32"
            
        if "mode" not in options["memmap"]:
            options["memmap"]["mode"] = "r"
            

        self.memmapOptions = options["memmap"]
        self.extractedDataPaths = [(size, self.getPath(name)) for name, size in zip(names, sizes)]

        self.CurrentItemIndex = 0
        self.currentBatchIndex = 0
        self.result = None
        self.length = self.memmapOptions["shape"][0]
        self.recordLengths = None
        self.termindated = False
        self.recordSlices = None

        if "recordSlices" in options:
            self.recordSlices = options["recordSlices"]

        if "lengths" in options and options["lengths"] is not None:
            self.recordLengths = options["lengths"]
            self.length = len(options["lengths"])

        if self.recordSlices is not None:
            if "lengths" in options and options["lengths"]:
                self.length = sum([len(options["lengths"][s]) for s in options["recordSlices"]])
            else:
                self.length = sum([len(range(10)[s]) for s in options["recordSlices"]])

        if self.length == 0:
            raise Exception("Stream has no records (empty shape or empty record slices)")

        # todo outsource to optionize
        if "multiProcesssing" in options:
            self.options["multiProcesssing"] = options["multiProcesssing"]

        if "batchTimeout" in options:
            self.options["batchTimeout"] = options["batchTimeout"]

        if "batchSize" in options:
            self.batchSize = options["batchSize"]
        else:
            self.batchSize = self.getOption("batchSize")

        if not self.options["multiProcesssing"]:
            self.batchSize = self.length

        self.log("Prepare loading %s (multiprocessing: %i)" % (self.extractedDataPaths, self.getOption("multiProcesssing")))

        if not self.getOption("multiProcesssing"):
            self.result = fillBatchQueue(
                self.extractedDataPaths,
                self.memmapOptions,
                resultSize=self.batchSize,
                batchLengths=self.recordLengths,
                recordSlices=self.recordSlices,
            )
        else:
            self.startBatch()
        return self

    def loadNextBatch(self):
        result = None
        curIndex = self.batchSize * self.currentBatchIndex + self.CurrentItemIndex
        timeout = self.getOption("batchTimeout")
        self.currentBatchIndex += 1
        while result is None:
            if self.termindated:
                self.restartBatch(startFromBatch=curIndex // self.batchSize)

            try:
                result = self.resultQueue.get(timeout=timeout)
            except queue.Empty as e:
                self.logWarning("Batch Filling run Empty, restart Batch(#%i): %s" % (curIndex // self.batchSize, e))
                self.restartBatch(startFromBatch=curIndex // self.batchSize)
                result = None
            except Exception as e:
                self.logError("Batch Fill hung, restart Batch(#%i): %s" % (curIndex // self.batchSize, e))
                self.restartBatch(startFromBatch=curIndex // self.batchSize)
                result = None

        self.result = result

    def startBatch(self):
        self.restartBatch(terminate=False)

    def restartBatch(self, terminate=True, startFromBatch=0):

        self.currentBatchIndex = startFromBatch

        self.result = None
        if self.getOption("multiProcesssing"):
            if terminate and not self.termindated:
                self.batchFillProcess.terminate()

            self.resultManager = mltp.Manager()
            self.resultQueue = self.resultManager.Queue(maxsize=1)

            self.batchFillProcess = mltp.Process(
                target=fillBatchQueue,
                args=(
                    self.extractedDataPaths,
                    self.memmapOptions,
                    self.resultQueue,
                    self.batchSize,
                    self.recordLengths,
                    startFromBatch,  # startwith current batch
                    self.recordSlices,
                ),
            )
            self.termindated = False
            gc.collect()
            self.batchFillProcess.start()
        else:
            self.result = fillBatchQueue(
                self.extractedDataPaths,
                self.memmapOptions,
                resultSize=self.batchSize,
                batchLengths=self.recordLengths,
                startFromBatch=startFromBatch,
                recordSlices=self.recordSlices,
            )

    def __iter__(self):
        if self.CurrentItemIndex > 0 or self.currentBatchIndex > 0:
            self.restartBatch(startFromBatch=0)
        if self.getOption("multiProcesssing"):
            self.result = None
        self.currentBatchIndex = 0
        self.CurrentItemIndex = 0
        return self

    def __next__(self, raiseStopIteration=True):
        if self.result is None:
            self.loadNextBatch()
            self.CurrentItemIndex = 0
            self.currentBatchIndex = 0

        totalIndex = self.currentBatchIndex * self.batchSize + self.CurrentItemIndex

        if raiseStopIteration and totalIndex >= self.length:
            raise StopIteration

        if self.getOption("multiProcesssing") and (self.CurrentItemIndex >= self.batchSize):
            self.loadNextBatch()
            self.CurrentItemIndex = 0

        itemResult = self.result[self.CurrentItemIndex]

        self.CurrentItemIndex += 1

        return itemResult

    def __getitem__(self, index):
        requiresBatch = index // self.batchSize

        if self.getOption("multiProcesssing"):
            if requiresBatch != self.currentBatchIndex:
                self.restartBatch(startFromBatch=requiresBatch)
                self.result = self.resultQueue.get()
            elif self.result is None:
                self.result = self.resultQueue.get()
            index = index % self.batchSize
        return self.result[index]

    def getNextItem(self):
        return self.__next__()

    def getNextItemAndReshuffle(self):
        try:
            return self.__next__(True)
        except StopIteration:
            self.CurrentItemIndex = 0
            self.restartBatch()
            return self.__next__(True)

    def __len__(self):
        return self.length

    def getAll(self):
        return self.result

    def close(self):
        if self.getOption("multiProcesssing"):
            self.batchFillProcess.terminate()
            self.termindated = True
