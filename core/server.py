from core.game import Good, Declaration, Partie, Category
from core.players import Rabelais, HumanPlayer

class Server:

    def get_player(self, player_num):
        return HumanPlayer(input("Player {}, please enter your name: ".format(player_num)))

    def __init__(self):
        player1 = self.get_player('1')
        player2 = Rabelais('Rabelais')
        self.players = {player1, player2}
        self.partie = Partie(player1, player2)

    def announce(self, message):
        for player in self.players:
            player.announce(message)

    def register(self, player, card):
        for recipient in self.players:
            recipient.register(player, card)

    def exchange(self, deal):
        elder, younger = deal.elder, deal.younger
        
        if elder.carte_blanche:
            self.announce('{} is carte blanche.'.format(elder))
        
        elder_exchange = elder.get_elder_exchange()
        self.announce('{} exchanges {} cards.'.format(elder, len(elder_exchange)))
        deal.exchange(elder, elder_exchange)
        
        remainder = len(deal.deck)
        
        if younger.carte_blanche:
            self.announce('{} is carte_blanche.'.format(younger))
        
        younger_exchange = younger.get_younger_exchange(remainder)
        self.announce('{} exchanges {} cards.'.format(younger, len(younger_exchange)))
        deal.exchange(younger, younger_exchange)        

    def declarations(self, deal):
        elder = deal.elder
        younger = deal.younger

        winners = {category: {} for category in Category.categories}
        self.announce('---')
        for category in Category.categories:
            detail = False
            
            elder_declaration = Declaration(getattr(elder, category))

            if not elder_declaration.score:
                good = Good.NOT_GOOD
                self.announce('{} is not good in {}.'.format(elder, category))
            
            else:
                good = younger.get_good(elder_declaration)

                self.announce('{} has {}.'.format(elder, elder_declaration))
                self.announce("That's {}.".format(good))

                if good == Good.EQUAL:
                    detail = True
                    elder_declaration = Declaration(getattr(elder, category), detail=True)
                    good = younger.get_good(elder_declaration)

                    self.announce('{} has {}.'.format(elder, elder_declaration))
                    self.announce("That's {}.".format(good))

            if good == Good.GOOD:
                winners[category]['winner'] = elder_declaration
            elif good == Good.NOT_GOOD:
                younger_declaration = Declaration(getattr(younger, category), detail)
                if younger_declaration:
                    winners[category]['winner'] = younger_declaration

        for category in Category.categories:
            result = winners[category]
            winning_declaration = result.get('winner')
            if winning_declaration:
                self.announce("{winner} wins {category} with {score}.".format(winner=winning_declaration.result.player, 
                                                                              category=category, 
                                                                              score=winning_declaration.all_results))

        deal.score_declarations()
        if deal.repique:
            self.announce('{} is repique.'.format(deal.repique))
        self.announce(self.deal.score)

    def tricks(self, deal):
        lead = deal.elder
        announced_pique = False
        self.announce('---')
        while lead.hand:
            follow = (deal.players - {lead}).pop()

            lead_card = lead.get_lead()
            self.register(lead, lead_card)
            follow_card = follow.get_follow(lead_card)
            self.register(follow, follow_card)

            lead_play = {'player': lead, 'card': lead_card}
            follow_play = {'player': follow, 'card': follow_card}
            
            result = deal.play_trick(lead_play, follow_play)
            lead = result['winner']
            self.announce('{} takes the trick.'.format(lead))

            if not announced_pique and deal.pique:
                self.announce("{} is pique.".format(deal.pique))
                announced_pique = True

            self.announce('{}: {}'.format(lead, deal.score[lead]))
        
        if result['caput']:
            self.announce('{} is caput.'.format(result['caput']))

    def play_a_hand(self):
        d = self.partie.new_deal()
        # The deal
        self.announce('---')
        d.deal()
        self.exchange(d)
        self.declarations(d)
        self.tricks(d)
        return d.score

    def play_a_game(self):
        while len(self.partie.deals) < 6:
            self.play_a_hand()
            self.announce("After {} deal(s), the score is {}".format(len(self.partie.deals), self.partie.score))
        
        final_score = self.partie.get_final_score()
        
        winner = self.partie.winner
        loser = self.partie.loser

        if self.partie.score[loser] >= 100:
            self.announce('{} crossed the rubicon and {} won with {}.'.format(loser, winner, final_score))
        else:
            self.announce('{} failed to cross the rubicon and {} won with {}.'.format(loser, winner, final_score))