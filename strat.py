from soccersimulator.strategies  import Strategy
from soccersimulator.mdpsoccer import SoccerTeam, Simulation, SoccerAction
from soccersimulator.gui import SimuGUI,show_state,show_simu
from soccersimulator.utils import Vector2D
from soccersimulator import settings
from tools import MyState
from baseaction import Je, StratJe

## Strategie aleatoire

class FonceStrategy(Strategy):
    def __init__(self):
        super(FonceStrategy,self).__init__("Fonce")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)

class StaticStrategy(Strategy):
    def __init__(self):
        super(StaticStrategy,self).__init__("Static")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction()
        
class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random(-0.5,0.5),Vector2D.create_random(-0.5,0.5))

class StrategyAttaquant(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        mystate=MyState(state,id_team,id_player)
        je=Je(mystate)
        stratje = StratJe(je, mystate)
        
        #dribble
        if mystate.my_position != mystate.ball_position() and not mystate.procheduballon(): 
            return je.aller(mystate.ball_position())
        else:
            if not mystate.estdanscda():
                return stratje.dribble()
            else:
                return je.shoot1(mystate.ball_position().distance(mystate.pos_sonbut()),mystate.pos_sonbut()) 
            
class StrategyAttaquantP(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        mystate=MyState(state,id_team,id_player)
        je=Je(mystate)
        stratje = StratJe(je, mystate)
        return stratje.meposia()
            
class StrategyDefense(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        mystate=MyState(state,id_team,id_player)
        je=Je(mystate)
        stratje = StratJe(je, mystate)
           
        if mystate.my_position != mystate.ball_position() and not mystate.procheduballon() and mystate.balldanscdd():
            return stratje.interception()
        if mystate.procheduballon():
            return stratje.papp()
        if not mystate.balldanscdd():
            return stratje.meposid()
        
class StrategyGoal(Strategy):
    def __init__(self):
        Strategy.__init__(self,"GoalKeeper")
        
    def compute_strategy(self,state,id_team,id_player):
        mystate=MyState(state,id_team,id_player)
        je=Je(mystate)
        stratje = StratJe(je, mystate)
        
        if mystate.balldanscdg() and not mystate.procheduballon():
            return je.aller(mystate.ball_position())
        if mystate.procheduballon():
            return stratje.degagement()
        if not mystate.balldanscdg() and mystate.danslescages():
            return stratje.meposig() 
        
class StratAttaquePlusPlus(Strategy):
    def __init__(self):
        Strategy.__init__(self,"AttaquePlusPlus")
    def compute_strategy(self,state,id_team,id_player):
        if
    