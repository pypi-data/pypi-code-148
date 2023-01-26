import numpy as np
from numpy.random import default_rng


class DataAugmentation:
    
    customAugmentation = {}
    
    @classmethod
    def addAugmentation(cls, name, function):
        """ Adds a custom augmentation function to the DataAugmentation, the function must have the following signature: (X, Y, config)"""
        cls.customAugmentation[name] = function
        
    @staticmethod
    def augmentRecordWiseByConfig(configArray, X, Y, splitName):
        X = np.expand_dims(X, axis=0)
        Y = np.expand_dims(Y, axis=0)
        X, Y = DataAugmentation.augmentByConfig(configArray, X, Y, splitName)
        
        # return X[0,:,:], Y[0,:,:]
        return X, Y
    
    @staticmethod
    def augmentByConfig(configArray, X, Y, splitName):
        for c in configArray:
            X, Y = DataAugmentation.loadFromConfig(c, X, Y, splitName)
        return X, Y
    
    @staticmethod
    def loadFromConfig(config, X, Y, splitName):
        name = config["name"]
        if "trainingOnly" in config and config["trainingOnly"] and splitName != "training":
            return X, Y

        if name == "TemporalContext":
            contextSize = config["addedChannels"] + 1
            X = DataAugmentation.temporalContext(X, contextSize)
            # the test dataset does not need temporalContext for the evaluation
            if splitName != "Test":
                Y = DataAugmentation.temporalContext(Y, contextSize)
        elif name == "ShuffleSegments":
            seed = config["seed"] if "seed" in config else None
            X, Y = DataAugmentation.shuffle(X, Y, seed)
        elif name == "gaussNoise":
            stddev = config["stddev"] if "stddev" in config else None
            X = DataAugmentation.gaussNoise(X, stddev)
        elif name == "channelSelect":
            sliceSplit = [int(s) for s in str(config["channels"]).split(":")]
            X = DataAugmentation.channelSelect(X, slice(*sliceSplit))
        elif name == "replaceYWithX":
            sliceSplit = [int(s) for s in str(config["channels"]).split(":")]
            Y = DataAugmentation.channelSelect(X, slice(*sliceSplit))
        elif name == "znorm":
            X = DataAugmentation.znorm(X)
        elif name == "cutForSegmentLength":
            X, Y = DataAugmentation.cutForSegmentLength(X, Y, config["segmentLength"])
        elif name == "MagScale":
            low = config["low"] if "low" in config else 0.8
            high = config["high"] if "high" in config else 1.25
            X = DataAugmentation.MagScale(X, low, high)
        elif name == "channelShuffle":
            channelSlice = config["channelSlice"]
            X = DataAugmentation.channelShuffle(X, channelSlice)
        elif name == "ReshapeWithOverlap":
            X = DataAugmentation.reshapeWithOverlap(X, config["windowSize"], config["stepSize"])

        elif name == "fixedSize":
            center = config["position"] == "center"
            size = config["size"]
            sizeY = config["sizeY"] if "sizeY" in config else size
            X = DataAugmentation.fixedSize(X, size, fillValue=0, center=center)
            Y = DataAugmentation.fixedSize(Y, sizeY, fillValue=-1, center=center)

        elif name == "smoothWindowY":
            Y = DataAugmentation.smoothWindow(Y, config["windowSize"])
        elif name == "softMax":
            Y = DataAugmentation.softMax(Y)
        elif name == "restoreLength":
            originalLength = config["originalLength"]
            if config["originalLength"] is not None:
                Y = DataAugmentation.restoreLength(Y, originalLength)
        elif name in DataAugmentation.customAugmentation:
            XY = DataAugmentation.customAugmentation[name](X, Y, config)
            if XY is not None:
                X, Y = XY
        else:
            raise Exception("Unknown augmentation: %s, you can add custom Augmentation using DataAugmentation.addAugmentation()"%name)

        return X, Y

    """
    all data inputs (`array`) is expected to be in following default shape: (-1, Segementlength, Channelcount)
    """

    @staticmethod
    def paddingSegments(array, paddingSize):
        """adds a zero filled segments before and after the array

        Args:
            paddingSize ([int]): padding size in samples
        """
        _, windowSize, numChannels = array.shape
        padding = np.zeros((paddingSize, windowSize, numChannels))

        return np.concatenate((padding, array, padding))

    @staticmethod
    def temporalContext(array, contextSize):
        """Create a temporal context, by adding `contextSize` channels, with the content of
           future segments

        Args:
            contextSize ([int]): channel count to be added

        """
        _, windowSize, numChannels = array.shape
        size = len(array)

        marginSize = contextSize // 2
        paddedX = DataAugmentation.paddingSegments(array, marginSize)

        newX = np.empty((size, contextSize, windowSize, numChannels), dtype=array.dtype)

        for XId in range(marginSize, size + marginSize):
            startAt = XId - marginSize
            endWith = XId + marginSize + 1
            newX[startAt, ::, ::, ::] = paddedX[startAt:endWith, ::, ::]
            # assert all(newX[startAt, ::, 10] == array[startAt, ::, 0])

        return newX

    @staticmethod
    def shuffle(X, Y, seed=None):
        """shuffles all segments (axis=0)

        Args:
            seed ([int]): numpy seed to use

        """
        if not seed:
            seed = 2
        np.random.seed(seed)
        np.random.shuffle(X)
        np.random.seed(seed)
        np.random.shuffle(Y)

        return X, Y

    @staticmethod
    def channelShuffle(X, channelSlice, seed=None):

        rng = default_rng(seed)
        channelSlice = slice(channelSlice[0], channelSlice[1])

        cutChannels = X[:, :, channelSlice].copy()
        rng.shuffle(cutChannels, axis=2)
        X[:, :, channelSlice] = cutChannels

        return X

    @staticmethod
    def channelSelect(X, channelSlice=slice(0, None)):
        """selects all channels fitting the given slice

        Args:
            channelSlice (slice): array slice

        """

        return X[:, :, channelSlice]

    @staticmethod
    def fixedSize(X, size, fillValue=0, center=True):
        newShape = list(X.shape)
        newShape[1] = size

        centerNew = size // 2
        signalSize = X.shape[1]
        centerSignal = signalSize // 2

        startAt = centerNew - centerSignal if center else 0

        newX = np.full(newShape, fillValue, dtype=X.dtype)

        if X.shape[1] > size:
            startAt *= -1
            newX[:, :, :] = X[:, startAt : startAt + newShape[1], :]
        else:
            newX[:, startAt : startAt + signalSize, :] = X

        return newX

    @staticmethod
    def znorm(X):
        X = (X - X.mean(axis=1, keepdims=True)) / (X.std(axis=1, keepdims=True) + 0.000000001)
        return X

    @staticmethod
    def MagScale(X, low=0.8, high=1.25, seed=2):
        rng = default_rng(seed)
        scale = low + rng.random(1, dtype=X.dtype) * (high - low)
        X = scale * X

        return X

    @staticmethod
    def reshapeWithOverlap(X, windowSize, stepSize):
        windowSize = int(windowSize)
        stepSize = int(stepSize)
        segmentLength = int(X.shape[1] / stepSize)
        newX = []
        for Xi in X:
            # padding
            paddingSize = int((windowSize / 2) - (stepSize / 2))
            padding = np.zeros((paddingSize, Xi.shape[1]))
            paddedX = np.concatenate((padding, Xi, padding))
            # list comprehension
            last_start = paddedX.shape[0] - windowSize + 1
            period_starts = range(0, last_start, stepSize)
            reshapedX = np.array([paddedX[k : k + windowSize, :] for k in period_starts])
            # reshape to numpy: (4,240,1200,2)
            newX.append(reshapedX)
        # parameters:
        # numSegements = 4 = X.shape[0]
        # predictionsPerSegment=240
        #
        return np.array(newX)

    @staticmethod
    def majorityVoteAnnotations(Y, windowSize, channel, reduce=False):
        windowSize = int(windowSize)
        segmentLength = Y.shape[1]
        channelCount = Y.shape[2]
        Y = Y.reshape(-1, windowSize, channelCount)
        for yIndex, _ in enumerate(Y):

            values, counts = np.unique(Y[yIndex, ::, channel], return_counts=True)
            majorityIndex = np.argmax(counts)

            Y[yIndex, ::, channel] = values[majorityIndex]

        Y = Y.reshape(-1, segmentLength, channelCount)
        if reduce:
            Y = Y[:, ::windowSize, :]

        return Y

    @staticmethod
    def cutForSegmentLength(X, Y, segmentLength):
        length = X.shape[1]
        if length % segmentLength != 0:
            f = length // segmentLength
            end = f * segmentLength
            X = X[:, :end, :]
            Y = Y[:, :end, :]
        return X, Y

    @staticmethod
    def gaussNoise(X, stddev=0.01):
        noise = np.random.normal(0, 0.05, X.shape).astype(X.dtype)
        return X + noise

    def smoothWindow(Y, windowSize, threshHold=0):
        filter = np.full(windowSize, 1)
        assert Y.shape[0] == 1
        classCount = Y.shape[2]
        for i in range(classCount):
            Y[0, :, i] = np.convolve(Y[0, :, i], filter, "same")
        return Y / windowSize

    def softMax(y):
        m = np.max(y, axis=2)
        m = m[:, :, np.newaxis]
        e_y = np.exp(y - m)
        div = np.sum(e_y, axis=2)
        div = div[:, :, np.newaxis]
        return e_y / div

    def restoreLength(y, length):
        curLength = y.shape[1]
        padLeft = (curLength - length) // 2

        return y[:, padLeft : (padLeft + length), :]
