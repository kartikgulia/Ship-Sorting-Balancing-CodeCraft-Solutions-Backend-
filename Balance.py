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

    # want to get lowest position we can place cargo in for a given column
    def lowestPosition(self, column):
        if (self.cargo_grid[1][column].name == "UNUSED"):
            return [1, column]
        cargo_column = [row[column] for row in self.cargo_grid]
        for x in cargo_column:
            if (x.name == "UNUSED"):
                return self.cargo_grid[x][column].position
        """
    def Balance(self):
        if(self.Balance_Check):
            self.CargoList() # if ship container is unbalanced, make a list of all containers on the heavier side
            for x in self.cargoList:                              
        else:
            return
        for x in range(len(self.cargo_grid)):
            if (x == 0):
                continue
            for y in range(len(self.cargo_grid[x])):
                if (y == 0):
                    continue
        """
