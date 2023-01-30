from dataclasses import dataclass


@dataclass
class PCIDevice:
    vendor_id: int
    product_id: int
    revision: int

    def __hash__(self):
        return self.vendor_id << 24 | self.product_id << 8 | self.revision

    def __str__(self):
        return f"{hex(self.vendor_id)}:{hex(self.product_id)}:{hex(self.revision)}"

    @classmethod
    def from_str(cls, pciid):
        fields = pciid.split(":")
        if len(fields) not in [2, 3]:
            raise ValueError("The pciid '{pciid}' is invalid. Format: xxxx:xxxx[:xx]")

        revision = 0 if len(fields) == 2 else int(fields[2], 16)
        return cls(vendor_id=int(fields[0], 16),
                   product_id=int(fields[1], 16),
                   revision=revision)
