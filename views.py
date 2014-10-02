from classes import Player, Declaration, Partie

class Client:

    def get_player(self, player_num):
        return Player(input("Player {}, please enter your name: ".format(player_num)))

    def __init__(self):
        player1 = self.get_player('1')
        player2 = self.get_player('2')
        self.partie = Partie(player1, player2)

    def get_cards(self, message, player, max_cards=1):
        card_str = input("Your hand: {}\n{}".format(player.print_hand(), message))
        cards = card_str.split()

        if len(cards) > max_cards:
            print("You may draw up to {} cards".format(max_cards))
            return self.get_cards(message, player, max_cards)

        return [player.hand[chars] for chars in cards]

    def declarations(self, deal):
        elder = deal.elder
        younger = deal.younger

        winners = {'point': None, 'sequences': None, 'sets': None}
        
        for attr in ('point', 'sequences', 'sets'):
            elder_value = getattr(elder, attr)
            younger_value = getattr(younger, attr)
            print('Testing {} against {} for {}'.format(elder_value, younger_value, attr))
            if elder_value[0] > younger_value[0]:
                value = Declaration.GOOD
            elif elder_value[0] == younger_value[0]:
                value = Declaration.EQUAL
            else:
                value = Declaration.NOT_GOOD

            print('Elder has {} of {}.'.format(attr, elder_value[0]))
            print("That's {}.".format(value))

            if value == Declaration.EQUAL:
                if elder_value[1] > younger_value[1]:
                    value = Declaration.GOOD
                elif elder_value[1] == younger_value[1]:
                    value = Declaration.EQUAL
                else:
                    value = Declaration.NOT_GOOD

                print('Elder has {} of {}.'.format(attr, elder_value[1]))
                print("That's {}.".format(value))

            if value == Declaration.GOOD:
                winners[attr] = elder
            elif value == Declaration.NOT_GOOD:
                winners[attr] = younger

        return winners

    def play_a_hand(self):
        d = self.partie.new_deal()
        d.deal()
        elder, younger = d.elder, d.younger
        elder_exchange = self.get_cards('Elder, please exchange up to five cards: ', 
                                    elder, 
                                    max_cards=5)
        d.exchange(elder, elder_exchange)
        remainder = len(d.deck)
        
        younger_exchange = self.get_cards('Younger, please exchange up to {} cards: '.format(remainder),
                                     younger,
                                     max_cards=remainder)
        d.exchange(younger, younger_exchange)

        declarations_winners = self.declarations(d)

        for attr, winner in declarations_winners.values():
            if winner == younger:
                print "Younger wins {} with {}".format(attr, getattr(younger, attr))