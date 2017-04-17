from strat import *
from soccersimulator.mdpsoccer import SoccerTeam



def get_team(numba):
    s = SoccerTeam(name="leoniro1")
    if numba == 1:
        #s.add("John",StrategyAttaquant())
        #s.add("Kerry", StrategyGoal())
        s.add("Leonie", StrategyAttaquant())
        #s.add("Saaroro", StrategyDefense())
        return s
    if numba == 2:
        s.add("Saitaroro",StrategyAttaquant())  
        #s.add("Fred", StrategyGoal())
        #s.add("Leonie", StrategyGoal())
        s.add("Leoie", StrategyDefense())
    if numba == 4:
        s.add("Saitaroro",StrategyAttaquant())  
        s.add("Pogboom", StrategyGoal())
        s.add("Leonie", StrategyAttaquant())
        s.add("LeonieElleestarchibelleettout", StrategyDefense())
    return s
    
        
            
