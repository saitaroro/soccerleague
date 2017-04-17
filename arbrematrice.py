from soccersimulator import settings,SoccerTeam, Simulation, show_simu, KeyboardStrategy
from soccersimulator import Strategy, SoccerAction, Vector2D, load_jsonz,dump_jsonz
import logging
from arbres_utils import build_apprentissage,affiche_arbre,DTreeStrategy,apprend_arbre,genere_dot
from sklearn.tree 	import export_graphviz
from sklearn.tree import DecisionTreeClassifier
import os.path
from tools import MyState
from baseaction import *
import pickle

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
#nosstrat
class StrategyAttaquant(Strategy):
    def __init__(self):
        super(StrategyAttaquant,self).__init__("Attaquant")
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
            
class StrategyDefense(Strategy):
    def __init__(self):
        super(StrategyDefense,self).__init__("Defense")
        
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
        super(StrategyGoal,self).__init__("GoalKeeper")
        
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

class StrategyAttaquantP(Strategy):
    def __init__(self):
        super(StrategyAttaquantP,self).__init__("Polposition")
    def compute_strategy(self,state,id_team,id_player):
        mystate=MyState(state,id_team,id_player)
        je=Je(mystate)
        stratje = StratJe(je, mystate)
        return stratje.meposia()


#######
## Constructioon des equipes
#######

team1 = SoccerTeam("teamattaq")
team4 = SoccerTeam("teamdef")
strat_j1 = KeyboardStrategy()
strat_j2 = KeyboardStrategy()
team2 = SoccerTeam("team2")
team2.add("rien 1", StrategyAttaquant())
team2.add("rien 2", StrategyDefense())

strat_j1.add('z', StrategyAttaquant())
strat_j1.add('a',StaticStrategy())
strat_j1.add('e', StrategyAttaquantP())
team1.add("Jexp 1",strat_j1)
team1.add("Jexp 2", StrategyDefense())
 
strat_j2.add('w', StrategyGoal())
strat_j2.add('x', StrategyDefense())
team4.add("Jexp 1",StrategyAttaquant())
team4.add("Jexp 2", strat_j2)


### Transformation d'un etat en features : state,idt,idp -> R^d
def my_get_features(state,idt,idp):
    """ extraction du vecteur de features d'un etat, ici distance a la balle, distance au but, distance balle but """
    mystate=MyState(state,idt,idp)
    p_pos= state.player_state(idt,idp).position
    f1 = state.ball.position.distance(p_pos)
    """
     p_pos.distance( Vector2D((2-idt)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))
    """
    f2 = mystate.ennemieleplusproche().distance(p_pos)
    
    f3 = mystate.equipierleplusproche[0]
    f4 = mystate.distbut()
    f5 = state.ball.position.distance(mystate.pos_monbut())
    return [f1,f2,f3,f4,f5]

def entrainement1(fn):
    
    simu = Simulation(team1,team2)
    show_simu(simu)
    
    training_states = strat_j1.states
    
    dump_jsonz(training_states,fn)
    
    
def entrainement2(fn):
    
    
    simu = Simulation(team4,team2)
    show_simu(simu)
    # recuperation de tous les etats
    training_states = strat_j2.states
    # sauvegarde dans un fichier
    dump_jsonz(training_states,fn)

    

def apprentissage1(fn1,fn2,fn3):
    ### chargement d'un fichier sauvegarder
    states_tuple = load_jsonz(fn1)+load_jsonz(fn2)+load_jsonz(fn3)
    ## Apprentissage de l'arbre
    data_train, data_labels = build_apprentissage(states_tuple,my_get_features)
    dt = apprend_arbre(data_train,data_labels,depth=10)
    # Visualisation de l'arbre
    affiche_arbre(dt)
    genere_dot(dt,"arbreattaq.dot")
    pickle.dump(dt,open("attaquant.pkl","wb"))
    return dt
    
def apprentissage2(fn1,fn2,fn3):
    ### chargement d'un fichier sauvegarder
    states_tuple = load_jsonz(fn1)+load_jsonz(fn2)+load_jsonz(fn3)
    ## Apprentissage de l'arbre
    data_train, data_labels = build_apprentissage(states_tuple,my_get_features)
    dt = apprend_arbre(data_train,data_labels,depth=10)
    # Visualisation de l'arbre
    affiche_arbre(dt)
    genere_dot(dt,"arbredef.dot")
    pickle.dump(dt,open("defenseur.pkl","wb"))
    return dt


    
