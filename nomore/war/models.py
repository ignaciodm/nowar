from abc import ABC, abstractmethod

# Create your models here.
from typing import Optional


class Army:
    pass

    @property
    def can_be_attacked(self) -> bool:
        """
            At this moment armies cannot be attacked_by, independently of how they are configured.
            :return: whether the army can be attacked_by or not.
        """
        return False


class ArmyUnit(ABC):
    def __init__(self, life_amount: int, attacking_damage: int) -> None:
        self._life_amount = life_amount
        """
            How much life will an army unit have. Once it is less than 0, the army unit is considered dead
        """

        self._default_attacking_damage = attacking_damage
        """
            How much damage an army unit inflicts when attacking.
        """

    @property
    def can_be_attacked(self) -> bool:
        """
            At this moment an army unit can always be attacked_by.

            :return: whether the army can be attacked_by or not.
        """
        return True

    def attacked_by(self, attacker: 'ArmyUnit'):
        self._life_amount = self._life_amount - attacker.attacking_damage()

    @property
    def is_dead(self) -> bool:
        return not self.is_alive

    @property
    def is_alive(self) -> bool:
        return self._life_amount > 0.0

    @abstractmethod
    def attacking_damage(self) -> float:
        pass


class Catapult(ArmyUnit):
    _LIFE = 200
    _ATTACKING_DAMAGE = 100

    def __init__(self):
        super().__init__(Catapult._LIFE, Catapult._ATTACKING_DAMAGE)

    def attacking_damage(self) -> float:
        return self._default_attacking_damage


class EquippedArmyUnit(ArmyUnit):

    def __init__(self, life_amount: int, attacking_damage: int, weapon: Optional['Weapon'] = None):
        super().__init__(life_amount, attacking_damage)

        self._weapon = weapon

    @property
    def weapon(self) -> Optional['Weapon']:
        return self._weapon

    @weapon.setter
    def weapon(self, weapon: Optional['Weapon']):
        self._weapon = weapon

    def attacking_damage(self) -> float:
        return self._default_attacking_damage + self.weapon.attacking_damage \
            if self._weapon else self._default_attacking_damage


class Knight(EquippedArmyUnit):
    _LIFE = 100
    _ATTACKING_DAMAGE = 20

    def __init__(self, weapon: Optional['Weapon'] = None):
        super().__init__(Knight._LIFE, Knight._ATTACKING_DAMAGE, weapon)


class Archer(EquippedArmyUnit):
    _LIFE = 50
    _ATTACKING_DAMAGE = 25

    def __init__(self, weapon: Optional['Weapon'] = None):
        super().__init__(Archer._LIFE, Archer._ATTACKING_DAMAGE, weapon)


class Weapon:
    def __init__(self, attacking_damage: float) -> None:
        self._attacking_damage = attacking_damage

    @property
    def attacking_damage(self) -> float:
        return self._attacking_damage
