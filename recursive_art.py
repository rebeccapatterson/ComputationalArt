"""
RECURSIVE ART CODE 04-19-16.  DOES NOT NEED INPUTS. OUTPUT IS A RANDOMLY
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
    #all possible functions
    functions= {"x": lambda x,y: x,
                "y": lambda x,y: y,
                "cos_pi": lambda x: math.cos(math.pi*x),
                "sin_pi": lambda x: math.sin(math.pi*x),
                "squared": lambda x: x**2,
                "cubed": lambda x: x**3,
                "prod": lambda a,b: a*b,
                "avg": lambda a,b: (a+b)/2 }

    #connect function names to the number of arguments
    fn_args= {"x":0, "y":0, "cos_pi":1, "sin_pi":1, "squared":1, "cubed":1, "prod":2, "avg":2}
    #just look at the number of arguments
    fn_names= fn_args.keys()

    if max_depth==1:
    #if there can only be 1 more level, only look at function names for the 
    # functions with zero arguments and have no recursion
        fn_names= [fn for fn in fn_names if fn_args[fn]==0]

    elif min_depth>0:
    #if there is more than one level before minimum depth, only look at 
    # functions that take arguements and will recurse the function
        fn_names= [fn for fn in fn_names if fn_args[fn]>0]

    #randomly choose one of the function names specified through the if statements
    fn_name= random.choice(fn_names)
    #connect the function name to the actual function
    function= functions[fn_name]    

    #if the chosen function has no arguments, end recursion
    if fn_args[fn_name]==0:
        return function
    #if it has one argument
    elif fn_args[fn_name]==1:
        args= [build_random_function(min_depth-1, max_depth-1)]
    #otherwise it needs two arguments
    else:
        args= [build_random_function(min_depth-1, max_depth-1),
               build_random_function(min_depth-1, max_depth-1)]
    #recurse with number of arguments specified in if statements    
    return lambda x,y: function(*[arg(x,y) for arg in args])  


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
    value_1= float((val-input_interval_start))/interval_1
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
                    color_map(red_function(x, y)),
                    color_map(green_function(x, y)),
                    color_map(blue_function(x, y))
                    )
    im.save(filename)

#no new doctest were added because of reliance on random.randint.
if __name__ == '__main__':
    import doctest
#    doctest.testmod()

    # Create some computational art!
    generate_art("myart38.png")

    # Test that PIL is installed correctly
    # test_image("noise.png")