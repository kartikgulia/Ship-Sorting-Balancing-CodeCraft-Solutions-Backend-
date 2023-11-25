from CargoGrid import Cargo_Grid


class Balance:

    starboardMass = 0
    portSideMass = 0
    cargoList = []

    def __init__(self, cargo_grid):
        self.cargo_grid = cargo_grid

    def Balance_Check(self):
        i = 0
        for x in range(len(self.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.cargo_grid[x])):
                if (y == 0):
                    continue
                if (y < 7):
                    self.portSideMass += self.cargo_grid[x][y].weight
                else:
                    self.starboardMass += self.cargo_grid[x][y].weight
                i += 1
        if (abs(self.starboardMass - self.portSideMass) <= (max(self.starboardMass, self.portSideMass) * 0.10)):
            return True
        else:
            return False

    # make a list of the cargo containers that belong to the side that is heavier. Easier to iterate
    def CargoList(self):
        for x in range(len(self.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.cargo_grid[x])):
                if (y == 0):
                    continue
                if (self.portSideMass > self.starboardMass):
                    if (y > 6):
                        continue
                    else:
                        if (self.cargo_grid[x][y].name != "NAN" and self.cargo_grid[x][y].name != "UNUSED"):
                            self.cargoList.append(self.cargo_grid[x][y])
                elif (self.portSideMass < self.starboardMass):
                    if (y < 7):
                        continue
                    else:
                        if (self.cargo_grid[x][y].name != "NAN" and self.cargo_grid[x][y].name != "UNUSED"):
                            self.cargoList.append(self.cargo_grid[x][y])

    def Balance(self):
        for x in range(len(self.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.cargo_grid[x])):
                if (y == 0):
                    continue
