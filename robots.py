from core.server import Server, Rabelais, Partie


class Viewer(Rabelais):

    def announce(self, message):
        print(message)

    def register(self, player, card, silent=False):
        self.seen_cards[card.hash()] = card
        print('{} plays {}.'.format(player, card))


class Robot(Server):

    def __init__(self):
        player1 = Rabelais('Barry Lyndon')
        player2 = Viewer('Rabelais')
        self.players = {player1, player2}
        self.partie = Partie(player1, player2)

    def report(self, d):
        self.announce("{}:\n{}".format(d.elder, d.elder.print_hand()))
        self.announce("{}:\n{}".format(d.younger, d.younger.print_hand()))

    def play_a_hand(self):
        d = self.partie.new_deal()
        # The deal
        self.announce('---')
        d.deal()
        self.report(d)
        self.exchange(d)
        self.report(d)
        self.declarations(d)
        self.tricks(d)
        self.announce('\nDeal: {}'.format(d.score))
        input("...")
        return d.score

if __name__ == "__main__":

    r = Robot()
    r.play_a_game()
    print('\nWinner: {} with {}'.format(r.partie.winner, r.partie.final_score))
