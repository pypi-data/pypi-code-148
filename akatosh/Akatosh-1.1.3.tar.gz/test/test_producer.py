from Akatosh import Actor, Producer, Mundus


class Milk(Actor):
    def __init__(
        self,
        expiration_time: int,
        **kwargs,
    ) -> None:
        super().__init__(step=1, priority=1, **kwargs)
        self._expiration_time = expiration_time
        self._life_time = 0
        self._expired = False

    def action(self):
        self._life_time += 1
        if self.expired is False:
            if self._life_time > self._expiration_time:
                self._expired = True
                print(f"Time {self.timeline.now}\tMilk {self.id} has expired.")

    @property
    def expired(self) -> bool:
        return self._expired

    @property
    def expiration_time(self) -> int:
        return self._expiration_time


class MilkFarm(Producer):
    def __init__(
        self,
        production_cycle: int = 1,
        num_of_bottles: int = 1,
        **kwargs,
    ) -> None:
        super().__init__(
            product=Milk,
            prodction_rate=num_of_bottles,
            step=production_cycle,
            product_kargs={"expiration_time": 3},
            priority=0,
            label="Milk Farm",
            **kwargs,
        )


class Client(Actor):
    def __init__(
        self,
        restock_period: int = 1,
        restock_quantity: int = 50,
        farm: MilkFarm = None,
        **kwargs,
    ) -> None:
        super().__init__(step=restock_period, priority=2, **kwargs)
        self._restock_quantity = restock_quantity
        self._farm = farm

    def action(self):
        stock = 0
        while stock < self.restock_quantity:
            try:
                self.consume(self._farm, 1)
                stock += 1
            except Exception as e:
                break
        print(
            f"Time {self.timeline.now}\tClient {self.id} has restocked {stock} bottles of milk."
        )

    @property
    def restock_quantity(self) -> int:
        return self._restock_quantity


farm = MilkFarm(1, 10)
client = Client(3, 50, farm)


Mundus.simulate(20)
