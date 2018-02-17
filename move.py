class Move:
    def __init__(self, x, y, x1, y1):
        self.start = (x, y)
        self.end = (x1, y1)

    def __str__(self):
        return "("+str(self.start)+", "+str(self.end)+")"
