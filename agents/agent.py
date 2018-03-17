from ext import globals


class Agent():
    def __init__(self, strategy):
        self.id = globals.gAgentId
        globals.gAgentId += 1
        self.score = 0
        self.strategy = strategy # 0 : random, 1 : adaptive, etc...

    def flip(self):
        """
        Flip action
        :return:
        """
        self.updateScore()

    def updateScore(self):
        return 0
