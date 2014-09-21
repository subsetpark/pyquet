from enum import Enum
from random import shuffle, choice

class Rank(Enum):
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

PIPS = {
    Rank.Seven: 7,
    Rank.Eight: 8,
    Rank.Nine: 9,
    Rank.Ten: 10,
    Rank.Jack: 10,
    Rank.Queen: 10,
    Rank.King: 10,
    Rank.Ace: 11
}

class Suit:
    DIAMONDS = '♢'
    HEARTS = '♡'
    SPADES = '♤'
    CLUBS = '♧'
    suits = [DIAMONDS, HEARTS, SPADES, CLUBS]

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return "{}{}".format(self.rank.name, self.suit.capitalize())

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.rank.value < other.rank.value

    def __eq__(self, other):
        return self.rank.value == other.rank.value

    def __sub__(self, other):
        return self.rank.value - other.rank.value

    def hash(self):
        CHARMAP = {
            Rank.Seven: '7',
            Rank.Eight: '8',
            Rank.Nine: '9',
            Rank.Ten: 'T',
            Rank.Jack: 'J',
            Rank.Queen: 'Q',
            Rank.King: 'K',
            Rank.Ace: 'A',
            Suit.DIAMONDS: 'D',
            Suit.HEARTS: 'H',
            Suit.SPADES: 'S',
            Suit.CLUBS: 'C'
        }
        return '{}{}'.format(CHARMAP[self.rank], CHARMAP[self.suit])

class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for r in Rank for s in Suit.suits]
        shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

    def pop(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.hand = {}
        self.name = name
        self.discards = []

        self.score = 0
        self.deal_score = None

    def __repr__(self):
        return 'Player: {}'.format(self.name)

    def suits(self):
        return sorted([[c for c in self.hand.values() if c.suit == s] for s in Suit.suits], 
                      key=len)

    def print_hand(self):
        cards = sorted(self.hand.values(), key=lambda c: (c.suit, c.rank.value))
        return " | ".join([str(c) for c in cards])

    def discard(self, cards):
        for card in cards:
            del self.hand[card.hash()]
            self.discards.append(card)

    def draw(self, cards):
        for card in cards:
            self.hand[card.hash()] = card

    @property
    def point(self):
        """
        A player may declare for point if they have 4 or more cards in one suit.
        Whoever has the longest point wins. If two players have the same value 
        for point, then the player with the highest value point wins.
        """
        suits = self.suits()

        max_length = len(suits[-1])
        
        if max_length < 4:
            return None

        point_suits = [suit for suit in suits if len(suit) == max_length]

        point_pips = [sum([PIPS[c.rank] for c in point_suit]) for point_suit in point_suits]
        max_points = max(point_pips)
        point_suit = point_suits[point_pips.index(max_points)]
        point_length = len(point_suit)
    
        return (point_length, max_points)

    @property
    def sequences(self):
        suits = self.suits()
        sequences = []
        for suit in suits:
            longest_sequence = []
            suit.sort()
            i = 0
            runner = 1

            while i < len(suit):
                run = [suit[i]]
                while runner < len(suit):
                    card = suit[runner - 1]
                    next_card = suit[runner]
                    if next_card - card == 1:
                        runner = runner + 1
                        run.append(next_card)
                    else:          
                        break

                if len(run) > len(longest_sequence):
                    longest_sequence = run

                i = runner
                runner = i + 1
                
            sequences.append(longest_sequence)

        return sorted([sequence for sequence in sequences if len(sequence) >= 3],
                      key=len)

    @property
    def sets(self):
        ELIGIBLE_RANKS = [
            Rank.Ace,
            Rank.King,
            Rank.Queen,
            Rank.Jack,
            Rank.Ten
        ]
        return sorted([l for l in 
                       [[c for c in self.hand.values() if c.rank == r] 
                           for r in ELIGIBLE_RANKS] 
                        if len(l) >= 3],
                      key=lambda l: (len(l), l[0].rank))


class Deal:
    def __init__(self, elder, younger):
        self.deck = Deck()
        self.elder = elder
        self.younger = younger

    def get_cards(self, message, player, max_cards=1):
        card_str = input("Your hand: {}\n{}".format(player.print_hand(), message))
        cards = card_str.split()
        return [player.hand[chars] for chars in cards]

    def deal(self):
        for i in range(12):
            self.elder.draw([self.deck.pop()])
            self.younger.draw([self.deck.pop()])

    def exchange(self, player, cards):
        player.discard(cards)
        for i in cards:
            player.draw([self.deck.pop()])

class Partie:
    def __init__(self, player1_name, player2_name):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.deals = []

    def play(self):
        players = {self.player1, self.player2}
        dealer = random.choice(list(players))
        non_dealer = players - {dealer}