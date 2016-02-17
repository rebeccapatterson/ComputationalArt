"""
RECURSIVE ART CODE 02-16-16.  DOES NOT NEED INPUTS. OUTPUT IS A RANDOMLY
GENERATED IMAGE.

@author: REBECCA PATTERSON
"""

import math

import random
from PIL import Image


def build_random_function(min_depth, max_depth):
	#no doctest created because the function uses random.randint, so outputs
	#cannot be predicted or tested.
    """ Builds a nested list that represents a function within specified 
        levels using internally defined building blocks.

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list

        Uses 8 building blocks to create function: 
            [["x"], ["y"], ["cos_pi", arg], ["sin_pi", arg], ["squared", arg], 
            "cubed", arg], ["prod", arg, arg], ["avg", arg, arg]]
        Where each instance of arg recurses the function and creates a
        new level.
    """
    if max_depth==1:   
    #if there can only be 1 more level, give block with zero arguments and
    #has no recursion
        random_number= random.randint(0, 1)
    #zero arguments ["x", "y"]
        if random_number==0:
            return ["x"]
        if random_number==1:
            return ["y"]
    elif min_depth>0:
    #if there is more than one level left before hitting minimum, give a 
    #building block that takes arguements that will recurse the function
    	random_number= random.randint(0, 5)
        #one arguement
        if random_number==0:
            return ["cos_pi", build_random_function(min_depth-1, max_depth-1)]
        if random_number==1:
            return ["sin_pi", build_random_function(min_depth-1, max_depth-1)]
        if random_number==2:
        	return ["squared", build_random_function(min_depth-1, max_depth-1)]
        if random_number==3: 
            return ["cubed", build_random_function(min_depth-1, max_depth-1)]        
        # two_arguements
        if random_number==4:
            return ["prod", build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
        if random_number==5:
            return ["avg", build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
    else:
    #if within the bounds of acceptable levels, can raturn any block
    	random_number= random.randint(0, 5)
    	#no arguments, will stop recursion
        if random_number==0:
            return ["x"]
        if random_number==1:
        	return ["y"] 
        #one arguements, will continue with recursion   	
        if random_number==2:
            return ["cos_pi", build_random_function(min_depth-1, max_depth-1)]
        if random_number==3:
            return ["sin_pi", build_random_function(min_depth-1, max_depth-1)]
        if random_number==4:
        	return ["squared", build_random_function(min_depth-1, max_depth-1)]
        if random_number==5:        
            return ["cubed", build_random_function(min_depth-1, max_depth-1)]        
        #two arguements, will continue with recursion   
        if random_number==6:
            return ["prod", build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
        if random_number==7:
            return ["avg", build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
 

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    #base case
    if f[0]== "x":
        return x
    if f[0]== "y":
        return y
    #evaluate with specified action and arguements. will recurse until
    #it reached base case and entire function has been evaluated.     
    if f[0]== "cos_pi":
    	return math.cos(math.pi*evaluate_random_function(f[1], x,y))
    if f[0]== "sin_pi":
    	return math.sin(math.pi*evaluate_random_function(f[1], x,y))
    if f[0]== "squared":
    	return (evaluate_random_function(f[1],x,y))**2
    if f[0]== "cubed":
        return (evaluate_random_function(f[1],x,y))**3
    if f[0]== "prod":
    	return (evaluate_random_function(f[1],x,y))* (evaluate_random_function(f[2],x,y))
    if f[0]== "avg":
        return 0.5* (evaluate_random_function(f[1],x,y) + evaluate_random_function(f[2],x,y))


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_interval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    interval_1= input_interval_end- input_interval_start
    interval_2= output_interval_end- output_interval_start
    value_1= float((input_interval_end-val))/interval_1
    value_2= value_1*interval_2+ output_interval_start
    return value_2


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


#no new doctest were added because of reliance on random.randint.
if __name__ == '__main__':
    import doctest
#    doctest.testmod()

    # Create some computational art!
    generate_art("myart11.png")

    # Test that PIL is installed correctly
    # test_image("noise.png")