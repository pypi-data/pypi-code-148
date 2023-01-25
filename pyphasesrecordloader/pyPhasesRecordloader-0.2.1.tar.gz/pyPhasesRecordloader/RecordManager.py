from teleschlafmedizin.model.PSGSignal import PSGSignal
from teleschlafmedizin.model.Annotation import Annotation
from teleschlafmedizin.model.recordManager.RecordMeta import Channel, Record, RecordAnnotation, RecordChannel
from pyPhases.util.Logger import classLogger
from teleschlafmedizin.model.util.DynamicModule import DynamicModule
from . import recordLoaders as recordManagerPath




class RecordWriter:
    recordWriter = DynamicModule(recordManagerPath)
    record: Record = None

    def writerRecord(recordName):
        pass

    def writeAnnotation(self, annotation: Annotation):
        pass

    def writeDataAnnotation(self, dataAnnotation: RecordAnnotation):
        """Writes a RecordAnnotationannotation to the Record

        Args:
            dataAnnotation (Annotation): RecordAnnotation with events and an Annotation with name

        """
        a = self.annotation.fromDataAnnotation(dataAnnotation)
        return self.writeAnnotation(a)

    @staticmethod
    def get() -> "RecordWriter":
        return RecordWriter.recordWriter.get()


class RecordManager:
    @staticmethod
    def getReader() -> RecordLoader:
        return RecordLoader.get()

    def getWriter() -> RecordWriter:
        return RecordWriter.get()
