from pyquet.game import Rank, Player, Category

class HumanPlayer(Player):
    def get_cards(self, message, max_cards=1):
        card_str = input("\n{}\nYour hand: {}\n".format(message, self.print_hand()))
        cards = card_str.split()

        if len(cards) > max_cards:
            print("You may draw up to {} cards".format(max_cards))
            return self.get_cards(message, max_cards)

        if len(set(cards)) != len(cards):
            print("Please select up to {} unique cards.")
            return self.get_cards(message, max_cards)

        try:
            return [self.hand[chars] for chars in cards]
        except KeyError:
            return self.get_cards(message, max_cards)
    
    def get_elder_exchange(self):
        return self.get_cards('{}, please exchange up to five cards.'.format(self))

    def get_younger_exchange(self, max_cards):
        return self.get_cards('{}, please exchange up to {} cards.'.format(self, max_cards), max_cards)

    def get_lead(self):
        return self.get_cards('\n{}, please lead.'.format(self))[0]

    def get_follow(self, lead_card):
        return self.get_cards('{}, play {}.'.format(self, lead_card.suit))[0]


class Rabelais(Player):

    SCORE_VALUES = {
        Category.POINT: {
            0: 0,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8
        },
        Category.SEQUENCES: {
            0: 0,
            3: 3,
            4: 4,
            5: 15,
            6: 16,
            7: 17,
            8: 18
        },
        Category.SETS: {
            0: 0,
            3: 3,
            4: 14
        }
    }

    def card_sort(self, cards):
        return sorted(list(cards), key=lambda x:(x.suit, x.rank.value))

    def get_elder_exchange(self):
        low_ranks = {
            Rank.Seven,
            Rank.Eight,
            Rank.Nine
        }
        suits = self.suits()

        point_suit = suits[-1]
        max_length = len(point_suit)

        low_non_points = [card for card in self.hand.values() if card.rank in low_ranks and card not in point_suit]
        if len(low_non_points) >= 5:
            return self.card_sort(low_non_points)[:5]

        sequence_cards = set([card for sequence in self.sequences.value for card in sequence])
        set_cards = set([card for card_set in self.sets.value for card in card_set])
        aces = set([card for card in self.hand.values() if card.rank == Rank.Ace])

        undesirables = set(self.hand.values()) - (sequence_cards | set_cards | aces)

        if len(undesirables) >= 5:
            return self.card_sort(undesirables)[:5]

        discards = set(low_non_points) | undesirables
        return self.card_sort(discards)[:5]

    def get_younger_exchange(self, max_cards):
        keepers = set()
        suits = self.suits()
        for suit in suits:
            if suit:
                suit.sort(reverse=True)
                distance = 14 - suit[0].rank.value
                if len(suit) - 1 >= distance:
                    keepers.update(suit[:distance + 1])

        weighted_score = sorted(Category.categories, key=lambda x:-self.SCORE_VALUES[x][getattr(self, x).score])[0]

        if weighted_score in (Category.SETS, Category.SEQUENCES):
            keepers.update([card for group in getattr(self, weighted_score).value for card in group])
        else:
            keepers.update(suits[-1])

        remainder = set(self.hand.values()) - keepers

        return sorted(list(remainder), key=lambda x:x.rank.value)[:max_cards]

    def get_lead(self):
        return self.suits()[-1][-1]

    def get_follow(self, lead_card):
        follow_suit = sorted([card for card in self.hand.values() if card.suit == lead_card.suit])
        if follow_suit:
            better_cards = [card for card in follow_suit if card.rank.value > lead_card.rank.value]
            if better_cards:
                return better_cards[0]
            else:
                return follow_suit[0]
        else:
            return sorted(self.hand.values())[0]