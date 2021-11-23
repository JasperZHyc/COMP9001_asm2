import math
import config
import random
class SpaceObject:
    def __init__(self, x, y, width, height, angle, obj_type, id):
        # Enter your code here
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.angle=angle%360
        self.obj_type=obj_type
        self.id=id
        self.radius=config.radius[self.obj_type]
        self.count=config.bullet_move_count   # to record the life remaining of bullet

    def turn_left(self):
        # Enter your code here
        # if spaceship counterclockwise rotate
        if(self.obj_type=="spaceship"):
            self.angle+=config.angle_increment # rotate speed
        self.angle=self.angle % 360
    def turn_right(self):
        
        # Enter your code here
        # if spaceship clockwise rotate
        if(self.obj_type=="spaceship"):
            self.angle-=config.angle_increment # rotate speed
        self.angle=self.angle % 360
    def move_forward(self):
        
        # Enter your code here
        # maintain angle move
        #angle0=self.angle*math.pi/180
        self.x+=config.speed[self.obj_type]*math.cos(math.radians(self.angle))
        if(self.x<=0):  # left boundary
            self.x=self.width+self.x
        elif(self.x>=self.width): # right boundary
            self.x=self.x-self.width
        self.y-=config.speed[self.obj_type]*math.sin(math.radians(self.angle))
        if(self.y<=0):  # up boundary
            self.y=self.height+self.y
        elif(self.y>=self.height): # low boundary
            self.y=self.y-self.height
        
    def get_xy(self):
        
        # Enter your code here
        # return x&y 
        return (self.x,self.y)

    def collide_with(self, other):
        
        # Enter your code here
        # if collide, return true, otherwise return false
        minusx=min((min(self.width-self.x,self.x)+min(self.width-other.x,other.x)),abs((self.x-other.x))) # the least difference of x with two objects
        minusy=min((min(self.height-self.y,self.y)+min(self.height-other.y,other.y)),abs((self.y-other.y)))# the least difference of y with two objects
        distance=(minusx**2+minusy**2)**0.5
        if(distance<=(config.radius[self.obj_type]+config.radius[other.obj_type])):
            return True
        else: 
            return False

    def __repr__(self):
        
        # Enter your code here
        # return information about the object
        state_str=""
        state_str+=str(self.obj_type)
        state_str+=" "
        state_str+=str(round(self.x,1))
        state_str+=","
        state_str+=str(round(self.y,1))
        state_str+=","
        state_str+=str(self.angle)
        state_str+=","
        state_str+=str(self.id)
        return state_str

    # You can add additional methods if required
