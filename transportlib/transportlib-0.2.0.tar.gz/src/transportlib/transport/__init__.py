import abc

class BaseTransport(abc.ABC):

    def __init__(self,
                 csv_file_path,
                 watermark_val_prev = None,
                 watermark_val_curr = None,
                 *args,
                 **kwargs
                 ):
        self.csv_file_path = csv_file_path
        self.watermark_val_prev = watermark_val_prev
        self.watermark_val_curr = watermark_val_curr

    @abc.abstractmethod
    def run(self):
        pass
