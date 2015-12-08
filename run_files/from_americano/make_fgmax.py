"""
Create fgmax_grid.txt and fgmax_transect input files 
"""


from clawpack.geoclaw import fgmax_tools
import numpy


# Default values (might be changed below)

tstart_max =  0.       # when to start monitoring max values
tend_max = 120.0#1.e10       # when to stop monitoring max values
dt_check = 0.1         # target time (sec) increment between updating 
                       # max values
min_level_check = 4    # which levels to monitor max on
arrival_tol = 1.e-2    # tolerance for flagging arrival

# ======================== 
# Lat-Long grid on x-axis:

#Walsh 11

fg = fgmax_tools.FGmaxGrid()
fg.point_style = 2       # will specify a 2d grid of points

fg.x1 = -124.35
fg.y1 =  47.25
fg.x2 = -124.15
fg.y2 =  47.35

fg.nx = 200 # => .2 deg = 22.2 km / 200 = 111.11 m
fg.ny = 100  # => .1 deg = 11.1 km / 100 = 111.11 m

fg.tstart_max = tstart_max
fg.tend_max = tend_max
fg.dt_check = dt_check
fg.min_level_check = min_level_check
fg.arrival_tol = arrival_tol

fg.input_file_name = 'fgmax_grid11.txt'
fg.write_input_data()
