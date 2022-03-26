from abc import ABC, abstractmethod, abstractproperty

# Create your models here.
from typing import Optional, Union, List


class ArmyBase(ABC):

    @property
    def can_be_attacked(self) -> bool:
        pass

    @abstractmethod
    def attacking_damage(self) -> float:
        pass

    @property
    def is_alive(self) -> bool:
        pass

    def attack(self, target: 'ArmyUnit'):
        if self.is_alive:
            if target.can_be_attacked:
                target.attacked_with(self.attacking_damage())
            else:
                raise RuntimeError('Army base cannot be attacked')

        else:
            raise RuntimeError('A dead army item cannot attack')


class Army(ArmyBase):
    def __init__(self, troops: List[Union['Army', 'ArmyUnit']]) -> None:
        self._troops = troops

    @property
    def can_be_attacked(self) -> bool:
        """
            At this moment armies cannot be attacked_by, independently of how they are configured.
            :return: whether the army can be attacked_by or not.
        """
        return False

    def attacking_damage(self) -> float:
        return sum([troop.attacking_damage() if troop.is_alive else 0 for troop in self._troops])

    @property
    def is_alive(self) -> bool:
        return any([troop.is_alive for troop in self._troops])


class ArmyUnit(ArmyBase, ABC):
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

    def attacked_with(self, damage: float):
        self._life_amount = self._life_amount - damage

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
    _ATTACKING_DAMAGE = 50

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


class ArmyBuilder:
    """
        A place to abstract how to build armies. Too much for the current use case, but as the complexity of the
        army creation changes, it could be useful.
    """

    def __init__(self):
        self._troops = []

    def with_troops(self, troops: List) -> 'ArmyBuilder':
        for troop in troops:
            self._troops.append(troop)

        return self

    def build(self) -> Army:
        return Army(self._troops)
