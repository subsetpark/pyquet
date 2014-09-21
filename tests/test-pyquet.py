from unittest import TestCase
from pyquet import Deck, Deal, Player, Rank, Suit, Card

def new_deal():
    p1 = Player('Marcus')
    p2 = Player('Vergil')
    return Deal(p1, p2)

class TestClasses(TestCase):
    def test_card(self):
        ace_diamonds = Card(Rank.Ace, Suit.DIAMONDS)
        king_clubs = Card(Rank.King, Suit.CLUBS)
        ace_clubs = Card(Rank.Ace, Suit.CLUBS)

        self.assertGreater(ace_diamonds, king_clubs)
        self.assertEquals(ace_diamonds, ace_clubs)
    def test_deck(self):
        d = Deck()
        self.assertEquals(len(d.cards), 32)
        self.assertEquals(len([c for c in d.cards if str(c) == 'Ace ♧']), 1)

    def test_point(self):
        p = Player('Marcus')
        p.hand = [
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
        ]

        point = p.point
        self.assertEquals(point[0], 4)
        self.assertEquals(point[1], 41)

        p.hand = [
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
        ]

        point = p.point
        self.assertEquals(point[0], 4)
        self.assertEquals(point[1], 37)

    def test_sequences(self):
        p = Player('Marcus')
        p.hand = [
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
        ]
        sequences = p.sequences
        run = [
            Card(Rank.Ten, Suit.HEARTS),
            Card(Rank.Jack, Suit.HEARTS),
            Card(Rank.Queen, Suit.HEARTS),
            Card(Rank.King, Suit.HEARTS),
        ]
        self.assertEquals(sequences[-1], run)

    def test_sets(self):
        p = Player('Marcus')
        p.hand = [
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
        ]
        sets = [[
            Card(Rank.King, Suit.HEARTS),
            Card(Rank.King, Suit.SPADES),
            Card(Rank.King, Suit.CLUBS)
            ],
            [
                Card(Rank.Queen, Suit.HEARTS),
                Card(Rank.Queen, Suit.SPADES),
                Card(Rank.Queen, Suit.DIAMONDS),
                Card(Rank.Queen, Suit.CLUBS),
            ]
        ]
        self.assertEquals(p.sets, sets)

    def test_deal(self):
        d = new_deal()

        d.deal()
        assert len(d.elder.hand) == len(d.younger.hand) == 12
        self.assertEquals(len(d.deck.cards), 8)

    def test_exchange(self):
        d = new_deal()

        d.deal()

        elder_exchange = d.elder.hand[0:5]

        d.exchange(d.elder, elder_exchange)

        younger_exchange = d.younger.hand[0:3]

        d.exchange(d.younger, younger_exchange)

        assert len(d.elder.hand) == len(d.younger.hand) == 12
        self.assertEquals(len(d.deck.cards), 0)
        self.assertEquals(len(d.elder.discards + d.younger.discards), 8)