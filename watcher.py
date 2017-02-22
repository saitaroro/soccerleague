from baseaction import Je
from tools import MyState
from soccersimulator.settings import *
from soccersimulator import SoccerTeam,Strategy, Simulation,Vector2D
from soccersimulator import show_simu
from __init__ import get_team
import numpy as np


class ExpeStrat(Strategy):
    def __init__(self):
        Strategy.__init__(self)
        self.a = 0
        self.b = 0
    def compute_strategy(self,state,id_team,id_player):
        mystate=MyState(state,id_team,id_player)
        return Je(MyState(state,id_team,id_player)).shoot_exp(self.a,self.b)
         


class Watcher(object):
    MAX_STEP=40
    def __init__(self):
        team1 = SoccerTeam("expe")
        self.strat = ExpeStrat()
        team1.add("jexpe",self.strat)
        team2 = SoccerTeam("rien")
        team2.add("jrien",Strategy())
        self.simu=Simulation(team1,team2,max_steps=100000)
        self.simu.listeners+=self
        self.nb_expe = 10
        self.res = dict()
        self.bestres = dict()
        lista = np.linspace(3,10,10)
        listb = np.linspace(3,10,10)
        self.list_params = [(x,y) for x in lista for y in listb ]
        self.i = 0
        self.but = 0
        self.expe_tot = 0
        		#ajout de l observeur Watcher a la liste des observeurs pendant la simulation
    def begin_match(self, team1, team2, state):
    		#initialisation des parametres				
        self.last, self.but, self.expe_tot=0, 0, 0
          
    def begin_round(self, team1, team2, state):
    		#self.simu.state.states[(1,0)].position=
         x,y = np.random.random()*GAME_WIDTH/2.+GAME_WIDTH/2, np.random.random()*GAME_HEIGHT
         self.simu.state.states[(1,0)].position = Vector2D(x,y)
         self.simu.state.ball.position = Vector2D(x,y)
         self.strat.a,self.strat.b = self.list_params[self.i]
         self.last = state.step
     
    def update_round(self,team1,team2,state):
        if state.step>self.last+self.MAX_STEP: 
            self.simu.end_round()
    	
    def start(self,visu=True):
         if visu:
             show_simu(self.simu)
         else:
             self.simu.start()
    def end_round(self,team1,team2,state):
        if state.goal>0: 
              self.but+=1
        self.expe_tot+=1
        if self.expe_tot>self.nb_expe:
            self.res[self.list_params[self.i]]= self.but*1./self.expe_tot
            if self.but*1./self.expe_tot >=0.7:
                self.bestres[self.list_param[self.i]] = self.but*1./self.expe_tot
            print(self.list_params[self.i],self.res[self.list_params[self.i]])
            self.i+=1
            self.but = 0
            self.expe_tot =0
            if self.i>len(self.list_params):
                self.simu.end_match()
    

watcher = Watcher()
watcher.start(True)