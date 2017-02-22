from strat import RandomStrategy, StrategyAttaquant, StrategyDefense, StrategyGoal
from soccersimulator.mdpsoccer import SoccerTeam


def get_team(numba):
    s = SoccerTeam(name="leoniro1")
    if numba == 1:
        #s.add("John",StrategyAttaquant())
        #s.add("Kerry", StrategyGoal())
        s.add("Leonie", StrategyAttaquant())
        #s.add("Saaroro", StrategyDefense())
        return s
    #if numba == 2:
        #s.add("Saitaroro",StrategyDefense())  
        #s.add("Fred", StrategyGoal())
        #s.add("Leonie", StrategyAttaquant())
        #s.add("Leoie", StrategyDefense())
    return s
    #if numba == 3
    #if numba == 4:
    
        
            
