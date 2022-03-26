from typing import Type, Union, Optional, List

import pytest

from war.models import Knight, Archer, Catapult, Army, Weapon
from war.tests.test_utils import make_dead_army_unit, make_army_unit


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
    "army_item, expected_can_be_attacked",
    [
        (Knight(), True),
        (Archer(), True),
        (Catapult(), True),
        (Army([]), False),
    ])
def test_army_item_can_be_attacked(
        army_item: Union[Knight, Archer, Catapult, Army], expected_can_be_attacked: bool):
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
    attacker = make_army_unit(attacker_class, weapon)
    target = make_army_unit(target_class)

    attacker.attack(target)

    assert target.is_dead == expected_target_is_dead


@pytest.mark.parametrize(
    "troops, expected_attacking_damage",
    [
        #
        # Armies of mixed army units of 2
        #
        ([Knight(), Knight()], 40),
        ([Knight(Weapon(10)), Knight()], 50),
        ([Knight(Weapon(10)), Archer()], 55),
        ([Knight(Weapon(10)), Catapult()], 80),

        #
        # Army of with dead units does not sum to attacking power
        #
        ([Knight(), Knight(), make_dead_army_unit()], 40),
        ([Knight(Weapon(10)), Knight(), make_dead_army_unit()], 50),
        ([Knight(Weapon(10)), Archer(), make_dead_army_unit()], 55),
        ([Knight(Weapon(10)), Catapult(), make_dead_army_unit()], 80),

        #
        # A nested army
        #
        (
                [Knight(), Archer(), Catapult(), Army([Knight(), Archer()])],
                20 + 25 + 50 + 20 + 25
        ),
        (
                [Knight(), Archer(), Catapult(), Army([Knight(), Archer(), Army([Knight(), Archer()])])],
                20 + 25 + 50 + 20 + 25 + 20 + 25
        ),
    ])
def test_army_total_attacking_damage(
        troops: List[Union[Knight, Archer, Catapult]], expected_attacking_damage: float):
    army = ArmyBuilder().with_troops(troops).build()

    assert army.attacking_damage() == expected_attacking_damage


def test_army_unit_cannot_attack_if_dead():
    with pytest.raises(RuntimeError):
        make_dead_army_unit().attack(make_army_unit(Archer))
