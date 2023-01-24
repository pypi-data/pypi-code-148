from __future__ import annotations
from typing import Union, List, Optional, TYPE_CHECKING
from dataclasses import dataclass
from uuid import uuid4

if TYPE_CHECKING:
    from Akatosh import Actor


@dataclass
class ResourceClaim:
    _user: Actor
    _quantity: Union[int, float]

    def __eq__(self, __o: ResourceClaim) -> bool:
        if self.user is __o.user:
            return True
        else:
            return False

    @property
    def user(self) -> Actor:
        return self._user

    @property
    def quantity(self) -> Union[int, float]:
        return self._quantity


class Resource:

    _id: int
    _label: str
    _capacity: Union[int, float]
    _claimed_quantity: Union[int, float]

    _claims: List[ResourceClaim]

    def __init__(
        self,
        label: Optional[str] = None,
        capacity: Union[int, float] = 1,
        init_claimed_quantity: Union[int, float] = 0,
    ) -> None:
        self._id = uuid4().int
        self._label = label or str()
        self._capacity = capacity
        self._claimed_quantity = init_claimed_quantity

        self._claims = list()

    def get(self, quantity: Union[int, float]) -> bool:
        if quantity <= self.available_quantity:
            self._claimed_quantity += quantity
            return True
        else:
            raise ValueError(
                f"Quantity {quantity} is greater than available quantity {self.available_quantity}."
            )

    def put(self, quantity: Union[int, float]) -> bool:
        if quantity <= self.claimed_quantity:
            self._claimed_quantity -= quantity
            return True
        else:
            raise ValueError(
                f"Quantity {quantity} is greater than claimed quantity {self.claimed_quantity}."
            )

    def distribute(self, user: Actor, quantity: Union[int, float]) -> bool:
        if quantity <= self.available_quantity:
            self._claimed_quantity += quantity
            resource_claim = ResourceClaim(user, quantity)
            if resource_claim not in self.claims:
                self.claims.append(resource_claim)
                return True
            else:
                for claim in self.claims:
                    if claim.user is user:
                        claim._quantity += quantity
                        return True
        else:
            raise ValueError(
                f"Quantity {quantity} is greater than available quantity {self.available_quantity}."
            )

    def release(self, user: Optional[Actor | List[Actor]] = None, amount:Optional[int | float]=None) -> bool:
        if user is None:
            self._claimed_quantity = 0
            self._claims.clear()
            return True
        else:
            if isinstance(user, list):
                for u in user:
                    for claim in self.claims[:]:
                        if claim.user == u:
                            if amount is None:
                                if claim.quantity > self.claimed_quantity:
                                    raise ValueError(
                                        f"Resource claim's quantity {claim.quantity} is greater than resource's claimed quantity {self.claimed_quantity}."
                                    )
                                else:
                                    self._claimed_quantity -= claim.quantity
                                    self.claims.remove(claim)
                            else:
                                if amount > claim.quantity:
                                    raise ValueError(
                                        f"User tries to release {amount} units, but only {claim.quantity} units are claimed by the user."
                                    )
                                else:
                                    self._claimed_quantity -= amount
                                    claim._quantity -= amount
                                    if claim.quantity == 0:
                                        self.claims.remove(claim)
            else:
                for claim in self.claims[:]:
                    if claim.user == user:
                        if amount is None:
                            if claim.quantity > self.claimed_quantity:
                                raise ValueError(
                                    f"Resource claim's quantity {claim.quantity} is greater than resource's claimed quantity {self.claimed_quantity}."
                                )
                            else:
                                self._claimed_quantity -= claim.quantity
                                self.claims.remove(claim)
                        else:
                            if amount > claim.quantity:
                                raise ValueError(
                                    f"User tries to release {amount} units, but only {claim.quantity} units are claimed by the user."
                                )
                            else:
                                self._claimed_quantity -= amount
                                claim._quantity -= amount
                                if claim.quantity == 0:
                                    self.claims.remove(claim)

    @property
    def id(self) -> int:
        return self._id

    @property
    def label(self) -> str:
        return self._label

    @property
    def capacity(self) -> Union[int, float]:
        return self._capacity

    @property
    def claimed_quantity(self) -> Union[int, float]:
        return self._claimed_quantity

    @property
    def available_quantity(self) -> Union[int, float]:
        return self.capacity - self.claimed_quantity

    @property
    def claims(self) -> List[ResourceClaim]:
        return self._claims

    @property
    def users(self):
        return [claim.user for claim in self.claims]

    @property
    def  utilization(self) -> Union[int, float]:
        return self.claimed_quantity / self.capacity
