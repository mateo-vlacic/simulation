import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import combinations

# Global Variables
gridsize=1500
edge=gridsize/2

eat_epsilon=2

def get_euclid_dist(p1, p2):
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)
def get_angle(p1, p2):
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    return np.arctan2(y2-y1, x2-x1)


class Creature:
    def __init__(self, x, y, speed, life_exp, sense_radius):
        self.x = x # x-location
        self.y = y # y-location
        self.speed = speed # Number of units it can move per timestep
        self.life_exp = life_exp
        self.sense_radius = sense_radius
        
        self.facing = 2*np.pi*random.random()
        self.age = 0
        self.hunger = 0
        self.alive = True
        
        self.hunger_display = ax.text(self.x, 
                                      self.y+25, 
                                      self.hunger)
        self.age_display = ax.text(self.x, 
                                   self.y-25, 
                                   self.age)
        self.sense_circle = plt.Circle((self.x, self.y),
                                       radius = self.sense_radius,
                                       fill = False,
                                       linewidth = 0.1)
        self.sense_circle_display = ax.add_patch(self.sense_circle)
        
    def step(self, new_dir, units):
        # Moves the creature by the specified units after turning them to face the new specified direction
        
        self.facing = new_dir

        delta_x = units * np.cos(self.facing)
        delta_y = units* np.sin(self.facing)

        self.x += delta_x
        self.y += delta_y

        self.x = max(min(self.x, edge), -edge)
        self.y = max(min(self.y, edge), -edge)
        
    def move(self):   
        if self.x == edge:
            turndir = random.uniform(3*np.pi/4, 5*np.pi/4)
        elif self.x == -edge:
            turndir = random.uniform(-np.pi/4, np.pi/4)%(2*np.pi)
        elif self.y == edge:
            turndir = random.uniform(5*np.pi/4, 7*np.pi/4)
        elif self.y == -edge:
            turndir = random.uniform(np.pi/4, 3*np.pi/4)
        else:
            if self.sense_food():
                turndir = self.sense_food()
            else:
                turndir = (self.facing + random.uniform(-np.pi/6, np.pi/6))%(2*np.pi)
        self.step(turndir, self.speed)
    
    def check_for_food(self):
        global food_set
        
        for food in food_set:
            if food.alive:
                dist = get_euclid_dist(self, food)
                if dist < eat_epsilon:
                    self.hunger = -1
                    food.alive = False
                    break

        self.hunger += 1
        
    def sense_food(self):
        global food_set
        if len(food_set) > 0:
            foodlist = [(get_euclid_dist(self, food), get_angle(self, food)) for food in food_set]
            foodlist.sort()
            if foodlist[0][0] <= self.sense_radius:
                return foodlist[0][1]

    def die(self):
        self.alive = False
        self.age_display.remove()
        self.hunger_display.remove()
        self.sense_circle_display.remove()
        
    def reproduce(self):
        global creature_set
        baby = Creature(x = self.x + random.uniform(50,100),
                        y = self.y + random.uniform(50,100),
                        speed = self.speed,
                        life_exp = self.life_exp,
                        sense_radius = self.sense_radius
                       )
        creature_set.append(baby)

    def update_visuals(self):
        self.hunger_display.set_position((self.x, self.y+25))
        self.hunger_display.set_text(self.hunger)
        self.age_display.set_position((self.x, self.y-25))
        self.age_display.set_text(self.age)
        self.sense_circle.center = self.x, self.y



class Food:
    def __init__(self, x, y):
        self.x = x # x-location
        self.y = y # y-location
        self.alive=True


def initialise(num_creatures, num_food):
    creature_set = [Creature(x = gridsize*random.random() - gridsize/2,
                             y = gridsize*random.random() - gridsize/2,
                             speed = 3,
                             life_exp = 500,
                             sense_radius = 300
                            ) for n in range(num_creatures)]
    food_set = [Food(gridsize*random.random() - gridsize/2,
                 gridsize*random.random() - gridsize/2) for n in range(num_food)]
    return creature_set, food_set




fig, ax = plt.subplots(figsize=(7,7))
ax.set_ylim(-edge, edge)
ax.set_xlim(-edge, edge)

creature_set, food_set = initialise(num_creatures=7,
                            num_food=20)

creature_x = [creature.x for creature in creature_set]
creature_y = [creature.y for creature in creature_set]
# time_left = [1 for creature in creature_set]

food_x = [food.x for food in food_set]
food_y = [food.y for food in food_set]

creature_field = ax.scatter(creature_x,
                            creature_y,
                            c='darkred')

food_field = ax.scatter(food_x, food_y, c='green')


def update_state(time):
    
    global creature_set
    global food_set
    
    if random.random() < 0.01:
        food_set.append(Food(gridsize*random.random() - gridsize/2,
                 gridsize*random.random() - gridsize/2))

    for creature in creature_set:
        if creature.age > creature.life_exp or creature.hunger > 200:
            creature.die()
            continue
        else:
            creature.age += 1
            creature.move()
            creature.check_for_food()
            if random.random() < 1/300:
                creature.reproduce()
            
    food_set = [food for food in food_set if food.alive]
    creature_set = [creature for creature in creature_set if creature.alive]

    creature_x = [creature.x for creature in creature_set]
    creature_y = [creature.y for creature in creature_set]
    
    food_x = [food.x for food in food_set]
    food_y = [food.y for food in food_set]

#     time_left = [(creature.life_exp - creature.age)/creature.life_exp for creature in creature_set]
    
    creature_field.set_offsets(np.array([creature_x,
                                         creature_y]).T)
#     creature_field.set_color(np.array([time_left,
#                               [t/2 for t in time_left],
#                               [t/2 for t in time_left]]).T)
    
    food_field.set_offsets(np.array([food_x, food_y]).T)
    
    for creature in creature_set:
        creature.update_visuals()

animation = FuncAnimation(fig, update_state, interval = 10)

plt.show()