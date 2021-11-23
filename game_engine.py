import config
from space_object import SpaceObject

class Engine:
    def __init__(self, game_state_filename, player_class, gui_class):
        self.spaceshiplist=[] # used to store spaceship object
        self.asteroidslist=[] # used to store asteroid objects
        self.bulletslist=[] # used to store bullets objects
        self.upcomingasteroidslist=[] # used to store upcoming asteroid objects
        self.completeend=False # used to sign whether the game_state file is complete
        self.score=0
        self.fuel=0
        self.totalfuel=0  # used to store the beginning fuel
        self.import_state(game_state_filename)
        self.player = player_class()
        self.GUI = gui_class(self.width, self.height)
        self.fire=False     # used to sign whether spaceship fire 
        self.endgame=False  # used to sign whether the game should be ended
        self.fuelstage=0    # used in printing warning message
        self.bulletid=0     # used to store the bullet id should be 
    def import_state(self, game_state_filename):
        try:
            f=open(game_state_filename,'r')
        except FileNotFoundError:
            raise FileNotFoundError("Error: unable to open {}".format(game_state_filename))
        i=0
        stage=1
        count=0
        j=0
        line=f.readline().strip("\n")
        while(line):
            line=line.split()
            if(len(line)!=2):
                raise ValueError("Error: expecting a key and value in line {}".format(i+1)) #not consist of pair of value and key

            if(stage==1):       #check stage 1 data include line1~6
                rightkey=["width","height","score","spaceship","fuel","asteroids_count"]
                if(line[0]!=rightkey[i]):
                    raise ValueError("Error: unexpected key: {} in line {}".format(line[0],i+1)) # unexpected key
                line[1]=line[1].split(",")

                if(i!=3):        #check line1~3 5~6 situation
                    if(len(line[1])!=1):
                        raise ValueError("Error: invalid data type in line {}".format(i+1))   # invalid datatype of value
                    try:
                        line[1][0]=int(line[1][0])
                    except:
                        raise ValueError("Error: invalid data type in line {}".format(i+1)) # invalid datatype of value
                    #load map width and height
                    if(i==0):
                        self.width=line[1][0]
                    if(i==1):
                        self.height=line[1][0]
                    if(i==2):
                        self.score=line[1][0]
                    if(i==4):
                        self.fuel=line[1][0]
                        self.totalfuel=line[1][0]
                    if(i==5):
                        count=line[1][0]
                        stage=2
                        i+=1  
                        line=f.readline().strip("\n")
                        continue

                if(i==3):           #check the spaceship data situation
                    if(len(line[1])!=4):
                        raise ValueError("Error: invalid data type in line {}".format(i+1))   # invalid datatype of value
                    try:
                        line[1][0]=float(line[1][0])
                        line[1][1]=float(line[1][1])
                        line[1][2]=int(line[1][2])
                        line[1][3]=int(line[1][3])
                    except:
                        raise ValueError("Error: invalid data type in line {}".format(i+1)) # invalid datatype of value
                    a=SpaceObject(line[1][0],line[1][1],self.width,self.height,line[1][2],line[0],line[1][3])
                    self.spaceshiplist.append(a)

            if(stage==2):       # check asteroids current
                if(line[0] != "asteroid_large" and line[0] != "asteroid_small"):
                    raise ValueError("Error: unexpected key: {} in line {}".format(line[0],i+1)) # unexpected key
                line[1]=line[1].split(",")
                if(len(line[1])!=4):
                        raise ValueError("Error: invalid data type in line {}".format(i+1))   # invalid datatype of value
                try:
                    line[1][0]=float(line[1][0])
                    line[1][1]=float(line[1][1])
                    line[1][2]=int(line[1][2])
                    line[1][3]=int(line[1][3])
                except:
                    raise ValueError("Error: invalid data type in line {}".format(i+1)) # invalid datatype of value
                b=SpaceObject(line[1][0],line[1][1],self.width,self.height,line[1][2],line[0],line[1][3])
                self.asteroidslist.append(b)
                j+=1
                if(j==count):
                    stage=3
                    j=0
                    line=f.readline().strip("\n")
                    i+=1
                    continue
                
            
            if(stage==3):   #check bullet count line
                if(line[0] != "bullets_count"):
                    raise ValueError("Error: unexpected key: {} in line {}".format(line[0],i+1)) # unexpected key
                line[1]=line[1].split(",")
                if(len(line[1])!=1):
                    raise ValueError("Error: invalid data type in line {}".format(i+1))   # invalid datatype of value
                try:
                    line[1][0]=int(line[1][0])
                except:
                    raise ValueError("Error: invalid data type in line {}".format(i+1)) # invalid datatype of value
                count=line[1][0]
                if(count==0):
                    stage=5
                else:
                    stage=4
                line=f.readline().strip("\n")
                i+=1
                continue
            
            if(stage==4):   #check bullets initially
                if(line[0] !="bullet"):
                    raise ValueError("Error: unexpected key: {} in line {}".format(line[0],i+1)) # unexpected key
                line[1]=line[1].split(",")
                if(len(line[1])!=4):
                        raise ValueError("Error: invalid data type in line {}".format(i+1))   # invalid datatype of value
                try:
                    line[1][0]=float(line[1][0])
                    line[1][1]=float(line[1][1])
                    line[1][2]=int(line[1][2])
                    line[1][3]=int(line[1][3])
                except:
                    raise ValueError("Error: invalid data type in line {}".format(i+1)) # invalid datatype of value
                c=SpaceObject(line[1][0],line[1][1],self.width,self.height,line[1][2],line[0],line[1][3])
                self.bulletslist.append(c)
                j+=1
                if(j==count):
                    stage=5
                    j=0
                    line=f.readline().strip("\n")
                    i+=1
                    continue
            
            if(stage==5):   #check upcoming asteroids count line
                if(line[0] != "upcoming_asteroids_count"):
                    raise ValueError("Error: unexpected key: {} in line {}".format(line[0],i+1)) # unexpected key
                line[1]=line[1].split(",")
                if(len(line[1])!=1):
                    raise ValueError("Error: invalid data type in line {}".format(i+1))   # invalid datatype of value
                try:
                    line[1][0]=int(line[1][0])
                except:
                    raise ValueError("Error: invalid data type in line {}".format(i+1)) # invalid datatype of value
                count=line[1][0]
                if(count==0):
                    self.completeend=True
                stage=6
                line=f.readline().strip("\n")
                i+=1
                continue

            if(stage==6):   #check upcoming asteroids 
                if(line[0] != "upcoming_asteroid_large" and line[0] != "upcoming_asteroid_small"):
                    raise ValueError("Error: unexpected key: {} in line {}".format(line[0],i+1)) # unexpected key
                line[0]=line[0].strip('upcoming_')  # delete the upcoming_ to fit the config.py
                line[1]=line[1].split(",")
                if(len(line[1])!=4):
                        raise ValueError("Error: invalid data type in line {}".format(i+1))   # invalid datatype of value
                try:
                    line[1][0]=float(line[1][0])
                    line[1][1]=float(line[1][1])
                    line[1][2]=int(line[1][2])
                    line[1][3]=int(line[1][3])
                except:
                    raise ValueError("Error: invalid data type in line {}".format(i+1)) # invalid datatype of value
                d=SpaceObject(line[1][0],line[1][1],self.width,self.height,line[1][2],line[0],line[1][3])
                self.upcomingasteroidslist.append(d)
                j+=1
                if(j==count):
                    self.completeend=True
                    j=0

            line=f.readline().strip("\n")
            i+=1
        if(not self.completeend):
            raise ValueError("Error: game state incomplete")
        f.close()


    def export_state(self, game_state_filename):
        
        # Enter your code here
        
        f=open(game_state_filename,'w')
        f.write("width {}\n".format(self.width))
        f.write("height {}\n".format(self.height))
        f.write("score {}\n".format(self.score))
        f.write("spaceship {:.1f},{:.1f},{},{}\n".format(self.spaceshiplist[0].x,self.spaceshiplist[0].y,self.spaceshiplist[0].angle,self.spaceshiplist[0].id))
        f.write("fuel {}\n".format(self.fuel))
        f.write("asteroids_count {}\n".format(len(self.asteroidslist)))
        for asteroid in self.asteroidslist:
            f.write("{} {:.1f},{:.1f},{},{}\n".format(asteroid.obj_type,asteroid.x,asteroid.y,asteroid.angle,asteroid.id))
        f.write("bullets_count {}\n".format(len(self.bulletslist)))
        for bullet in self.bulletslist:
            f.write("{} {:.1f},{:.1f},{},{}\n".format(bullet.obj_type,bullet.x,bullet.y,bullet.angle,bullet.id))
        f.write("upcoming_asteroids_count {}\n".format(len(self.upcomingasteroidslist)))
        for asteroid in self.upcomingasteroidslist:
            f.write("{} {:.1f},{:.1f},{},{}\n".format("upcoming_"+asteroid.obj_type,asteroid.x,asteroid.y,asteroid.angle,asteroid.id))
        f.close()
        

    def run_game(self):
        
        while True:
            # 1. Receive player input
            action=self.player.action(self.spaceshiplist[0],self.asteroidslist,self.bulletslist,self.fuel,self.score)
            # 2. Process game logic
            if(action[1] and not action[2]):  #turn left
                self.spaceshiplist[0].turn_left()
            if(action[2] and not action[1]): # turn right
                self.spaceshiplist[0].turn_right()
            if(action[0]): # move forward
                self.spaceshiplist[0].move_forward()    # update spaceship location
            for object in self.asteroidslist:  # update asteroids location
                object.move_forward()
            #update bullets
            if(action[3]): # fire
                if(self.fuel<config.shoot_fuel_threshold):
                    print("Cannot shoot due to low fuel")
                else:               #shoot a new bullet
                    c=SpaceObject(self.spaceshiplist[0].x,self.spaceshiplist[0].y,self.width,self.height,self.spaceshiplist[0].angle,"bullet",self.bulletid)
                    self.fire=True
                    self.bulletid+=1
                    self.bulletslist.append(c)
            for bullet in self.bulletslist:     #remove expired bullets
                if(bullet.count==0):
                    self.bulletslist.remove(bullet)
            for bullet in self.bulletslist:         #update bullets location and life
                bullet.move_forward()
                bullet.count-=1
            #deduct fuel
            fuelwarning=[config.fuel_warning_threshold[0]/100,config.fuel_warning_threshold[1]/100,config.fuel_warning_threshold[2]/100,0]
            if(self.fire):
                self.fuel-=config.bullet_fuel_consumption
            self.fuel-=config.spaceship_fuel_consumption
            if(self.fuel<=self.totalfuel*fuelwarning[self.fuelstage]):
                if(self.fuel!=0):
                    print("{:.0%} fuel warning: {} remaining".format(fuelwarning[self.fuelstage],self.fuel))
                self.fuelstage+=1
            self.fire=False
            
            #detect collisions
            collisioncount=0
            asteroidsdellist=[]
            bulletsdellist=[]
            #bullet collision
            for asteroid in self.asteroidslist:
                for bullet in self.bulletslist:
                    if(bullet.collide_with(asteroid)):
                        if(asteroid.obj_type=="asteroid_small"):
                            self.score+=config.shoot_small_ast_score
                        if(asteroid.obj_type=="asteroid_large"):
                            self.score+=config.shoot_large_ast_score
                        print("Score: {} \t [Bullet {} has shot asteroid {}]".format(self.score,bullet.id,asteroid.id))
                        bulletsdellist.append(bullet)
                        asteroidsdellist.append(asteroid)
                        collisioncount+=1
                        break
            for adel in asteroidsdellist:
                self.asteroidslist.remove(adel)
            for bdel in bulletsdellist:
                self.bulletslist.remove(bdel)
            #spaceship collision

            for asteroid in self.asteroidslist:
                if(self.spaceshiplist[0].collide_with(asteroid)):
                    self.score+=config.collide_score
                    print("Score: {} \t [Spaceship collided with asteroid {}]".format(self.score,asteroid.id))
                    self.asteroidslist.remove(asteroid)
                    collisioncount+=1
                    break
                
            #replenish asteroids
            i=0
            while(i<collisioncount):
                if(len(self.upcomingasteroidslist)==0):
                    print("Error: no more asteroids available")
                    self.endgame=True
                    break
                else:
                    self.asteroidslist.append(self.upcomingasteroidslist[0])
                    print("Added asteroid {}".format(self.upcomingasteroidslist[0].id))
                    del self.upcomingasteroidslist[0]
                i+=1
            if(self.fuel==0):
                self.endgame=True
            if(self.endgame):
                break
            collisioncount=0
            
            # 3. Draw the game state on screen using the GUI class
            # self.GUI.update_frame(???)
            self.GUI.update_frame(self.spaceshiplist[0], self.asteroidslist, self.bulletslist, self.score, self.fuel)
        # Display final score
        self.GUI.finish(self.score)
    # You can add additional methods if required
