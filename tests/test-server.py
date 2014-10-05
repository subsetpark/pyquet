from unittest import TestCase
from core.game import Partie
from core.server import Server
from core.players import Rabelais

class Robot(Server):
    def __init__(self):
        player1 = Rabelais('Barry Lyndon')
        player2 = Rabelais('Rabelais')
        self.players = {player1, player2}
        self.partie = Partie(player1, player2)

class TestServer(TestCase):
    def test_play_robots(self):
        for i in range(100):
            r = Robot()
            r.play_a_game()