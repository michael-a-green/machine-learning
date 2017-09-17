import numpy as np
import random
import math
import pickle 


class Robot(object):
    def __init__(self, maze_dim, alpha = 0.5, epsilon = 1.0, gamma = 0.9, learning = False, verbose=False,training=False):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''

        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim
        self.VALID_ROTATIONS = [-90,0,90]
        self.timestep = 0
        self.internal_verbosity = verbose
        self.GOAL_BOUNDS = [self.maze_dim/2 - 1, self.maze_dim/2]
        self.last_movement = 0
        self.old_distance_factor = 0.0
        self.last_locations = []
        
        #flag to indicate in the previous timestep
        #the robot was in a corner and is turning out of it
        self.was_in_a_corner = 0
        
        #the number of times the robot reversed itself out of a corner
        self.reverse_count = 0
        
        #used to calculate new heading
        self.DIR_SENSORS = {'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
               'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
               'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
               'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}
        #used so that the robot can calcuation its current coordinates
        #in the maze
        self.DIR_MOVE = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
            'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}
            
        #used to come up with reverse heading
        self.DIR_REVERSE = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
               'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'}

        #variables used for Q-learning. Names have the same meaning
        # as the Q learning update equation
        #
        # Q(s,a) <-- Q(s,a) + alpha * (reward + gamma * max(a,Q(s',a) - Q(s,a))
        #
        self.ALPHA = alpha
        self.EPSILON = epsilon
        self.GAMMA = gamma
        self.Q = dict()
        self.learning = learning
        self.training = training
        
        #if not training read in previously trained pkl file into the Qtable
        if not(self.training):
            print "time=%0d reading in prevously trained pkl file"%(self.timestep)
            self.Q =   pickle.load( open("robot_Qtable.p","rb") )          

    
    def write_out_qtable(self):
        ''' Writes out contents of Qtable into a pkl file'''
        #everytime we hit the goal write out the Qtable in the form of a pkl file
        if self.internal_verbosity:
            print "time=%0d robot writing out Qtable"%(self.timestep)
            pickle.dump(self.Q, open('robot_Qtable.p',"wb"))

        
    def update_robot(self,sensors, current_location, current_heading, new_location, new_heading, movement, rotation):
        
        ''' This function implements state creation, Q-table initialization, reward
        calculate, and learning (updating action values given a (state,action) combintation
        '''
        
        #create a state value based on inputs (current_location, current_heading)
        temp_state = self.generate_state(current_location, current_heading)
        
        #update Q table with this state if it's new
        self.createQ(temp_state)
        
        #calculate reward. -1 if you moved to non-goal location, 10 if you entered
        #goal location
        temp_reward = self.calc_reward(new_location, current_location)
        
        #generate next state
        temp_next_state = self.generate_state(new_location, new_heading)
        
        #update action values using Q-learning
        self.learn(temp_state, temp_next_state, temp_reward, movement, rotation)

    def generate_state(self, location, heading):
        
        ''' State is just a tuple of (current location, current heading)
        In the form of a string '''
        
        temp_state = str(location) + " " + heading
        
        return temp_state

    
    def get_best_actions(self, state):
        ''' searches the q table for the actions with the highest action value and adds them to a list'''
        
        actions = []
        
        temp_maxQ = self.get_max_Q(state)
        
        for action in self.Q[state].keys():
            if self.Q[state][action] >= temp_maxQ:
                actions.append(action)
                    
        return actions

    def get_max_Q(self,state):
    
        temp_value = 0
        maxQ = 0;
        
        #check if state is in Q table. If not, return 0
        if not(state in self.Q.keys() ) :
            return 0.0

        qactions = self.Q[state].keys()
                
        for i in range(len(qactions)):
        
            if i == 0:
                temp_value = self.Q[state][qactions[i]]
            
            if self.Q[state][qactions[i]] > temp_value:
                temp_value = self.Q[state][qactions[i]]
        
        
        maxQ = temp_value
        return maxQ
    
    
    def distance_factor_to_goal(self,new_location):
        ''' creates a factor that is a function of distance to goal. The closer the distance the larger the number'''
        
        
        goal0X = self.maze_dim/2 - 1
        goal0Y = self.maze_dim/2 - 1
        goal1X = self.maze_dim/2 - 1
        goal1Y = self.maze_dim/2
        goal2X = self.maze_dim/2 
        goal2Y = self.maze_dim/2 
        goal3X = self.maze_dim/2
        goal3Y = self.maze_dim/2 - 1


        
        distance0 = math.sqrt(  (goal0Y - new_location[1])**2 + (goal0X - new_location[0])**2  )
        distance1 = math.sqrt(  (goal1Y - new_location[1])**2 + (goal1X - new_location[0])**2  )
        distance2 = math.sqrt(  (goal2Y - new_location[1])**2 + (goal2X - new_location[0])**2  )
        distance3 = math.sqrt(  (goal3Y - new_location[1])**2 + (goal3X - new_location[0])**2  )
        
        avg_distance = (distance0 + distance1 + distance2 + distance3)/4
        
        if (avg_distance > self.old_distance_factor):
            self.old_distance_factor = avg_distance
            return -2
        else:
            self.old_distance_factor = avg_distance
            return 0.1        
            
    def createQ(self, state):
        ''' Updates Q table as a side effect. returns None'''
    
        if self.learning:
            
            if self.Q.get(state) == None:
            
                temp_action_value = dict()
                
                for rotation in self.VALID_ROTATIONS:
                    for move in range(0,4):
                        #i want to discourage
                        #the robot from moving
                        #into reverse
                        if move >= 0:
                            temp_action_value[(rotation,move)] = 0.0
                        else:
                            temp_action_value[(rotation,move)] = -2.0
                
                self.Q[state] = temp_action_value
                
        return None
    
    def calc_reward(self,new_location, current_location):
    
        temp_reward = -1
    
        if new_location[0] in self.GOAL_BOUNDS and new_location[1] in self.GOAL_BOUNDS:        
            temp_reward = 10
        elif new_location == current_location:
            temp_reward = -10
        else:
            temp_reward = 1 + self.distance_factor_to_goal(new_location)
            
        #self.last_locations.append(new_location)
        
        return temp_reward
            
    def learn(self, state, nextstate, reward, movement, rotation):
    
        ''' Updates Q table as a side effect. Returns None'''
    
        if self.learning and (rotation,movement) != ('Reset','Reset'):
        
            temp = self.get_max_Q(nextstate)
            
            self.Q[state][(rotation,movement)] =   self.Q[state][(rotation,movement)] + \
                                                        self.ALPHA * (reward + self.GAMMA * self.get_max_Q(nextstate) - self.Q[state][(rotation,movement)])
                                                        
        return None
    
    #used by the robot to know
    #whether a movement is allowed based on
    #it's location and heading and sensory input
    # Needs to work when the robot is going forward or reverse
    def robot_is_allowed(self,current_rotation, sensors, reverse=False, last_movement = 0):
    
        #if the number of available spaces == 0 for the direction
        #it's heading, then it's not allowed otherwise it
        #is allowed one space
        
        if (reverse):
            #this is tough
            #sensors don't say how many squares are available in the opposite direction.
            #a guess is the last number of movements made
            #
            if last_movement > 0:
                return True
            else:
                return False
        else:
            if self.get_sensor_value_for_possible_rotation(current_rotation,sensors) == 0:
                return False
            else:
                return True
        
        return True
        

    #calculates new location based on several inputs
    #returns a list of [x,y] coordinates representing new location
    def calc_new_location(self, 
                        movement, #how many moves robot plans to make
                        sensors,  #sensory input for current location
                        current_heading, #which way it's pointed before doing its move
                        current_rotation, #the rotation the robot has chosen 
                        current_location, #the current locatoin
                        last_movement  #how many moves the robot last took
                        ):
    
        #correct movement input which
        #may be off if robot is going into reverse
        temp_movement = max(min(int(movement), 3), -3)
        
        temp_location = list(current_location)
        
        temp_new_heading = self.calc_new_heading(current_heading, current_rotation)
        
        temp_max_you_can_move = self.get_sensor_value_for_possible_rotation(current_rotation,sensors) 
        
        
        #The location calculation fails
        #when the robot decides it wants to move
        #more spaces than is available per the
        #intended heading and the sensor input
        #this corrects for that
        if abs(temp_movement) > temp_max_you_can_move:
            
            if temp_movement > 0:
                temp_movement = temp_max_you_can_move
            else:
                temp_movement = -1 * temp_max_you_can_move
        
        while temp_movement:
            #moving forward
            if temp_movement > 0:
                if self.robot_is_allowed(current_rotation, sensors):
                    temp_location[0] += self.DIR_MOVE[temp_new_heading][0]
                    temp_location[1] += self.DIR_MOVE[temp_new_heading][1]
                    temp_movement -= 1
                else:
                    if (self.internal_verbosity):
                        print "time=%0d robot can't move with heading %0s and location %0s"%(self.timestep, temp_new_heading, current_location)
                    temp_movement = 0
                    return temp_location
            #moving in reverse
            else:
                temp_reverse_heading = self.DIR_REVERSE[temp_new_heading]
                if self.robot_is_allowed(current_rotation,sensors,True, last_movement):
                    temp_location[0] += self.DIR_MOVE[temp_reverse_heading][0]
                    temp_location[1] += self.DIR_MOVE[temp_reverse_heading][1]
                    temp_movement += 1
                else:
                    if (self.internal_verbosity):
                        print "time=%0d robot can't move with reverse heading %0s and location %0s"%(self.timestep, temp_reverse_heading, current_location)
                    temp_movement = 0
                    return temp_location
                    
        return temp_location
                

    #takes a possible rotation and says how many open spaces
    #there are in the new direction per the rotation
    def get_sensor_value_for_possible_rotation(self,rotation, sensors):
        if rotation == 0:
            #moving forward
            return sensors[1]
        elif rotation == 90:
            #moving to the right hand side
            return sensors[2]
        elif rotation == -90:
            #moving to the left hand size
            return sensors[0]
        else:
            print "robot received erroneous rotation = %0d!"%(rotation)
            
    def calc_new_heading(self,current_heading, rotation):
        #new heading
    
        if rotation == 'Reset':
            new_heading = "up"
        elif rotation == 0:
            new_heading = current_heading
        elif rotation == -90:
            new_heading =  self.DIR_SENSORS[current_heading][0]
        elif rotation == 90:
            new_heading = self.DIR_SENSORS[current_heading][2]
        else:
            print "ERROR: robot received invalid rotation = ", rotation
            print "       robot received inavlid heading = ",  current_heading
            
        return new_heading
    
        
    def do_constrained_random_action(self,sensors):
        ''' When the robot acts randomly it should not be
        purely random but act in a random way that is constrained
        by the realities of the maze. So we don't want the
        robot to suddendly drive in reverse when it could just
        move forward or to rotate into a corner. So when we
        want the robot to do a random action for exploration purposes
        let's make it do something random yet sane.
        
        Also when it gets into a corner, let's
        make it just rotation 180
        
        Returns (rotation,movement) action tuple
        
        ''' 
        
        #pick a rotation,movement pair that results in largest number of moves
        #without going backwards
        
        #find the rotation that enables you to move the furthest 
        constrained_rotations = [rotation for rotation in self.VALID_ROTATIONS if self.get_sensor_value_for_possible_rotation(rotation,sensors) == max(sensors)]
        
        constrained_rotation = random.choice(constrained_rotations)
        
        constrained_movement = self.get_sensor_value_for_possible_rotation(constrained_rotation,sensors)
        
        #sanitize it
        constrained_movement = max( min(constrained_movement, 3), -3 )
        
        #check if you are in a corner - sensor reading [0,0,0]
        all_three_are_zero = 1
        for thing in sensors:
            if thing != 0:
                all_three_are_zero = 0
                break          
        
        #If in a corner, better to turn completely around
        if all_three_are_zero:
            self.was_in_a_corner = 1
            constrained_movement = 0
            constrained_rotation = 90
            print "time=%0d robot facing into a corner. performing auto maneuver to get out of corner!"%(self.timestep)
            return (constrained_rotation,constrained_movement)
            
        if self.was_in_a_corner  == 1:
            #turn 1 more time to get out of the corner
            self.was_in_a_corner = 0
            constrained_movement = 0
            constrainted_rotation = 90
            print "time=%0d robot was facing into a corner. finishing auto maneuver to get out of corner!"%(self.timestep)
            return (constrained_rotation,constrained_movement)

        #IF not in a corner go in the direction with the largest number of
        #free squares (calculated above)
        
        print "time=%0d robot picking via constrained random choice rotation = %0d movement = %0d "%(self.timestep,constrained_rotation,constrained_movement)
        
        return (constrained_rotation,constrained_movement)
                            
        if self.internal_verbosity  and all_three_are_zero:
            print "time=%0d facing into a corner. going in reverse with movement = %0d!"%(self.timestep, -1 *  (self.last_movement + self.reverse_count))
         
        if self.internal_verbosity and len(max_rotations ) > 1 and all_three_are_zero == 0:
            print "time=%0d making random choice out of %0d possible rotations!"%(self.timestep,len(max_rotations ) )
            
                    
    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''
        
        # Description of sensor input
        # sensors is a lit with the following format
        # sensors = [<NUMBER_OF_OPEN_SQUARES_TO_THE_LEFT>,<NUMBER_OF_OPEN_SQUARES_AHEAD>,<NUMBER_OF_OPEN_SQUARES_TO_RIGHT>]
        
        rotation = 0
        movement = 0
        
        
        max_moves_to_make = 0
        max_rotation = 0
        
 
        
        #check to see if you are facing into a corder
        #if so, then all_three_are_zero == 1

        

        #heuristic:
        #if max_moves_to_make is 0 in all directions, then revers by number of moves made
        #in the last move
        
#         if (all_three_are_zero):
#             chosen_rotation = 0
#             chosen_movement = -1 * self.last_movement + -1 * self.reverse_count
#             self.reverse_count += 1
#         else:
#             chosen_rotation = random.choice(max_rotations)
#             if self.get_sensor_value_for_possible_rotation(chosen_rotation,sensors) > 3:
#                 chosen_movement = 3
#             elif self.get_sensor_value_for_possible_rotation(chosen_rotation,sensors) < -3:
#                 chosen_movement = -3
#             else:
#                 chosen_movement = self.get_sensor_value_for_possible_rotation(chosen_rotation,sensors)
#       

        #August 28 : things to try. Let it go back in reverse.
        
        if not(self.learning):
            #Just acting randomly
            chosen_rotation = random.choice(self.VALID_ROTATIONS)
            chosen_movement = random.choice(range(-3,4))
            print "time=%0d robot unconstrained randomly picks rotation and movement (%0d, %0d)"%(self.timestep, chosen_rotation, chosen_movement)
        else:
            #Will act randomly with probability epsilon otherwise picks
            #best action based on Q table
            temp_epsilon = self.EPSILON * 100
            temp_rand_epsilon = random.randint(1,100)
            
            if temp_rand_epsilon <= temp_epsilon:
                if sensors == [0,0,0] or self.was_in_a_corner == 1:
                    (chosen_rotation, chosen_movement) = self.do_constrained_random_action(sensors)
                else:
                    chosen_rotation = random.choice(self.VALID_ROTATIONS)
                    chosen_movement = random.choice(range(0,4))
                    print "time=%0d robot randomly picks rotation and movement"%(self.timestep)
            else:
                if self.was_in_a_corner:
                     (chosen_rotation, chosen_movement) = self.do_constrained_random_action(sensors)
                else:
                    if sensors == [0,0,0] or self.was_in_a_corner == 1:
                        (chosen_rotation, chosen_movement) = self.do_constrained_random_action(sensors)
                    else:
                        temp_state =  self.generate_state(self.location, self.heading)
                        self.createQ(temp_state)
                        #best_actions = [(rot,mov) for rot in self.VALID_ROTATIONS for mov in range(0,4) if self.Q[temp_state][(rot,mov)] == self.get_max_Q(temp_state)]
                        best_actions = self.get_best_actions(temp_state)
                        if len(best_actions) == 0:
                            (chosen_rotation, chosen_movement) = (0,0)
                        else:
                            (chosen_rotation, chosen_movement) =  random.choice(best_actions)
                        print "time=%0d robot picks rotation and movement from Q-learning "%(self.timestep)
        
        if self.internal_verbosity:
            print "time=%0d robot internally calculated current location = %0s"%(self.timestep, self.location)
        
        
        temp_current_location = self.location
        
        self.location = self.calc_new_location( 
                                                chosen_movement, #how many moves robot plans to make
                                                sensors,  #sensory input for current location
                                                self.heading, #which way it's pointed before doing its move
                                                chosen_rotation, #the rotation the robot has chosen 
                                                self.location, #the current locatoin
                                                self.last_movement  #how many moves the robot last took
                        )
        
        temp_new_location = self.location
 
         #Do I still need this??? It's screwing up update_robot()        
#        if (self.location == temp_current_location):
#            chosen_movement = 0
            
        
        if self.internal_verbosity:
            print "time=%0d robot predicted new location = %0s"%(self.timestep, self.location)
            
        #pick only valid movement values
        self.last_movement = chosen_movement
        
        #If new location is in the goal space, then sent ('Reset','Reset')
        if temp_current_location[0] in self.GOAL_BOUNDS and temp_current_location[1] in self.GOAL_BOUNDS:
        
            chosen_movement = 'Reset'
            chosen_rotation = 'Reset'
            self.location = [0,0]
            
            print "time=%0d robot HIT GOAL with location %0s"%(self.timestep, temp_current_location)
            
            print "time=%0d resetting location back to self.location =  %0s"%(self.timestep, self.location)
            
        
        movement = chosen_movement
        rotation = chosen_rotation                            

        
        #new heading
        current_heading = self.heading
        self.heading = self.calc_new_heading(current_heading, rotation)
        
        if rotation == 'Reset':
            print "time=%0s resetting self.heading = %0s"%(self.timestep, self.heading)
            
    
        self.update_robot(sensors, temp_current_location, current_heading, temp_new_location, self.heading, chosen_movement, chosen_rotation)

    
        if self.internal_verbosity:
        
            if (rotation == 'Reset'):
                print "time=%0d robot picks rotation = Reset"%(self.timestep)
            else:
                print "time=%0d robot picks rotation = %0d"%(self.timestep, rotation)
            print "time=%0d robot current heading = %0s new heading = %0s"%(self.timestep,current_heading, self.heading)
            if movement == 'Reset':
                print "time=%0d robot picks movement = Reset"%(self.timestep)
            else:
                print "time=%0d robot picks movement = %0d"%(self.timestep, movement)
            print "time=%0d robot epsilon = %.2f"%(self.timestep, self.EPSILON)
        
        
        
        #vary exploration/exploitation when training
        #differently than when running
        if self.training:
            self.EPSILON = abs( math.cos(0.03 * self.timestep) )
        else:
            self.EPSILON = abs( math.cos(0.03 * self.timestep) )
            #self.EPSILON -= 0.01 * self.EPSILON
        
        self.timestep = self.timestep + 1
        
        return rotation, movement



    
        
        
        

    
        