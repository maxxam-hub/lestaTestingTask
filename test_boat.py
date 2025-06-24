import pytest
from boat import Boat, Passenger

def test_install_oars():
    boat = Boat()
    for oar in boat.oars:
        oar.install()
    assert all(oar.installed for oar in boat.oars)

def test_anchor_behavior():
    boat = Boat()
    boat.anchor.drop()
    assert boat.anchor.lowered is True
    boat.anchor.raise_up()
    assert boat.anchor.lowered is False

def test_single_passenger_under_400kg():
    boat = Boat()
    assert boat.add_passenger(Passenger("P1", 70)) is True

def test_five_passengers_total_weight_under_limit():
    boat = Boat()
    for i in range(5):
        assert boat.add_passenger(Passenger(f"P{i}", 75)) is True
    assert boat.get_total_weight() == 375


def test_six_passengers_not_allowed():
    boat = Boat()
    for i in range(5):
        assert boat.add_passenger(Passenger(f"P{i}", 70)) is True
    assert boat.add_passenger(Passenger("P5", 70)) is False


def test_five_passengers_over_400kg():
    boat = Boat()
    for i in range(5):
        assert boat.add_passenger(Passenger(f"P{i}", 85)) is True if i < 4 else False


def test_empty_boat_stable():
    boat = Boat()
    assert boat.place_on_water() is True


def test_remove_oars():
    boat = Boat()
    for oar in boat.oars:
        oar.install()
    for oar in boat.oars:
        oar.remove()
    assert not any(oar.installed for oar in boat.oars)


def test_storage_limit():
    boat = Boat()
    assert boat.storage.load(50.0) is True
    assert boat.storage.load(1.0) is False


def test_place_on_water_in_salt_and_waves():
    boat = Boat()
    boat.add_passenger(Passenger("P1", 70))
    assert boat.place_on_water(salt=True, waves=0.4) is True


def test_exceed_wave_height():
    boat = Boat()
    boat.add_passenger(Passenger("P1", 70))
    assert boat.place_on_water(waves=0.6) is False


def test_trailer_attachment():
    boat = Boat()
    assert boat.attach_to_trailer() is True
    assert boat.on_trailer is True


def test_no_oars_no_movement():
    boat = Boat()
    boat.anchor.raise_up()
    assert not boat.move_forward()


def test_forward_movement():
    boat = Boat()
    for oar in boat.oars:
        oar.install()
    boat.anchor.raise_up()
    assert boat.move_forward() is True


def test_rotation_logic():
    boat = Boat()
    boat.anchor.raise_up()
    assert boat.rotate("left") == "rotating right"
    assert boat.rotate("right") == "rotating left"
    boat.anchor.drop()
    assert boat.rotate("left") == "cannot rotate while anchored"


def test_stability_with_storage_and_passengers():
    boat = Boat()
    for i in range(5):
        assert boat.add_passenger(Passenger(f"P{i}", 70)) is True
    assert boat.storage.load(50.0) is True
    assert boat.place_on_water() is True


def test_instability_with_excess_storage():
    boat = Boat()
    for i in range(5):
        assert boat.add_passenger(Passenger(f"P{i}", 70)) is True
    assert boat.storage.load(51.0) is False
    assert boat.place_on_water() is True


def test_instability_with_excess_weight():
    boat = Boat()
    for i in range(5):
        assert boat.add_passenger(Passenger(f"P{i}", 80)) is True
    assert boat.storage.load(1.0) is False
    assert boat.place_on_water() is False