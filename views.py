from classes import Player, Declaration, Partie, Category
from rabelais import Rabelais

class Prompt:
    ELDER_EXCHANGE = 1
    YOUNGER_EXCHANGE = 2

class Client:

    def get_player(self, player_num):
        return Player(input("Player {}, please enter your name: ".format(player_num)))

    def __init__(self):
        player1 = self.get_player('1')
        player2 = Rabelais('Rabelais')
        self.partie = Partie(player1, player2)

    def get_cards(self, prompt, player, max_cards=1):
        if not isinstance(player, Rabelais):
            messages = {
                Prompt.ELDER_EXCHANGE: '{}, please exchange up to five cards.'.format(player),
                Prompt.YOUNGER_EXCHANGE: '{}, please exchange up to {} cards.'.format(player, max_cards)
            }
            card_str = input("\n{}\nYour hand: {}\n".format(messages[prompt], player.print_hand()))
            cards = card_str.split()

            if len(cards) > max_cards:
                print("You may draw up to {} cards".format(max_cards))
                return self.get_cards(prompt, player, max_cards)

            if len(set(cards)) != len(cards):
                print("Please select up to {} unique cards.")
                return self.get_cards(prompt, player, max_cards)

            try:
                result = [player.hand[chars] for chars in cards]
            except KeyError:
                return self.get_cards(prompt, player, max_cards)
        
        else:
            functions = {
                Prompt.ELDER_EXCHANGE: player.get_elder_exchange,
                Prompt.YOUNGER_EXCHANGE: player.get_younger_exchange
            }
            
            result = functions[prompt]

        return result

    def exchange(self, deal):
        elder, younger = deal.elder, deal.younger
        if elder.carte_blanche:
            print('{} is carte blanche.'.format(elder))
        elder_exchange = self.get_cards(Prompt.ELDER_EXCHANGE, elder, max_cards=5)
        deal.exchange(elder, elder_exchange)
        
        remainder = len(deal.deck)
        
        if younger.carte_blanche:
            print('{} is carte_blanche.'.format(younger))
        younger_exchange = self.get_cards(Prompt.YOUNGER_EXCHANGE, younger, max_cards=remainder)
        deal.exchange(younger, younger_exchange)        

    def declarations(self, deal):
        elder = deal.elder
        younger = deal.younger

        winners = {category: {} for category in Category.categories}
        
        for attr in Category.categories:
            elder_result = getattr(elder, attr)
            younger_result = getattr(younger, attr)
            
            if not elder_result.score:
                value = Declaration.NOT_GOOD
                print('{} is not good in {}.'.format(elder, attr))
            
            else:
                if elder_result.score > younger_result.score:
                    value = Declaration.GOOD
                elif elder_result.score == younger_result.score:
                    value = Declaration.EQUAL
                else:
                    value = Declaration.NOT_GOOD

                print('{} has {} of {}.'.format(elder, attr, elder_result.score))
                print("That's {}.".format(value))

                if value == Declaration.EQUAL:
                    winners[attr]['equal'] = True
                    if elder_result.value > younger_result.value:
                        value = Declaration.GOOD
                    elif elder_result.value == younger_result.value:
                        value = Declaration.EQUAL
                    else:
                        value = Declaration.NOT_GOOD

                    print('{} has {} of {}.'.format(elder, attr, elder_result.value))
                    print("That's {}.".format(value))

            if value == Declaration.GOOD:
                winners[attr]['winner'] = elder
            elif value == Declaration.NOT_GOOD and younger_result.score:
                winners[attr]['winner'] = younger

        for category, result in winners.items():
            winner = result.get('winner')
            if winner:
                equal = winners[category].get('equal')
                attr_level = 'value' if equal else 'score'
                print("{winner} wins {category} with {score}.".format(winner=winner, category=category, score=getattr(getattr(winner, category), attr_level)))

        deal.score_declarations()
        if deal.repique:
            print('{} is repique.'.format(deal.repique))

    def tricks(self, deal):
        lead = deal.elder
        announced_pique = False

        while lead.hand:
            follow = (deal.players - {lead}).pop()

            lead_card = self.get_cards('\n{}, please lead.'.format(lead), lead)[0]
            follow_card = self.get_cards('{}, play {}.'.format(follow, lead_card.suit), follow)[0]
            
            lead_play = {'player': lead, 'card': lead_card}
            follow_play = {'player': follow, 'card': follow_card}
            
            result = deal.play_trick(lead_play, follow_play)
            lead = result['winner']

            if not announced_pique and deal.pique:
                print("{} is pique.".format(deal.pique))
                announced_pique = True

            print('{}: {}'.format(lead, deal.score[lead]))
        
        if result['caput']:
            print('{} is caput.'.format(result['caput']))

    def play_a_hand(self):
        d = self.partie.new_deal()
        # The deal
        d.deal()
        self.exchange(d)
        self.declarations(d)
        print(d.score)
        self.tricks(d)
        print(d.score)
        return d.score

    def play_a_game(self):
        while len(self.partie.deals) < 6:
            scores = self.play_a_hand()
            for player in self.partie.players:
                player.score += scores[player]
            print("After {} deals, the score is {}")

if __name__ == "__main__":
    c = Client()
    c.play_a_game()