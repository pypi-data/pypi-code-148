class BaseParsingStep(object):
    """
    Base class for parsing data step by step.
    The class represents one parsing step.

    input_data is required on initializing.
    To start parsing, call the "perform" method.

    input_data_to_output_data method must be overrated on inherited classes.

    For multithreaded use, override the "perform_next_step" method.
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
        return self.next_step_class

    def input_data_to_output_data(self, *args, **kwargs):
        """
        processes input_data to produce output_data.
        """
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
        if next_step_class is None:
            return None
        next_step = next_step_class(input_data=input_data,
                                    *next_step_args, **next_step_kwargs)
        return next_step.perform()

    def perform(self):
        """
        Performs data parsing.
        """
        self.input_data_to_output_data()
        self.output_data = getattr(self, "output_data", None)

        assert hasattr(self.output_data, "__iter__") or \
            self.output_data is None, \
            "Wrong data type of output data. " \
            "Must be either an iterable object or None."

        if self.output_data is None:
            return

        for num_in_list, data in enumerate(self.output_data, start=1):
            next_step_class = self.get_next_step_class(data=data)
            if next_step_class:
                self.perform_next_step(next_step_class=next_step_class,
                                       input_data=data,
                                       num_in_list=num_in_list,
                                       *self.next_step_args,
                                       **self.next_step_kwargs)
