from unittest import TestCase
from pyquet.game import Deck, Deal, Player, Rank, Suit, Card, Partie
from pyquet.players import Rabelais

def new_deal():
    p1 = Rabelais('Marcus')
    p2 = Rabelais('Vergil')
    p = Partie(p1, p2)
    return Deal(p, p1, p2)

class TestRabelais(TestCase):
    def test_get_elder_exchange(self):
        d = new_deal()
        d.deal()
        r = d.elder
        exchange = r.get_elder_exchange()
        print('{} from {}'.format(exchange, r.print_hand()))
        self.assertEquals(exchange[0].__class__, Card)
        d.exchange(r, exchange)

        r = d.younger
        exchange = r.get_younger_exchange(max_cards=3)
        print('{} from {}'.format(exchange, r.print_hand()))
        d.exchange(r, exchange)