
from soccersimulator.utils import Vector2D
from soccersimulator import settings


class MyState(object):
    def __init__(self, state, idteam, idplayer):
        self.state = state
        self.idt = idteam
        self.idp = idplayer
    @property
    def equipierleplusproche(self):
        dist = 500
        idx = 0
        for (idt,idp) in self.state.players:
            if idt != self.idt: 
                continue
            if idp == self.idp and idt == self.idt:
                continue
            if self.my_position.distance(self.state.player_state(idt,idp).position)<dist:
                idx = idp
                dist = self.my_position.distance(self.state.player_state(idt,idp).position)
                pos = self.state.player_state(idt,idp).position
            
        tab = [dist, pos, idx]
        return tab
    @property
    def my_position(self):
        return self.state.player_state(self.idt, self.idp).position
    
    def ball_position(self):
        return self.state.ball.position
    
    def ball_speed(self):
        return self.state.ball.vitesse
        
    def pos_sonbut(self):
        if self.idt==1:
            return Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)
        return Vector2D(0,settings.GAME_HEIGHT/2)
    def pos_monbut(self):
        if self.idt==2:
            return Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)
        else:
            return Vector2D(0,settings.GAME_HEIGHT/2)
            
    def ennemieleplusproche(self):
        dist = 500
        idx = 0
        for (idt,idp) in self.state.players:
            if idt == self.idt: 
                continue
            if self.my_position.distance(self.state.player_state(idt,idp).position)<dist:
                idx = idp
                dist = self.my_position.distance(self.state.player_state(idt,idp).position)
                pos = self.state.player_state(idt,idp).position
        return pos
        
    #zones joueurs
    

    def procheduballon(self):
        if self.my_position.distance(self.ball_position())>(settings.PLAYER_RADIUS+settings.BALL_RADIUS):
            return False
        return True
    def procheduballdef(self):
        return self.my_position.distance(self.ball_position())>(settings.PLAYER_RADIUS+settings.BALL_RADIUS)
    
    def prochedugoal(self):
        return self.my_position.distance(self.ball_position())>(settings.PLAYER_RADIUS+settings.BALL_RADIUS)*20
       

    def danslescages(self):
        return self.my_position.distance(self.pos_monbut())>(settings.PLAYER_RADIUS+settings.BALL_RADIUS)
        
    def distbut(self):
        return self.my_position.distance(self.pos_sonbut())
       
    
    
    
    #champ de defense        
    def estdanscdd(self):
        if self.idt == 1:
            return self.my_position.x<=37.5
        return self.my_position.x>=112.5
    
    #champ goal
    def estdanscdg(self):
        if self.idt == 1:
            return self.my_position.x<=37.5
        return self.my_position.x>=112.5
    #ligne def (x)
    def cdd(self):
        if self.idt == 1:
            return 37.5
        return 112.5
    
    def postir(self):
        if self.idt == 1:
            return 120
        return 30
        
    #ball dans la zone
    def estdanscda(self):
        if self.idt == 1:
            return self.my_position.x>=110
        return self.my_position.x<=40
        
        
    def ennemiedanscdd(self):
        if self.idt==1:
            return self.ennemieleplusproche.x<40
        return self.ennemieleplusproche.x>110

    def balldanscdd(self):
        if self.idt == 1:
            return self.ball_position().x<75
        return self.ball_position().x>75
        
     #ball dans la zone
    def balldanscdg(self):
        if self.idt == 1:
            return self.ball_position().x<=37.5 and self.ball_position().y>=25 and self.ball_position().y<=65
        return self.ball_position().x>=112.5 and self.ball_position().y>=25 and self.ball_position().y<=65
        
    def balldanscda(self):
        if self.idt == 1:
            return self.ball_position().x>25
        return self.ball_position().x<25

            