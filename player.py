import math
import config
class Player:
    def __init__(self):
        #0 means just move_forward
        #1 means turn left and move_forward
        #2 means turn right and move_forward
        self.action_try=0
        self.target_before=None
        
        
    def distance_objects(self,spaceship,asteroid): # return the least distance  between two objects
            minusx=min((min(spaceship.width-spaceship.x,spaceship.x)+min(spaceship.width-asteroid.x,asteroid.x)),abs((spaceship.x-asteroid.x)))
            minusy=min((min(spaceship.height-spaceship.y,spaceship.y)+min(spaceship.height-asteroid.y,asteroid.y)),abs((spaceship.y-asteroid.y)))
            distance=(minusx**2+minusy**2)**0.5
            return distance

    def angle_abs_objects(self,spaceship,asteroid): # return the angle of a line connected two center of two objects 
        minusx=min((min(spaceship.width-spaceship.x,spaceship.x)+min(spaceship.width-asteroid.x,asteroid.x)),abs((spaceship.x-asteroid.x)))
        return math.degrees(math.acos(minusx/self.distance_objects(spaceship,asteroid)))

    def action_back(self,action,spaceship): # use to make spaceship go back origin location after simulate action in choose_action
        spaceship.angle+=180
        spaceship.move_forward()
        spaceship.angle+=180
        if(action==0):
            pass
        if(action==1):
            spaceship.turn_right()
        if(action==2):
            spaceship.turn_left()

    def action_back_for_fdc(self,spaceship,angle):# use to make spaceship go back origin location after simulate action in choose_fire_direction
        spaceship.angle+=180
        spaceship.move_forward()
        spaceship.angle+=180
        spaceship.angle=angle

    
    def action(self, spaceship, asteroid_ls, bullet_ls, fuel, score):
        
        target=self.choose_asteroid(spaceship,asteroid_ls)
        if(len(bullet_ls)!=0 and (self.target_before in asteroid_ls)):
            target=self.change_target(spaceship,asteroid_ls,self.target_before)
        if(self.distance_objects(spaceship,target)<config.speed["bullet"]*(config.bullet_move_count)+config.radius[target.obj_type]):
            angle_right=self.choose_fire_direction(spaceship,target)
            if(self.distance_objects(spaceship,target)<config.radius["spaceship"]+config.radius[target.obj_type]+config.speed["spaceship"]):

                if(abs(angle_right-spaceship.angle)<=7.5):
                    self.target_before=target
                    return(False,False,False,True)
                if(spaceship.angle<angle_right and angle_right-spaceship.angle<180) or (spaceship.angle>angle_right and spaceship.angle-angle_right>180):
                    return (False,True,False,False)
                else:
                    return (False,False,True,False)
            if(self.distance_objects(spaceship,target)<config.speed["bullet"]*(config.bullet_move_count-2)+config.radius[target.obj_type]) or (target.obj_type=="asteroid_large"):
                if(abs(angle_right-spaceship.angle)<=7.5) or (abs(angle_right-spaceship.angle)<=7.5 and target.obj_type=="asteroid_large"):
                    self.target_before=target
                    return (True,False,False,True)
                if(spaceship.angle<angle_right and angle_right-spaceship.angle<180) or (spaceship.angle>angle_right and spaceship.angle-angle_right>180):
                    best_action=(True,True,False,False)
                else:
                    best_action=(True,False,True,False)
            else:
                best_action=self.choose_action(spaceship,target)
                return best_action

        else:
            best_action=self.choose_action(spaceship,target)

        return best_action

    def change_target(self,spaceship,asteroid_ls,target_done):
        asteroidlist_tmp=asteroid_ls[:]
        asteroidlist_tmp.remove(target_done)
        return self.choose_asteroid(spaceship,asteroidlist_tmp)
        
    def choose_asteroid(self,spaceship,asteroid_ls): # choose the asteroid spaceship should move to 
        profit_max=0
        for asteroid in asteroid_ls:
            distance=self.distance_objects(spaceship,asteroid)
            if(asteroid.obj_type=="asteroid_large"):
                profit=100/distance
            elif(asteroid.obj_type=="asteroid_small"):
                profit=150/distance
            if(profit>profit_max):
                profit_max=profit
                target_asteroid=asteroid
        return target_asteroid

    def choose_action(self,spaceship,target):   #choose action that action method should return, when spaceship haven't gone to the effective shoot range
        
        #just move_forward
        spaceship.move_forward()
        distance0=self.distance_objects(spaceship,target)
        self.action_try=0
        self.action_back(self.action_try,spaceship)
        #turn left and move_forward
        spaceship.turn_left()
        spaceship.move_forward()
        distance1=self.distance_objects(spaceship,target)
        self.action_try=1
        self.action_back(self.action_try,spaceship)
        #turn right and move_forward
        spaceship.turn_right()
        spaceship.move_forward()
        distance2=self.distance_objects(spaceship,target)
        self.action_try=2
        self.action_back(self.action_try,spaceship)
        #compare distance then return best action 
        if(min(distance0,distance1,distance2)==distance0):
            return (True,False,False,False)
        if(min(distance0,distance1,distance2)==distance1):
            return (True,True,False,False)
        if(min(distance0,distance1,distance2)==distance2):
            return (True,False,True,False)
        

    def choose_fire_direction(self,spaceship,target):   # choose the right fire direction
        angle_origin=spaceship.angle
        angle_abs=self.angle_abs_objects(spaceship,target)
        angle0=angle_abs
        angle1=(180-angle_abs)%360
        angle2=(180+angle_abs)%360
        angle3=(360-angle_abs)%360
        angles=[angle0,angle1,angle2,angle3]
        distance=[]
        #try 4 angles
        for angle in angles:
            spaceship.angle=angle
            spaceship.move_forward()
            distance.append(self.distance_objects(spaceship,target))
            self.action_back_for_fdc(spaceship,angle_origin)
        angle_true=angles[distance.index(min(distance))]
        return angle_true
            



   
            
        




    
            
        
    # You can add additional methods if required
