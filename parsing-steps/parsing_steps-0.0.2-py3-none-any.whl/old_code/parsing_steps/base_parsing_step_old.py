class BaseParsingStep(object):
    """
    Base class for parsing data step by step.
    The class represents one parsing step.

    input_data is required on initializing.
    To start parsing, call the "perform" method.

    For multithreaded use, override the "perform_next_step" method.
    To bypass locks, override the "download" method,
    adding some protection there.
    (This can happen with a large number of requests)
    """

    is_save_data_step = False
    next_step_class = None
    perform_in_new_thread = None
    non_inheritable_kwargs = [
        "num_in_list",
    ]

    def __init__(self, input_data, *args, **kwargs):
        """
        Sets the input parameters as the class fields.
        "input_data" parameter is required
        """
        # print(f"\n\n\n\n\n__init__ {self.__class__.__name__}")
        self.input_data = input_data
        for name, value in kwargs.items():
            setattr(self, name, value)

        self.input_args = args
        self.next_step_args = args
        self.input_kwargs = kwargs
        self.next_step_kwargs = {name: value for name, value in kwargs.items()
                                 if name not in self.non_inheritable_kwargs}

    def get_next_step_class(self, *args, **kwargs):
        """
        Returns "next_step" class
        """
        # print("get_next_step_class")
        return self.next_step_class

    def prepare_input_data(self, *args, **kwargs):
        """
        Prepares input data and modifies it (if needed).
        The initial data is written to self.raw_input_data.
        """
        # print("prepare_input_data")
        self.raw_input_data = self.input_data

    def input_data_is_valid(self, raise_exceptions=False, *args, **kwargs):
        """
        Input data validation.
        Returns True if input_data is valid,
        or False otherwise
        """
        # print("input_data_is_valid")
        self.validated_input_data = getattr(self, "input_data", None)
        return True

    def download(self, *args, **kwargs):
        """
        Downloading or something else.
        makes "raw_output_data" from "input_data".
        """
        # print("download")
        self.raw_output_data = self.input_data

    def process_raw_data(self, *args, **kwargs):
        """
        Processes input data.
        Takes raw data and writes to the field "output_data"
        """
        # print("process_raw_data")
        self.output_data = [self.raw_output_data]

    def input_data_to_output_data(self, *args, **kwargs):
        """
        processes input_data to produce output_data.
        """
        # print("input_data_to_output_data")
        self.download(*args, **kwargs)
        self.process_raw_data(*args, **kwargs)

    def process_if_not_valid(self, *args, **kwargs):
        """
        Actions that will run in case of invalid "input_data".
        Must be overridden if validation is overridden.
        """
        # print("process_if_not_valid")
        raise NotImplementedError

    def perform_next_step(self, next_step_class, input_data,
                          *next_step_args, **next_step_kwargs):
        """
        The method that starts the next parsing step.
        The code is run by the calling "perform" method.

        If you want to run parsing in multi-threaded mode or through tasks
        (celery, for example) - override this method.
        The "next_step.perform(*args, **kwargs)" method must be run
        on a new thread, process or task in this case.
        """
        # print("perform_next_step")
        if next_step_class is None:
            return None
        next_step = next_step_class(input_data=input_data,
                                    *next_step_args, **next_step_kwargs)
        return next_step.perform()

    def save_data(self, *args, **kwargs):
        """
        This method is called if the "is_save_data_step"
        attribute is set to True.
        Should be overridden in this case.
        """
        # print("save_data")
        raise NotImplementedError

    def parse(self, *args, **kwargs):
        """
        The method is called if
        the "is_save_data_step" attribute is set to False.
        """
        # print("parse")
        self.input_data_to_output_data(*args, **kwargs)

    def perform(self):
        """
        Performs data parsing.
        """
        # print("perform")
        args = self.input_args
        kwargs = self.input_kwargs

        # print(f"args: {args}")
        # print(f"kwargs: {kwargs}")
        self.prepare_input_data(*args, **kwargs)
        if self.input_data_is_valid(*args, **kwargs):
            if self.is_save_data_step:
                self.save_data(*args, **kwargs)
            else:
                self.input_data_to_output_data(*args, **kwargs)

            self.output_data = getattr(self, "output_data", None)
            if type(self.output_data) is not list:
                self.output_data = [self.output_data]
            for num_in_list, data in enumerate(self.output_data, start=1):
                next_step_class = self.get_next_step_class(data=data)
                self.perform_next_step(next_step_class=next_step_class,
                                       input_data=data,
                                       num_in_list=num_in_list,
                                       *self.next_step_args,
                                       **self.next_step_kwargs)
                # return None
        else:
            self.process_if_not_valid(*args, **kwargs)
