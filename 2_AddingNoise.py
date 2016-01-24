# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess 
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered 
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position. 
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random
from helpers import *

# This is the function you have to write. Note that measurement is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    
    # In order to make the noisy prediction, let's first reach the point
    #..of accurate prediction
    xy_estimate = [0,0]

    # All I need are three points of reference
    if OTHER == None:
        OTHER = [[None]*2 for i in range(5)]    # 3 points and h,b and turning angle
        OTHER[0] = measurement
        xy_estimate = measurement
    elif OTHER[1][0] == None:
        OTHER[1] = measurement
        xy_estimate = measurement
    else:
        if OTHER[2][0] == None:
            OTHER[2] = measurement
        else:
            OTHER[0] = OTHER[1]     # Keeping the latest 3 measurements
            OTHER[1] = OTHER[2]
            OTHER[2] = measurement
        xy_estimate = get_best_xy(OTHER)

    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    return xy_estimate, OTHER

def get_best_xy(OTHER):
    h = distance_between(OTHER[1], OTHER[2])    # Visualize the triangle(s)
    b = distance_between(OTHER[0], OTHER[2]) / 2

    # Averages
    temp = h
    if OTHER[3][0] != None:
        h = (OTHER[3][0] + h)/2
    OTHER[3][0] = temp

    temp = b
    if OTHER[3][1] != None:
        b = (OTHER[3][1] + b)/2
    OTHER[3][1] = temp

    f = b/h
    if f > 1:
        f = 1

    theta = acos(f)
    y = pi/2 - theta
    turning_angle = pi - 2*y

    # Take average
    temp = turning_angle
    if OTHER[4][0] != None:
        turning_angle = (OTHER[4][0] + temp)/2
    OTHER[4][0] = temp

    # And now is the time to perform some real action..
    # Find previous & current orientation and predict next pos using particle filters.
    d = 1   # Distance b/w particle and Traxbot's new positions
    count = 1000
    min_d = 100
    best_or = 0

    while d > 0.01 and count > 0:
        # Spawn a new particle at OTHER[1] and compare with OTHER[2]
        prev_orientation = random.random() * 2.0 * pi
        next_orientation = (prev_orientation + turning_angle) % (2*pi)
        new_x = OTHER[1][0] + h*cos(next_orientation)
        new_y = OTHER[1][1] + h*sin(next_orientation)
        d = distance_between([new_x,new_y], OTHER[2])

        if d < min_d:
            min_d = d
            best_or = next_orientation
        count -= 1
    else:
        new_orientation = (best_or + turning_angle) % (2*pi)
        new_x = OTHER[2][0] + h*cos(new_orientation)
        new_y = OTHER[2][1] + h*sin(new_orientation)
        return [new_x,new_y]


# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 1000:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 1000:
            print "Sorry, it took you too many steps to localize the target."
    return localized

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
measurement_noise = 0.05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)

from helpers import *
helpers.demo_grading(estimate_next_pos, test_target)
# Use local method instead for without visualization




