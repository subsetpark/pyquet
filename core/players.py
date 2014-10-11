from core.game import Good, Rank, Player, Category, Deck, all_cards, Declaration, SCORE_VALUES


class HumanPlayer(Player):

    def announce(self, message):
        print(message)

    def get_cards(self, message, min=1, max=1):
        card_str = input("\n{}\nYour hand:\n{}\n".format(message, self.print_hand()))
        cards = [string.upper() for string in card_str.split()]

        if len(cards) > max:
            print("You may draw up to {} cards".format(max))
            return self.get_cards(message, min, max)

        if len(set(cards)) != len(cards):
            print("Please select up to {} unique cards.")
            return self.get_cards(message, min, max)

        if len(cards) < min:
            print("Please select at least {} cards.".format(min))
            return self.get_cards(message, min, max)

        try:
            return [self.hand[chars] for chars in cards]
        except KeyError:
            return self.get_cards(message, max)

    def get_elder_exchange(self):
        return self.get_cards('{}, please exchange up to five cards.'.format(self), min=0, max=5)

    def get_younger_exchange(self, max_cards):
        return self.get_cards('{}, please exchange up to {} cards.'.format(self, max_cards), min=0, max=max_cards)

    def get_good(self, declaration):
        # This can be where you can sink eventually
        return super().get_good()

    def get_lead(self):
        return self.get_cards('\n{}, please lead.'.format(self))[0]

    def get_follow(self, lead_card):
        card = self.get_cards('{}, play {}.'.format(self, lead_card.suit))[0]
        if card.suit != lead_card.suit and [card for card in self.hand.values() if card.suit == lead_card.suit]:
            raise ValueError("You must play {}".format(lead_card))

    def draw(self, cards):
        for card in cards:
            self.hand[card.hash()] = card

    def register(self, player, card, silent=False):
        if not silent:
            print('{} plays {}.'.format(player, card))


class Rabelais(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unseen_cards = set()

    def reset(self):
        super().reset()
        self.unseen_cards = set(self.deal.pool)

    def announce(self, message):
        pass

    def get_elder_exchange(self):
        scored_cards = self.evaluate_hand()
        return scored_cards['cards'][:5]

    def get_younger_exchange(self, max_cards):
        evaluation = self.evaluate_hand()
        scored_cards = evaluation['cards']
        keepers = evaluation['keepers']

        for keeper in keepers:
            for i, card in enumerate(scored_cards):
                if card.rank == keeper.rank and card.suit == keeper.suit:
                    del scored_cards[i]

        return scored_cards[:max_cards]

    def get_declaration(self, category, detail=False):
        return Declaration(self.declare(category), detail)

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

    def draw(self, cards):
        for card in cards:
            self.hand[card.hash()] = card
            self.unseen_cards.remove(card)

    def register(self, player, card, silent=True):
        if player != self:
            self.unseen_cards.remove(card)
