from math import *
import random

class helpers:
    @staticmethod
    def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
        '''Here, the red circle represents the measured position of the broken robot, 
        the blue arrow and line represent your chase robot, and the green turtle and 
        green line represent the true position of the broken robot.'''
        localized = False
        distance_tolerance = 0.01 * target_bot.distance
        ctr = 0
        N = 1000
        # if you haven't localized the target bot, make a guess about the next
        # position, then we move the bot and compare your guess to the true
        # next position. When you are close enough, we stop checking.
        #For Visualization
        import turtle    #You need to run this locally to use the turtle module
        window = turtle.Screen()
        window.bgcolor('white')
        size_multiplier= 25.0  #change Size of animation
        broken_robot = turtle.Turtle()
        broken_robot.shape('turtle')
        broken_robot.color('green')
        broken_robot.resizemode('user')
        broken_robot.shapesize(0.1, 0.1, 0.1)
        measured_broken_robot = turtle.Turtle()
        measured_broken_robot.shape('circle')
        measured_broken_robot.color('red')
        measured_broken_robot.resizemode('user')
        measured_broken_robot.shapesize(0.1, 0.1, 0.1)
        prediction = turtle.Turtle()
        prediction.shape('arrow')
        prediction.color('blue')
        prediction.resizemode('user')
        prediction.shapesize(0.1, 0.1, 0.1)
        prediction.penup()
        broken_robot.penup()
        measured_broken_robot.penup()
        #End of Visualization
        while not localized and ctr <= N:
            ctr += 1
            measurement = target_bot.sense()
            position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
            target_bot.move_in_circle()
            true_position = (target_bot.x, target_bot.y)
            error = helpers.distance_between(position_guess, true_position)
            if error <= distance_tolerance:
                print "You got it right! It took you ", ctr, " steps to localize."
                localized = True
            if ctr == N:
                print "Sorry, it took you too many steps to localize the target."
            #More Visualization
            measured_broken_robot.setheading(target_bot.heading*180/pi)
            measured_broken_robot.goto(measurement[0]*size_multiplier, measurement[1]*size_multiplier-200)
            measured_broken_robot.stamp()
            broken_robot.setheading(target_bot.heading*180/pi)
            broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-200)
            broken_robot.stamp()
            prediction.setheading(target_bot.heading*180/pi)
            prediction.goto(position_guess[0]*size_multiplier, position_guess[1]*size_multiplier-200)
            prediction.stamp()
            #End of Visualization
        return localized

    # A helper function you may find useful.
    @staticmethod
    def distance_between(point1, point2):
        """Computes distance between point1 and point2. Points are (x, y) pairs."""
        x1, y1 = point1
        x2, y2 = point2
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)