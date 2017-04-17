
from soccersimulator.mdpsoccer import SoccerAction
from soccersimulator.utils import Vector2D


import math

class Je(object):

    def __init__(self, mystate):
        self.mystate = mystate

    def exp(self, x):
        return 4.66*(1-math.exp(-3.77*x))
    def exp_expe(self,a,b,x):
        return a*(1-math.exp(-b*x))
        
    def shoot_exp(self,a,b):
        shoot = self.mystate.pos_sonbut()-self.mystate.ball_position()
        d = shoot.norm
        return SoccerAction(Vector2D(),self.exp_expe(a,b,d)*shoot.normalize())
        
    def puissance(self, x):
        return 4*x**2
        
    def ral(self,p,x):
        return self.mystate.my_position.distance(p)*x/10
        
    def al(self,p):
        return SoccerAction(p-self.mystate.my_position, Vector2D())
        
    def aller(self,p):
        return SoccerAction(self.ral(p,p-self.mystate.my_position), Vector2D())
    
    def shoot1(self,Uballgoal,p):
        return SoccerAction(Vector2D(),self.exp(Uballgoal)*(p-self.mystate.my_position))
        
    def shoot2(self,Uballgoal,p):
        return SoccerAction(Vector2D(),p-self.puissance(Uballgoal)*self.mystate.my_position.normalize())
     
    def shootcoef(self, p, coef):
        if self.mystate.procheduballon:    
            return SoccerAction(Vector2D(),coef*(p-self.mystate.my_position))
        return self.SoccerAction(Vector2D(), Vector2D())
    
    def acceleration(self, p, c):
        return SoccerAction(c*(p-self.mystate.my_position), Vector2D()) 
    
    #plongeon for the fame
    #def pftf(self):

   
    


class StratJe(object):
    
    
    def __init__(self, je, mystate):
        self.je = je
        self.mystate= self.je.mystate
        
    #degagement posi    
    #passe au goal
    #def pag(self):
    
    #arrete de suivre la balle! 
    def asb(self):
        if self.mystate.equipierleplusproche == self.mystate.ball_position():
            return self.je.aller(self.mystate.my_position)
    
    
    #passe au plus proche 
    def papp(self):
        return self.je.shoot1(self.mystate.equipierleplusproche[0],self.mystate.equipierleplusproche[1])

    #atk action
    def interception(self):
        return self.je.aller(self.mystate.ball_position()+self.mystate.ball_speed()*12) 
    
    def interception2(self):
        return self.je.al(self.mystate.ball_position()+self.mystate.ball_speed()*12)
            
    #def action
    def degagement(self):
        return self.je.shoot1(self.mystate.ball_position().distance(self.mystate.pos_sonbut()),self.mystate.pos_sonbut())
    
    
    #mepositionne
    def meposig(self):
        return self.je.aller(self.mystate.pos_monbut())
    def meposid(self):
        pos = Vector2D(self.mystate.cdd(),self.mystate.my_position.y)
        return self.je.aller(pos)
    def meposia(self):
        pos = Vector2D(self.mystate.postir(), self.mystate.my_position.y)
        return self.je.aller(pos)
    #dribblecr7
    def dribble(self):
            return SoccerAction(Vector2D(),(self.mystate.pos_sonbut()-self.mystate.my_position).norm_max(1.8))
                  
