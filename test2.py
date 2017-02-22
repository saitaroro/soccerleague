#from soccersimulator.strategies  import Strategy
from soccersimulator.mdpsoccer import SoccerTeam, Simulation, SoccerState
from soccersimulator.gui import SimuGUI,show_state,show_simu
from soccersimulator.utils import Vector2D
#from soccersimulator import settings
#from tools import MyState
#from baseaction import Je, StratJe
from __init__ import get_team

state=SoccerState.create_initial_state(1,1)
state.player_state(1,0).position=Vector2D(120,45)
state.ball.position=state.player_state(1,0).position

simu= Simulation(get_team(1),get_team(2))
#Jouer et afficher la partie
show_simu(simu)
#Jouer sans afficher
simu.start()