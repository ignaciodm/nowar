from abc import ABC


# Create your models here.


class Army:
    pass

    @property
    def can_be_attacked(self) -> bool:
        """
            At this moment armies cannot be attacked, independtly of how they are configured.
            :return: whether the army can be attacked or not.
        """
        return False


class ArmyUnit(ABC):
    def __init__(self, life_amount: int, attacking_damage: int) -> None:
        self._life_amount = life_amount
        """
            How much life will an army unit have. Once it is less than 0, the army unit is considered dead
        """

        self._attacking_damage = attacking_damage
        """
            How much damage an army unit inflicts when attacking.
        """

    @property
    def can_be_attacked(self) -> bool:
        """
            At this moment an army unit can always be attacked.

            :return: whether the army can be attacked or not.
        """
        return True

    @property
    def is_alive(self) -> bool:
        return self._life_amount > 0.0


class Catapult(ArmyUnit):
    _LIFE = 50
    _ATTACKING_DAMAGE = 100

    def __init__(self):
        super().__init__(Catapult._LIFE, Catapult._ATTACKING_DAMAGE)


class EquippedArmyUnit(ArmyUnit):
    pass


class Knight(EquippedArmyUnit):
    _LIFE = 100
    _ATTACKING_DAMAGE = 20

    def __init__(self):
        super().__init__(Knight._LIFE, Knight._ATTACKING_DAMAGE)


class Archer(EquippedArmyUnit):
    _LIFE = 50
    _ATTACKING_DAMAGE = 25

    def __init__(self):
        super().__init__(Archer._LIFE, Archer._ATTACKING_DAMAGE)
