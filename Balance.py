from CargoGrid import Cargo_Grid


class Balance:
    def __init__(self, cargo_grid):
        self.cargo_grid = cargo_grid

    def Balance_Check(self):
        i = 0
        starboardMass = 0
        portSideMass = 0
        for x in range(len(self.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.cargo_grid[x])):
                if (y == 0):
                    continue
                if (y < 7):
                    portSideMass += self.cargo_grid[x][y].weight
                else:
                    starboardMass += self.cargo_grid[x][y].weight
                i += 1
        if (abs(starboardMass - portSideMass) <= (max(starboardMass, portSideMass) * 0.10)):
            return True
        else:
            return False
