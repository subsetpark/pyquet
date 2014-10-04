from unittest import TestCase
from pyquet import Deck, Deal, Player, Rank, Suit, Card
from pyquet.rabelais import Rabelais

def new_deal():
    p1 = Rabelais('Marcus')
    p2 = Rabelais('Vergil')
    return Deal(p1, p2)

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