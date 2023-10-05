class ModelSample:
    def __init__(self):
        self.name = None
        self.number = None
        self.Peclet = None
        self.R = None
        self.polygon = None

    def run(self):
        if self.name == "" or self.number == "" or self.Peclet == "" or self.R == "" or self.polygon == None:
            raise Exception
