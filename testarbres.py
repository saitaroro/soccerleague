from soccersimulator import SoccerTeam, Simulation, show_simu
from soccersimulator import Strategy, SoccerAction, Vector2D, load_jsonz,dump_jsonz
import logging
from arbres_utils import DTreeStrategy
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier
import os.path
from arbrematrice import *
import pickle

team2 = SoccerTeam("team2")
team2.add("rien 1", StrategyAttaquant())
team2.add("rien 2", StrategyDefense())

def jouer_arbre():
    ####
    # Utilisation de l'arbre
    ###
    dtree1 = pickle.load(open(os.path.join(os.path.dirname(__file__),"attaquant.pkl"),"rb"))
    dtree2 = pickle.load(open(os.path.join(os.path.dirname(__file__),"defenseur.pkl"),"rb"))
    dic = {"Fonce":FonceStrategy(),"Static":StaticStrategy(),"Attaquant":StrategyAttaquant(), "Defense":StrategyDefense(), "GoalKeeper": StrategyGoal()
    , "Polposition": StrategyAttaquantP()}
    treeStrat1 = DTreeStrategy(dtree1,dic,my_get_features)
    treeStrat2 = DTreeStrategy(dtree2,dic,my_get_features)
    team3 = SoccerTeam("Arbre Team")
    team3.add("Joueur 1",treeStrat1)
    team3.add("Joueur 2",treeStrat2)
    simu = Simulation(team2,team3)
    show_simu(simu)

if __name__=="__main__":
    fn1 = "test_statesatt1.jz"
    fn2 = "test_statesatt2.jz"
    fn3 = "test_statesatt3.jz"
    if not os.path.isfile(fn1) and not os.path.isfile(fn2) and not os.path.isfile(fn3):
        entrainement1(fn1)
        entrainement1(fn2)
        entrainement1(fn3)
    dt1 = apprentissage1(fn1,fn2,fn3)
    
    fn1 = "test_statesdef1.jz"
    fn2 = "test_statesdef2.jz"
    fn3 = "test_statesdef3.jz"
    if not os.path.isfile(fn1) and not os.path.isfile(fn2) and not os.path.isfile(fn3):
        entrainement2(fn1)
        entrainement2(fn2)
        entrainement2(fn3)
    dt2 = apprentissage2(fn1,fn2,fn3)
    jouer_arbre()
    