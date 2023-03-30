#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 06:04:43 2023

@author: Maranda Mcdonald
"""
from PIL import Image, ImageDraw

def get_colors():
    '''
        Color Dictionary
        8 - BlackGray - The background
        5 - White - A reflect block
        6 - Black - A black block
        7 - transparent - A transparent block
        4 - Gray - A possible space for putting block
        0 - BlackGray - A place that could not have block

    **Returns**

        color_map: *dict, int, tuple*
              Matches grid information to a color
    '''
    return {
        8: (20, 20, 20),
        5: (255, 255, 255),
        6: (0, 0, 0),
        7: (255, 0, 0),
        0: (100, 100, 100),
        4: (50, 50, 50),
    }

def render_board(grid, laserList, pointGoalList, filename, dimensions=100):
    '''
   
    **Parameters**

        grid: *list, list, int*
            List of integer lists presenting a 2D represention of the parsed board file including
            the locations of fixed blocks, holes in the board where no blocks may be placed, and
            open spaces in the board where blocks can be placed

            0 = free space to place a block
            4 = hole in the board where a laser can pass through unimpeded but no block can be placed
            5 = Fixed reflective block
            6 = Fixed refractive block
            7 = Fixed opaque block

        laserList: *list, list, int*
            List of integer lists specifying the origin coordinates and trajectory of each laser beam. Each
            interior list represents one laser 'emitter'. The length of the outside/containing list holding
            the inside lists may be arbitrarily long but length of every inside list is exactly 4 elements.
            The first element of the inside list is the x orgin, the followed by the y origin, followed by 
            +/-1 for the x direction, then +/-1 for the y direction. Coordinate 0,0 is the top left.

            [[x_origin,y_origin,+-1,+-1]...]

        pointGoalList: *list, list, int*
            List of integer lists containing the coordinates of goal points that must have a laser pass
            through them. Each individual 2 element list contained within the outer list represents the
            x and y coordinate of a single point. There may be multiple points and so the number of lists
            contained in the outer list can be arbitrarily large, however each of these inner lists is
            exactly 2 elements. Coordinate 0,0 is the top left.

            [[x_coordinate,y_coordinate]...]

        blockList: *list, int*
            An integer list storing the type and number of every block available in the given bff file that
            can be moved to solve the board. The number of occurances of each element in the list represents
            the number of those blocks that are present. The value at each element indicates the type of block.

            1 = REFLECTIVE
            2 = REFRACTIVE
            3 = OPAQUE
    
        filename: *str*
            TThe desired name of the final .png file
            
        dimensions: *int*
            The dimensions of the board, where dimesnions=100 is a 100 x 100 pixel board

    ** Returns **

        A rendered image of the board containing blocks, lasers and holes. Saves as a .png
    '''

    nSizex = len(grid[0])
    nSizey = len(grid)
    dimx = nSizex * dimensions
    dimy = nSizey * dimensions
    colors = get_colors()

    img = Image.new("RGB", (dimx, dimy), color=0)

    
    for jy in range(nSizey):
        for jx in range(nSizex):
            x = jx * dimensions
            y = jy * dimensions

            for i in range(dimensions):
                for j in range(dimensions):
                    img.putpixel((x + i, y + j),
                                 colors[grid[jy][jx]])
    #To color y
    for i in range(nSizey - 1):
        y = (i + 1) * dimensions
        shape = [(0, y), (dimx, y)]
        img_new = ImageDraw.Draw(img)
        img_new.line(shape, fill=0 in colors.keys(), width=5)
    
    #to color x
    for i in range(nSizex - 1):
        x = (i + 1) * dimensions
        shape = [(x, 0), (x, dimy)]
        img_new = ImageDraw.Draw(img)
        img_new.line(shape, fill=0 in colors.keys(), width=5)
    
    #To color the lasers
    for i in range(len(laserList)):
        lazor_info = laserList[i]
        lazor_pos = (lazor_info[0], lazor_info[1])
        img_new = ImageDraw.Draw(img)
        img_new.ellipse([lazor_pos[0] * dimensions / 2 - 10, lazor_pos[1] * dimensions / 2 - 10,
                         lazor_pos[0] * dimensions / 2 + 10, lazor_pos[1] * dimensions / 2 + 10], fill=(255, 0, 0))

    
    #To color 
    for i in range(len(pointGoalList)):
        img_new.ellipse([pointGoalList[i][0] * dimensions / 2 - 10, pointGoalList[i][1] * dimensions / 2 - 10,
                         pointGoalList[i][0] * dimensions / 2 + 10, pointGoalList[i][1] * dimensions / 2 + 10], fill=(255, 255, 255), outline="red", width=2)

    #To name the image file
    if not filename.endswith(".png"):
        filename_new = '.'.join(filename.split(".")[0:-1])
        filename_new += "_solved.png"

    img.save("%s" % filename_new)


#This is an example of the info passed to save an image for dark1_.bff
fptr="dark_1.bff"
grid=[[4, 0, 0], [0, 0, 0], [0, 0, 4]]
laserList=[[3, 0, -1, 1], [1, 6, 1, -1], [3, 6, -1, -1], [4, 3, 1, -1]]
pointGoalList=[[0, 3], [6, 1]]
blockList=[3, 3, 3]

render_board(grid=grid,laserList=laserList,
                  pointGoalList=pointGoalList, filename=fptr)