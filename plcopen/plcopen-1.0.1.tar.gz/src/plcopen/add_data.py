from dataclasses import dataclass, field
from typing import List, Optional
import plcopen.project
from plcopen.data_handle_unknown import DataHandleUnknown

__NAMESPACE__ = "http://www.plcopen.org/xml/tc6_0201"


@dataclass
class AddData:
    """
    Application specific data defined in external schemata.
    """
    class Meta:
        name = "addData"

    data: List["AddData.Data"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.plcopen.org/xml/tc6_0201",
        }
    )

    def get_data_by_name(self, name: str) -> Optional["AddData.Data"]:
        return next(iter([data for data in self.data if data.name == name]), None)


    @dataclass
    class Data:
        """
        :ivar any_element:
        :ivar name: Uniquely identifies the additional data element.
        :ivar handle_unknown: Recommended processor handling for unknown
            data elements. Specifies if the processor should try to
            preserve the additional data element, dismiss the element
            (e.g. because the data is invalid if not updated correctly)
            or use the processors default behaviour for unknown data.
        """
        
        configurations: Optional["plcopen.project.Project.Instances.Configurations"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201",
            }
        )
        pou: List["plcopen.project.Project.Types.Pous.Pou"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "http://www.plcopen.org/xml/tc6_0201"
            }
        )
        any_element: Optional[object] = field(
            default=None,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            }
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        handle_unknown: Optional[DataHandleUnknown] = field(
            default=None,
            metadata={
                "name": "handleUnknown",
                "type": "Attribute",
                "required": True,
            }
        )
