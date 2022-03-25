from typing import Type, Union

import pytest


from war.models import Knight, ArmyUnit, Archer, Catapult, Army


@pytest.mark.parametrize(
    "klass, expected_is_alive",
    [
        (Knight, True),
        (Archer, True),
        (Catapult, True),
    ])
def test_an_army_unit_alive_when_created(klass: Type[Union[Knight, Archer, Catapult]], expected_is_alive: bool):
    army_unit = klass()

    assert army_unit.is_alive == expected_is_alive


@pytest.mark.parametrize(
    "klass, expected_can_be_attacked",
    [
        (Knight, True),
        (Archer, True),
        (Catapult, True),
        (Army, False),
    ])
def test_army_item_can_be_attacked(klass: Type[Union[Knight, Archer, Catapult, Army]], expected_can_be_attacked: bool):
    army_item = klass()

    assert army_item.can_be_attacked == expected_can_be_attacked
