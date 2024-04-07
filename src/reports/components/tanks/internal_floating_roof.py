from dataclasses import dataclass

from src.database.definitions.floating_roof_tank import InternalFloatingRoofTank


@dataclass
class InternalFloatingRoofTankShim:
    tank: InternalFloatingRoofTank

    def __getattr__(self, name):
        # Allow us to pretend like we are actually the tank
        # (Priority goes to the shim first and then the tank itself)
        if name in self.__dict__:
            return self[name]
        elif hasattr(self.tank, name):
            return getattr(self.tank, name)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __hash__(self) -> int:
        # Use the tank's id as our hash
        return self.tank.id
