import xml.etree.ElementTree as ET

from pyPhases.util.Logger import classLogger

from pyPhasesRecordloader.RecordLoader import ParseError


@classLogger
class XMLAnnotationLoader:
    def __init__(self) -> None:
        super().__init__()

        self.annotations = []
        self.metaXML = None
        self.lightOff = 0
        self.lightOn = None
        self.annotationFrequency = 1
        self.minApneaDuration = 0

    def loadXmlFile(self, filePath):
        # nur trusted verwenden! siehe: https://docs.python.org/3/library/xml.html#xml-vulnerabilities
        self.log("Load xml file %s" % filePath)
        try:
            self.metaXML = ET.parse(filePath).getroot()
        except Exception as e:
            raise ParseError("Error parsing xml file %s: %s" % (filePath, e))
