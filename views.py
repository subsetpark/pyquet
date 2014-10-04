from pyquet.game import Declaration, Partie, Category
from pyquet.players import Rabelais, HumanPlayer

class Prompt:
    ELDER_EXCHANGE = 1
    YOUNGER_EXCHANGE = 2

class Client:

    def get_player(self, player_num):
        return HumanPlayer(input("Player {}, please enter your name: ".format(player_num)))

    def __init__(self):
        player1 = self.get_player('1')
        player2 = Rabelais('Rabelais')
        self.partie = Partie(player1, player2)

    def exchange(self, deal):
        elder, younger = deal.elder, deal.younger
        
        if elder.carte_blanche:
            print('{} is carte blanche.'.format(elder))
        
        elder_exchange = elder.get_elder_exchange()
        print('{} exchanges {} cards.'.format(elder, len(elder_exchange)))
        deal.exchange(elder, elder_exchange)
        
        remainder = len(deal.deck)
        
        if younger.carte_blanche:
            print('{} is carte_blanche.'.format(younger))
        
        younger_exchange = younger.get_younger_exchange(remainder)
        print('{} exchanges {} cards.'.format(younger, len(younger_exchange)))
        deal.exchange(younger, younger_exchange)        

    def declarations(self, deal):
        elder = deal.elder
        younger = deal.younger

        winners = {category: {} for category in Category.categories}
        print('---')
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

            lead_card = lead.get_lead()
            for player in deal.players:
                player.register(lead, lead_card)
            follow_card = follow.get_follow(lead_card)
            print('{} plays {}.'.format(follow, follow_card))
            lead_play = {'player': lead, 'card': lead_card}
            follow_play = {'player': follow, 'card': follow_card}
            
            result = deal.play_trick(lead_play, follow_play)
            lead = result['winner']
            print('{} takes the trick.'.format(lead))

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
            self.play_a_hand()
            print("After {} deal(s), the score is {}".format(len(self.partie.deals), self.partie.score))

if __name__ == "__main__":
    c = Client()
    c.play_a_game()