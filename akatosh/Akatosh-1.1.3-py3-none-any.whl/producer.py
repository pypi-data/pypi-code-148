from __future__ import annotations
from copy import deepcopy
from typing import Generator, List, Optional, Union, Callable, TYPE_CHECKING
from uuid import uuid4
import warnings
from math import inf

from Akatosh import Timeline, Mundus, Actor


class Consumer:
    _user: Actor
    _products: List

    def __init__(self, user: Actor) -> None:
        self._user = user
        self._products = list()

    def __eq__(self, __o: Consumer) -> bool:
        if self.user is __o.user:
            return True
        else:
            return False

    @property
    def user(self) -> Actor:
        return self._user

    @property
    def quantity(self) -> Union[int, float]:
        return len(self._products)

    @property
    def products(self) -> List:
        return self._products


class Producer:

    _id: int
    _action: Optional[Generator | Callable]
    _timeline: Timeline
    _priority: int
    _at: Union[int, float]
    _step: Union[int, float, Callable]
    _till: Union[int, float]
    _active: bool
    _after: Actor

    _time: Union[int, float]
    _status: List[str]
    _followers: List[Actor]

    _label: str
    _product: Callable
    _product_kargs: dict
    _production_rate: int
    _capacity: int
    _inventory: List
    _consumers: List[Consumer]

    def __init__(
        self,
        product: Callable,
        product_kargs: dict,
        prodction_rate: int,
        step: Union[int, float],
        timeline: Optional[Timeline] = None,
        priority: int = 0,
        at: Union[int, float, Callable] = 0,
        till: Optional[int | float | Callable] = None,
        active: bool = True,
        after: Optional[Actor] = None,
        label: Optional[str] = None,
        capacity: int = 1,
    ) -> None:

        # generate a unique id for this producer
        self._id = uuid4().int

        # assign the timeline to this producer
        if timeline is None:
            self._timeline = Mundus.timeline
        else:
            self._timeline = timeline
        self.timeline.actors.append(self)

        # assign the priority to this producer
        self._priority = priority

        # initialize the follower list
        self._followers = list()

        # assign the waiting target to this producer
        if after is not None:
            self._after = after
            after.followers.append(self)
            if after.priority > self.priority:
                warnings.warn(
                    message=f"Producer {self.id} has a lower priority than its waiting target {after.id}."
                )

        # initialize the time
        self._time = at
        self._till = till

        # initialize the status
        self._status = list()
        if active:
            self.status.append("active")
        else:
            self.status.append("inactive")
        if after is not None:
            self.status.append("onhold")

        # schedule the actor onto timeline
        if self.onhold is False:
            self.timeline.schedule(self)

        self._label = label or str()
        self._product = product
        self._product_kargs = product_kargs
        self._production_rate = prodction_rate
        self._step = step
        self._capacity = capacity
        self._inventory = list()
        self._consumers = list()

        if hasattr(self.product, "_priority"):
            if self.product.priority < self.priority:
                warnings.warn(
                    message=f"Producer {self} has lower priority than its producer's priority {self.priority}."
                )

    def perform(self):
        # non-continuous actor
        if self.step is None and self.till is None:
            if self.active:
                self.action()
        # continuous actor but misses step size
        elif self.step is None and self.till is not None:
            raise AttributeError(f"Actor {self.id} has no step size defined.")
        # continuous actor with step size but no end time
        elif self.step is not None and self.till is None:
            self._till = inf
            while self.time < self.till:
                if self.active:
                    self.action()
                if callable(self.step):
                    self._time += self.step()
                else:
                    self._time += self.step
                yield self.timeline.schedule(self)
            if self.active:
                self.action()
        # continuous actor with step size and end time
        elif self.step is not None and self.till is not None:
            if callable(self.till):
                self._till = self.till()
            while self.time < self.till:
                if self.active:
                    self.action()
                if callable(self.step):
                    self._time += self.step()
                else:
                    self._time += self.step
                yield self.timeline.schedule(self)
            if self.active:
                self.action()

    def action(self):
        for _ in range(self.production_rate):
            self.inventory.append(self.product(**self.product_kargs))

    def deactivate(self):
        if "active" in self.status:
            self.status.remove("active")
        if "inactive" not in self.status:
            self.status.append("inactive")

    def get(self, quantity: int = 1) -> List:
        if quantity <= len(self.inventory):
            return [self.inventory.pop() for _ in range(quantity)]
        else:
            raise ValueError(
                f"Quantity {quantity} is greater than available quantity {len(self.inventory)}."
            )

    def restock(self, quantity: int = 1) -> None:
        if len(self.inventory) + quantity <= self.capacity:
            self.inventory.extend([self.product for _ in range(quantity)])
        else:
            raise ValueError(
                f"Quantity {quantity} is greater than available capacity {self.capacity - len(self.inventory)}."
            )

    def distribute(self, user: Actor, quantity: Optional[int] = None) -> None:
        if quantity is None:
            consumer = Consumer(user)
            if consumer not in self.consumers:
                for _ in range(len(self.inventory)):
                    consumer.products.append(self.inventory.pop())
                self.consumers.append(consumer)
            else:
                for c in self.consumers:
                    if c.user is user:
                        for _ in range(len(self.inventory)):
                            consumer.products.append(self.inventory.pop())
        else:
            if isinstance(quantity, int):
                if quantity <= len(self.inventory):
                    consumer = Consumer(user)
                    if consumer not in self.consumers:
                        for _ in range(quantity):
                            consumer.products.append(self.inventory.pop())
                        self.consumers.append(consumer)
                    else:
                        for c in self.consumers:
                            if c.user is user:
                                for _ in range(quantity):
                                    consumer.products.append(self.inventory.pop())
                else:
                    raise ValueError(
                        f"Quantity {quantity} is greater than available quantity {len(self.inventory)}."
                    )
            else:
                raise TypeError(f"Quantity {quantity} is not an integer.")

    @property
    def label(self) -> str:
        return self._label

    @property
    def product(self) -> object:
        return self._product

    @property
    def product_kargs(self) -> dict:
        return self._product_kargs

    @property
    def production_rate(self) -> int:
        return self._production_rate

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def inventory(self) -> List:
        return self._inventory

    @property
    def consumers(self) -> List[Consumer]:
        return [consumer.user for consumer in self._consumers]

    @property
    def id(self):
        return self._id

    @property
    def priority(self):
        return self._priority

    @property
    def timeline(self):
        return self._timeline

    @property
    def time(self):
        return self._time

    @property
    def till(self):
        return self._till

    @property
    def step(self):
        return self._step

    @property
    def status(self):
        return self._status

    @property
    def after(self):
        return self._after

    @property
    def active(self):
        return "active" in self.status

    @property
    def inactive(self):
        return "inactive" in self.status

    @property
    def onhold(self):
        return "onhold" in self.status

    @property
    def completed(self):
        return "completed" in self.status

    @property
    def followers(self):
        return self._followers
