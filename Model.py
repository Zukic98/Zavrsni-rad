class ModelSample:
    name = None
    number = None
    Peclet = None
    R = None
    polygon = None

    def __init__(self):
        pass
    def run(self):
        if self.name == "" or self.number == "" or self.Peclet == "" or self.R == "" or self.polygon == None:
            raise ValueError("You need to fill all the fields and set the polygon to start the simulation")
        if not self.number.isnumeric():
            raise ValueError("Error: Number of penguins must be natural number!")
        if not self.Peclet.isnumeric():
            raise ValueError("Error: Peclet's number must be natural number!")
        if not self.R.isnumeric():
            raise ValueError("Error: R must be natural number!")

