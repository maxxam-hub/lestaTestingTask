from typing import List

class Oar:
    def __init__(self, side: str):
        self.side = side
        self.installed = False
        self.angle = 0

    def install(self):
        self.installed = True

    def remove(self):
        self.installed = False

    def rotate(self, degrees: int):
        if -90 <= degrees <= 90:
            self.angle = degrees
        else:
            raise ValueError("Oar rotation exceeds 180° range")


class Anchor:
    def __init__(self):
        self.lowered = False

    def drop(self):
        self.lowered = True

    def raise_up(self):
        self.lowered = False


class Passenger:
    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight


class Bench:
    def __init__(self, capacity: int = 2):
        self.passengers: List[Passenger] = []
        self.capacity = capacity

    def sit(self, passenger: Passenger) -> bool:
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            return True
        return False


class Storage:
    def __init__(self, max_weight: float):
        self.max_weight = max_weight
        self.current_weight = 0.0

    def load(self, weight: float) -> bool:
        if self.current_weight + weight <= self.max_weight:
            self.current_weight += weight
            return True
        return False


class Boat:
    MAX_PASSENGERS = 5
    MAX_TOTAL_WEIGHT = 400.0

    def __init__(self):
        self.oars = [Oar("left"), Oar("right")]
        self.anchor = Anchor()
        self.benches = [Bench() for _ in range(3)]
        self.storage = Storage(max_weight=50.0)
        self.passengers: List[Passenger] = []
        self.in_water = False
        self.on_trailer = False

    def get_total_weight(self) -> float:
        return sum(p.weight for p in self.passengers) + self.storage.current_weight

    def can_add_passenger(self, passenger: Passenger) -> bool:
        if len(self.passengers) >= self.MAX_PASSENGERS:
            return False
        if self.get_total_weight() + passenger.weight > self.MAX_TOTAL_WEIGHT:
            return False
        return True

    def add_passenger(self, passenger: Passenger) -> bool:
        if not self.can_add_passenger(passenger):
            return False
        for bench in self.benches:
            if bench.sit(passenger):
                self.passengers.append(passenger)
                return True
        return False

    def place_on_water(self, salt: bool = False, waves: float = 0.0) -> bool:
        self.in_water = True
        if len(self.passengers) <= self.MAX_PASSENGERS and self.get_total_weight() <= self.MAX_TOTAL_WEIGHT and waves <= 0.5:
            return True
        return False

    def attach_to_trailer(self) -> bool:
        self.on_trailer = True
        return True

    def move_forward(self) -> bool:
        return not self.anchor.lowered and all(oar.installed for oar in self.oars)

    def move_backward(self) -> bool:
        return self.move_forward()

    def rotate(self, side: str) -> str:
        if self.anchor.lowered:
            return "cannot rotate while anchored"
        return f"rotating {'right' if side == 'left' else 'left'}"