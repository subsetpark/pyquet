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

class Declaration:
    GOOD = 'good'
    EQUAL = 'equal'
    NOT_GOOD = 'not good'

class Category:
    POINT = 'point'
    SEQUENCES = 'sequences'
    SETS = 'sets'
    categories = [POINT, SEQUENCES, SETS]

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

    def __hash__(self):
        return hash(self.hash())

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

    def __repr__(self):
        return '{}'.format(self.name)

    def suits(self):
        return sorted([
               sorted([c for c in self.hand.values() if c.suit == s], key=lambda x:x.rank.value) 
                      for s in Suit.suits], key=len)

    def print_hand(self):
        cards = sorted(self.hand.values(), key=lambda c: (c.suit, c.rank.value))
        return " | ".join([str(c) for c in cards])
        

    class Result:
        def __init__(self, player, score, value):
            self.player = player
            self.score = score
            self.value = value

        def __lt__(self, other):
            return (self.score, self.value) < (other.score, other.value)

        def __eq__(self, other):
            return (self.score, self.value) == (other.score, other.value)

        def __repr__(self):
            return 'Result: {} with {}, {}'.format(self.player, self.score, self.value)

    @property
    def carte_blanche(self):
        courts = {Rank.Jack, Rank.Queen, Rank.King}
        return not [card for card in self.hand.values() if card.rank in courts]

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
            return self.Result(self, 0, 0)

        point_suits = [suit for suit in suits if len(suit) == max_length]

        point_pips = [sum([PIPS[c.rank] for c in point_suit]) for point_suit in point_suits]
        max_points = max(point_pips)
        point_suit = point_suits[point_pips.index(max_points)]
        point_length = len(point_suit)
    
        return self.Result(self, point_length, max_points)

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

        sequences = sorted([sequence for sequence in sequences if len(sequence) >= 3],
                            key=lambda l: (-len(l), -l[0].rank.value))
        max_length = len(sequences[0]) if sequences else 0
        return self.Result(self, max_length, sequences)

    @property
    def sets(self):
        ELIGIBLE_RANKS = [
            Rank.Ace,
            Rank.King,
            Rank.Queen,
            Rank.Jack,
            Rank.Ten
        ]
        sets = sorted([l for l in 
                       [[c for c in self.hand.values() if c.rank == r] 
                           for r in ELIGIBLE_RANKS] 
                        if len(l) >= 3],
                      key=lambda l: (-len(l), -l[0].rank.value))
        set_class = len(sets[0]) if sets else 0
        return self.Result(self, set_class, sets)


class Deal:
    def __init__(self, partie, elder, younger):
        self.partie = partie
        self.deck = Deck()
        self.elder = elder
        self.younger = younger
        self.players = {self.elder, self.younger}
        self.score = {self.elder: 0, self.younger: 0}
        self.tricks = {self.elder: 0, self.younger: 0}
        self.discards = {self.elder: [], self.younger: []}
        self.repique = None
        self.pique = None
 

    def deal(self):
        self.elder.hand = {}
        self.younger.hand = {}

        for i in range(12):
            self.elder.draw([self.deck.pop()])
            self.younger.draw([self.deck.pop()])
        for player in self.players:
            if player.carte_blanche:
                self.score[player] += 10
                break

    def exchange(self, player, cards):
        for card in cards:
            del player.hand[card.hash()]
            self.discards[player].append(card)
            player.draw([self.deck.pop()])

    def score_declarations(self):
        score_values = {
            Category.POINT: {
                4: 4,
                5: 5,
                6: 6,
                7: 7,
                8: 8
            },
            Category.SEQUENCES: {
                3: 3,
                4: 4,
                5: 15,
                6: 16,
                7: 17,
                8: 18
            },
            Category.SETS: {
                3: 3,
                4: 14
            }
        }
        for category in (Category.POINT, Category.SEQUENCES, Category.SETS):
            winning_score = max([getattr(player, category) for player in self.players])
            winner = winning_score.player
            if category == Category.POINT:
                self.score[winner] += score_values[category][winning_score.score]
            else:
                self.score[winner] += sum([score_values[category][len(value)] for value in winning_score.value])
        # Repique
        for player in self.players:
            other_player = (self.players - {player}).pop()
            if self.score[player] >= 30 and self.score[other_player] == 0:
                self.repique = player
                self.score[player] += 60

    def play_trick(self, lead_play, follow_play):
        lead_card = lead_play['card']
        follow_card = follow_play['card']
        lead_player = lead_play['player']
        follow_player = follow_play['player']

        del lead_player.hand[lead_card.hash()]
        del follow_player.hand[follow_card.hash()]

        result = {'caput': None}

        self.score[lead_player] += 1

        if follow_card.suit == lead_card.suit and follow_card.rank.value > lead_card.rank.value:
            self.score[follow_player] += 1
            winner = follow_player
            loser = lead_player
        else:
            winner = lead_player
            loser = follow_player

        if not self.repique and not self.pique:
            if self.score[winner] >= 30 and self.score[loser] == 0:
                self.score[winner] += 30
                self.pique = winner

        if not lead_player.hand:
            self.score[winner] += 1

            if self.tricks[winner] == 12: # If winner has taken all the tricks
                self.score[winner] += 40
                result['caput'] = winner

            elif self.tricks[winner] == 6: # If winner (and thus both) have taken half the tricks
                most_tricks_player = max(self.tricks.items(), key=lambda x: x[1])
                self.score[most_tricks_player[0]] += 10

        self.tricks[winner] += 1
        result['winner'] = winner

        for player in self.players:
            self.partie.score[player] += self.score[player]
        return result

class Partie:
    def __init__(self, player1, player2):
        players = {player1, player2}
        self.dealer = choice(list(players))
        self.non_dealer = (players - {self.dealer}).pop()
        self.deals = []
        self.score = {player1: 0, player2: 0}

    def new_deal(self):
        if len(self.deals) == 0 or len(self.deals) % 2 == 0:
            d = Deal(self, self.non_dealer, self.dealer)
        elif len(self.deals) % 2 == 1:
            d = Deal(self, self.dealer, self.non_dealer)
        self.deals.append(d)
        return d
