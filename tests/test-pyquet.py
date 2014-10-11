from unittest import TestCase
from core.game import Partie, Deck, Deal, Rank, Suit, Card, all_cards, Result, Category
from core.players import Rabelais

def new_deal():
    p1 = Rabelais('Marcus')
    p2 = Rabelais('Vergil')
    p = Partie(p1, p2)
    return Deal(p, p1, p2)

class TestClasses(TestCase):
    def test_card(self):
        ace_diamonds = Card(Rank.Ace, Suit.DIAMONDS)
        king_clubs = Card(Rank.King, Suit.CLUBS)
        ace_clubs = Card(Rank.Ace, Suit.CLUBS)

        self.assertGreater(ace_diamonds, king_clubs)
        self.assertEquals(ace_diamonds, ace_clubs)

    def test_deck(self):
        d = Deck(all_cards())
        self.assertEquals(len(d.cards), 32)
        self.assertEquals(len([c for c in d.cards if str(c) == 'Ace♧']), 1)

    def test_print_hand(self):
        d = new_deal()
        self.assertEquals(len(d.pool), 32)
        d.deal()
        self.assertEquals(len(d.pool), 32)

    def test_point(self):
        d = new_deal()
        p = d.elder
        p.draw([
            Card(Rank.Jack, Suit.HEARTS),
            Card(Rank.Ten, Suit.HEARTS),
            Card(Rank.King, Suit.HEARTS),
            Card(Rank.Ace, Suit.HEARTS),

            Card(Rank.Queen, Suit.SPADES),
            Card(Rank.Seven, Suit.SPADES),
            Card(Rank.Ace, Suit.SPADES),

            Card(Rank.Nine, Suit.DIAMONDS),
            Card(Rank.Ten, Suit.DIAMONDS),

            Card(Rank.Queen, Suit.CLUBS),
            Card(Rank.Eight, Suit.CLUBS),
            Card(Rank.Jack, Suit.CLUBS),
        ])

        point = p.point
        self.assertEquals(point.first, 4)
        self.assertEquals(point.second, 41)

        d = new_deal()
        p = d.elder
        p.draw([
            Card(Rank.Seven, Suit.HEARTS),
            Card(Rank.Ten, Suit.HEARTS),
            Card(Rank.King, Suit.HEARTS),
            Card(Rank.Eight, Suit.HEARTS),

            Card(Rank.Queen, Suit.SPADES),
            Card(Rank.Seven, Suit.SPADES),
            Card(Rank.Ace, Suit.SPADES),
            Card(Rank.Nine, Suit.SPADES),

            Card(Rank.Ten, Suit.DIAMONDS),

            Card(Rank.Queen, Suit.CLUBS),
            Card(Rank.Eight, Suit.CLUBS),
            Card(Rank.Jack, Suit.CLUBS),
        ])

        point = p.point
        self.assertEquals(point.first, 4)
        self.assertEquals(point.second, 37)

    def test_sequences(self):
        d = new_deal()
        p = d.elder
        p.draw([
            Card(Rank.Jack, Suit.HEARTS),
            Card(Rank.Ten, Suit.HEARTS),
            Card(Rank.King, Suit.HEARTS),
            Card(Rank.Queen, Suit.HEARTS),

            Card(Rank.Queen, Suit.SPADES),
            Card(Rank.Seven, Suit.SPADES),
            Card(Rank.Ace, Suit.SPADES),

            Card(Rank.Nine, Suit.DIAMONDS),
            Card(Rank.Ten, Suit.DIAMONDS),

            Card(Rank.Queen, Suit.CLUBS),
            Card(Rank.Eight, Suit.CLUBS),
            Card(Rank.Jack, Suit.CLUBS),
        ])
        run = [
            Card(Rank.Ten, Suit.HEARTS),
            Card(Rank.Jack, Suit.HEARTS),
            Card(Rank.Queen, Suit.HEARTS),
            Card(Rank.King, Suit.HEARTS),
        ]
        self.assertEquals(p.sequences, Result(p, Category.SEQUENCES, 4, [run]))

    def test_sets(self):
        d = new_deal()
        p = d.elder
        p.draw([
            Card(Rank.Jack, Suit.HEARTS),
            Card(Rank.Ten, Suit.HEARTS),
            Card(Rank.King, Suit.HEARTS),
            Card(Rank.Queen, Suit.HEARTS),

            Card(Rank.Queen, Suit.SPADES),
            Card(Rank.Seven, Suit.SPADES),
            Card(Rank.King, Suit.SPADES),

            Card(Rank.Nine, Suit.DIAMONDS),
            Card(Rank.Queen, Suit.DIAMONDS),

            Card(Rank.Queen, Suit.CLUBS),
            Card(Rank.Eight, Suit.CLUBS),
            Card(Rank.King, Suit.CLUBS),
        ])
        sets = [
            [
                Card(Rank.Queen, Suit.DIAMONDS),
                Card(Rank.Queen, Suit.HEARTS),
                Card(Rank.Queen, Suit.SPADES),
                Card(Rank.Queen, Suit.CLUBS),
            ],[
                Card(Rank.King, Suit.HEARTS),
                Card(Rank.King, Suit.SPADES),
                Card(Rank.King, Suit.CLUBS)
            ]
        ]
        self.assertEquals(p.sets, Result(p, Category.SETS, 4, sets))

    def test_deal_deal(self):
        d = new_deal()

        d.deal()
        assert len(d.elder.hand) == len(d.younger.hand) == 12
        self.assertEquals(len(d.deck.cards), 8)

    def test_exchange(self):
        d = new_deal()

        d.deal()

        elder_exchange = list(d.elder.hand.values())[0:5]

        d.exchange(d.elder, elder_exchange)

        younger_exchange = list(d.younger.hand.values())[0:3]

        d.exchange(d.younger, younger_exchange)

        assert len(d.elder.hand) == len(d.younger.hand) == 12
        self.assertEquals(len(d.deck.cards), 0)
        self.assertEquals(len(d.discards[d.elder] + d.discards[d.younger]), 8)

    def test_hand_evaluator(self):
        d = new_deal()
        d.deal()
        print(d.elder.print_hand())
        print(d.elder.evaluate_hand())