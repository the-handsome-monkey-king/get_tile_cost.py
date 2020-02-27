#!/usr/bin/env python
"""get_tile_cost.py

Get the cost of a W x H floor with w x h tiles given a cost
by the user."""

__author__ = "Ryan Morehouse"
__license__ = "MIT"

import sys
import math

def main():
    area_w = get_user_float("Please enter floor width: ")
    area_h = get_user_float("Please enter the floor height: ")
    tile_w = get_user_float("Please enter the tile width: ")
    tile_h = get_user_float("Please enter the tile height: ")
    use_subtiles = get_user_bool(
        "Can tiles be split into multiple tiles [y/n]: ")
    if( use_subtiles == 'n'):
        use_subtiles = False
    else:
        use_subtiles = True
    extra_tiles = get_user_int(
        "Please enter number of desired extra tiles: ")
    print("Please enter the cost per tile without dollar sign")
    cost_per_tile = get_user_float(
        "(Anything below 1 cent will be simply dropped): ")
    # store cost as an int of pennies
    cost_per_tile = round(cost_per_tile * 100)

    tiles = (int)(math.ceil(
        get_tiles(area_w, area_h, tile_w, tile_h, use_subtiles)))

    # add extra desired tiles
    total_tiles = (int)(tiles + extra_tiles)

    total_cost = (float)(cost_per_tile) * (float)(total_tiles) / 100.0

    print("Estimated tiles needed: {}".format(tiles))
    print("Extra tiles desired: {}".format(extra_tiles))
    print("Total tiles needed: {}".format(total_tiles))
    print("Cost per tile: {}".format((float)(cost_per_tile) / 100))
    print("Total estimated cost: {}".format(total_cost))

def get_user_float(msg):
    while(True):
        try:
            f = (float)(raw_input(msg))
            if f <= 0:
                raise ValueError
            return f
        except(ValueError):
            print("That response is invalid. Please try again.")

def get_user_int(msg):
    while(True):
        try:
            f = (int)(raw_input(msg))
            if f < 0:
                raise ValueError
            return f
        except(ValueError):
            print("That response is invalid. Please try again.")

def get_user_bool(msg):
    while(True):
        try:
            response = raw_input(msg)
            if response in ['y', 'n']:
                return response
            else:
                raise ValueError
        except:
            print("That response is invalid. Please try again.")


def get_tiles(area_w, area_h, tile_w, tile_h, use_subtiles):
    # if tiles fit area perfectly
    if (area_w % tile_w == 0 and area_h % tile_h == 0):
        x_tiles = area_w / tile_w
        y_tiles = area_h / tile_h
        tiles = x_tiles * y_tiles
        return tiles

    # if tiles fit one way perfectly
    elif (area_w % tile_w == 0):
        tiles = get_tiles_for_one_remaining_dimension(
            area_d = area_h, tile_d = tile_h,
            other_area_d = area_w, other_tile_d = tile_w,
            use_subtiles = use_subtiles)
        return tiles
    
    # if tiles fit the other way perfectly
    elif (area_h % tile_h == 0):
        tiles = get_tiles_for_one_remaining_dimension(
            area_d = area_w, tile_d = tile_w,
            other_area_d = area_h, other_tile_d = tile_h,
            use_subtiles = use_subtiles)
        return tiles
    
    # if there is remaining space on both sides
    else:
        # get tiles for one dimension first
        tiles = get_tiles_for_one_remaining_dimension(
            area_d = area_w, tile_d = tile_w,
            other_area_d = area_h, other_tile_d = tile_h,
            use_subtiles = use_subtiles)
        # get extra tiles for remaining dimension
        extra_tiles = get_tiles_for_last_dimension(
            area_d = area_h, tile_d = tile_h,
            other_area_d = area_w, other_tile_d = tile_w,
            use_subtiles = use_subtiles)

        tiles += extra_tiles
        return tiles

def get_tiles_for_one_remaining_dimension(area_d, tile_d,
        other_area_d, other_tile_d, use_subtiles):
    
    other_tile_count = math.ceil(other_area_d / other_tile_d)
    remaining_tile_count = math.floor(area_d / tile_d)

    if(use_subtiles == True):
        remaining_tile_count += 1
        tiles = other_tile_count * remaining_tile_count
        return tiles
    
    else:
        tiles = other_tile_count * remaining_tile_count

        remaining_d = area_d - (remaining_tile_count * tile_d)
        subtiles = math.floor(tile_d / remaining_d)
        extra_tiles = math.floor(other_tile_count / subtiles) +1
        tiles += extra_tiles
        return tiles

def get_tiles_for_last_dimension(area_d, tile_d,
        other_area_d, other_tile_d, use_subtiles):
    
    if (use_subtiles == True):
        extra_tiles = other_area_d / other_tile_d
        return extra_tiles
    else:
        remaining_d = area_d - (math.floor(area_d / tile_d) * tile_d)
        subtiles = math.floor(tile_d / remaining_d)
        extra_tiles = (math.floor(other_area_d / tile_d) / subtiles) +1
        return extra_tiles




if __name__ == "__main__":
    main()
