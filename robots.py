from core.server import Server, Rabelais, Partie

class Robot(Server):
    def __init__(self):
        player1 = Rabelais('Barry Lyndon')
        player2 = Rabelais('Rabelais')
        self.players = {player1, player2}
        self.partie = Partie(player1, player2)

    def play_a_hand(self):
        d = self.partie.new_deal()
        # The deal
        self.announce('---')
        d.deal()
        self.exchange(d)
        self.declarations(d)
        self.tricks(d)
        print('\nDeal: {}'.format(d.score))
        print('Score: {}'.format(self.partie.score))
        return d.score

if __name__ == "__main__":

    r = Robot()
    r.play_a_game()
    print('\nWinner: {} with {}'.format(r.partie.winner, r.partie.final_score))