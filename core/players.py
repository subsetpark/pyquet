from core.game import Good, Rank, Player, Category, Deck, all_cards, Declaration, SCORE_VALUES, Card


class HumanPlayer(Player):

    def announce(self, message):
        print(message)

    def get_cards(self, message, min=1, max=1):
        card_str = input("\n{}\nYour hand:\n{}\n".format(message, self.print_hand()))

        # DEBUGGING PURPOSES
        if card_str == 'DEBUG':
            if not self.deal.elder.__class__ == HumanPlayer:
                computer = self.deal.elder
            else:
                computer = self.deal.younger
            print("{}:\n{}\nSeen: {}".format(computer, computer.print_hand(), computer.seen_cards))

        if not card_str:
            return []

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
            return self.get_cards(message, min, max)

    def get_elder_exchange(self):
        return self.get_cards('{}, please exchange up to five cards.'.format(self), min=0, max=5)

    def get_younger_exchange(self, max_cards):
        return self.get_cards('{}, please exchange up to {} cards.'.format(self, max_cards), min=0, max=max_cards)

    def get_good(self, declaration):
        # This can be where you can sink eventually
        return super().get_good(declaration)

    def get_lead(self):
        return self.get_cards('\n{}, please lead.'.format(self))[0]

    def get_follow(self, lead_card):
        card = self.get_cards('{}, play {}.'.format(self, lead_card.suit))[0]
        
        if card.suit != lead_card.suit and self.get_suit(lead_card.suit):
            self.announce("You must play {}".format(lead_card.suit))
            return self.get_follow(lead_card)

        return card

    def draw(self, cards):
        for card in cards:
            self.hand[card.hash()] = card

    def register(self, player, card, silent=False):
        if not silent:
            print('{} plays {}.'.format(player, card))


class Rabelais(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_cards = {}

    def reset(self):
        super().reset()
        self.seen_cards = {}

    def announce(self, message):
        pass

    def evaluate_hand(self):
        scored_cards = {}
        keepers = []
        # Score for position in declarations
        for card in self.hand.values():
            score = 0
            for category in Category.categories:
                result = self.declare(category)
                if result.find_card(card):
                    score += result.value * result.strength
            scored_cards[card] = score
        
        # Score for trick-taking ability
        for suit in self.suits():
            if not suit:
                continue

            suit.reverse()

            if suit[0].rank == Rank.Ace: # Offensive ability
                scored_cards[suit[0]] = scored_cards.get(suit[0], 0) + 1
                for i, card in enumerate(suit):
                    scored_cards[card] = scored_cards.get(card, 0) + 1
                    keepers.append(card)
                    if i == len(suit) - 1 or card - suit[i+1] != 1:
                        break
            else:                        # Defensive ability
                distance = 14 - suit[0].rank.value
                if len(suit) - 1 >= distance:
                    for card in suit[:distance + 1]:
                        scored_cards[card] = scored_cards.get(card, 0) + .5
                        keepers.append(card)

        result = sorted([(score, card) for card, score in scored_cards.items()])
        return {'cards': [weighted[1] for weighted in result],
                'keepers': keepers}


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

    def get_lead(self):
        best_suit = (None, 0)
        for suit_cards in self.suits():
            if suit_cards:
                suit = suit_cards[0].suit
                counter = 0
                suit_cards.reverse()
                for rank in reversed([r for r in Rank]):
                    candidate = Card(rank, suit).hash()
                    if self.hand.get(candidate) or self.seen_cards.get(candidate):
                        counter +=1
                if counter > best_suit[1]:
                    best_suit = (suit, counter)
        if best_suit[0]:
            return self.get_suit(best_suit[0])[0]
        else:
            return self.suits()[-1][-1]

    def get_follow(self, lead_card):
        follow_suit = self.get_suit(lead_card.suit)
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
            self.seen_cards[card.hash()] = card

    def register(self, player, card, silent=True):
        if player != self:
            self.seen_cards[card.hash()] = card