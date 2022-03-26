from typing import Type, Union, Optional

import pytest

from war.models import Knight, Archer, Catapult, Army, Weapon, ArmyUnit


class TestArmyUnit(ArmyUnit):
    """
        An army unit used for testing
    """

    def attacking_damage(self) -> float:
        return self._default_attacking_damage


def make_dead_army_unit() -> ArmyUnit:
    return TestArmyUnit(-10, 10)


def make_army_unit(attacker_class, weapon=None):
    if weapon:
        return attacker_class(weapon)
    else:
        return attacker_class()
