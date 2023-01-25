from augmolino import augmentation
import numpy as np
import os


class augmenter:

    def __init__(self, augmentations=None):
        """
        Group class which holds a dynamic amount of 
        augmentations specified by the user

        Parameters
        ----------
        `augmentations`:
            Augmentation. Single or array of augmentations from
            `augmentation.py`. If left unspecified, the augmenter
            can later be filled with augmentations via `augmenter.add()`.
            Default is `None`.

        Examples
        --------
        >>> # get augmentations as signals and plot them:
        >>> from augmolino import augmenter, augmentation
        >>> import matplotlib.pyplot as plt
        >>> # specify set of augmentations:
        >>> augs = [
                augmentation.timeStretch(rate=2),
                augmentation.pitchShift(semitones=2),
                augmentation.offsetAudio(s=1)]
        >>> # create the augmenter
        >>> a = augmenter.augmenter(augs)
        >>> # run augmenter
        >>> xs = a.execute("tests/sounds/impulse_response.wav")
        >>> # create plot
        >>> fig, axs = plt.subplots(3,1)
        >>> # display signals
        >>> for i, x in enumerate(xs):
            >>> axs[i].plot(x)
        >>> plt.show()
        """

        if not augmentations:
            # init empty augmenter
            self.pipe = []

        else:
            # create array of augmentations
            if len(augmentations) > 1:
                self.pipe = augmentations
            else:
                self.pipe = [augmentations]

    def add(self, augmentation):
        """
        Add a single augmentation to the augmenter pipeline.

        Parameters
        ----------
        `augmentation`:
            Augmentation. Gets appended to existing or empty
            pipe of augmentations within the augmenter.
        """
        self.pipe.append(augmentation)

    def execute(self, source, dest=None, **kwargs):
        """
        Run all augmentations within the pipe. Specific settings are
        inside of each augmentation.

        Parameters
        ----------
        `source`:
            List, String. Source of data. Can be a folder,
            array of filenames or single files.
        `dest`:
            String. Destination for saved augmented files. If `None`
            is passed, the first augmented signals per augmentation
            are returned as `numpy` array and not saved. Pass `"auto"`
            to save them to the source folder under unique IDs generated
            from the augmentations settings. Default is `None`.
        `kwargs`:
            Keyword arguments which were not passed in the initialization
            of augmentations. They get appended here.

        Returns
        -------
        `xs`:
            Array, None. Returns each augmented signal if no save location
            has been specified for the coresponding augmentation.
            Otherwise it returns `None`.

        """

        # source given as a list of file paths
        if isinstance(source, (list, tuple, np.ndarray)):
            files = source

        # single source path to file
        if os.path.isfile(source):
            files = [source]

        # source given as parent folder
        if os.path.isdir(source):
            if dest == None:
                raise ValueError("Augmenter without save directory "\
                    "pointed to multiple files. Did you forget "\
                    "to specify a path?")
            files = [os.path.join(source, file) for file in os.listdir(source) if file.lower().endswith("wav")]

        if dest == None:
            xs = [[]] * len(self.pipe)
        else:
            xs = None
        # this is sloooow but the only way to append dynamic sizes
        for i, augmentation in enumerate(self.pipe):
            for file in files:
                x = augmentation.run(file, dest, **kwargs)

                if dest == None:
                    xs[i].append(x)
                    xs[i] = np.asarray(xs[i][i])

        return xs

    def summary(self):

        num_aug = len(self.pipe)

        print("")
        print("------------augmenter.summary------------")
        print("-----------------------------------------")
        print(f" number of augmentations: {num_aug}     ")
        print("")
        print(" type:                                   ")

        for aug in self.pipe:
            print(f" > {aug.descriptor}                 ")

        print("------------augmenter.summary------------")
        print("")
