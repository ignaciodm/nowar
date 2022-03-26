from typing import Type, Union, Optional

import pytest

from war.models import Knight, Archer, Catapult, Army, Weapon


@pytest.mark.parametrize(
    "klass, expected_is_alive",
    [
        (Knight, True),
        (Archer, True),
        (Catapult, True),
    ])
def test_an_army_unit_is_alive_when_created(klass: Type[Union[Knight, Archer, Catapult]], expected_is_alive: bool):
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


@pytest.mark.parametrize(
    "attacker_class, weapon, target_class, expected_target_is_dead",
    [
        # knight attack knight
        (Knight, None, Knight, False),
        (Knight, Weapon(79.9), Knight, False),
        (Knight, Weapon(80.1), Knight, True),

        # knight attack archer
        (Knight, None, Archer, False),
        (Knight, Weapon(29.9), Archer, False),
        (Knight, Weapon(30.1), Archer, True),

        # knight attach catapult
        (Knight, None, Catapult, False),
        (Knight, Weapon(179.9), Catapult, False),
        (Knight, Weapon(180.1), Catapult, True),

        # archer attack archer
        (Archer, None, Archer, False),
        (Archer, Weapon(24.9), Archer, False),
        (Archer, Weapon(25.1), Archer, True),

        # archer attack knight
        (Archer, None, Knight, False),
        (Archer, Weapon(74.9), Knight, False),
        (Archer, Weapon(75.1), Knight, True),

        # knight attach catapult
        (Archer, None, Catapult, False),
        (Archer, Weapon(174.9), Catapult, False),
        (Archer, Weapon(175.1), Catapult, True),

        # catapult attack catapult
        (Catapult, None, Catapult, False),

        # catapult attack knight
        (Catapult, None, Knight, False),

        # catapult attack archer
        (Catapult, None, Archer, True),
    ])
def test_army_unit_attack_army_unit(
        attacker_class: Type[Union[Knight, Archer, Catapult, Army]],
        weapon: Optional[Weapon],
        target_class: Type[Union[Knight, Archer, Catapult, Army]],
        expected_target_is_dead: bool):
    attacker = _make_army_unit(attacker_class, weapon)
    target = _make_army_unit(target_class)

    target.attacked_by(attacker)

    assert target.is_dead == expected_target_is_dead


def _make_army_unit(attacker_class, weapon = None):
    if weapon:
        return attacker_class(weapon)
    else:
        return attacker_class()
