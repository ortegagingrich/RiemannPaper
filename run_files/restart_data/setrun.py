"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

import os
import numpy as np


#------------------------------
def setrun(claw_pkg='geoclaw'):
#------------------------------

    """
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "geoclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData

    """

    from clawpack.clawutil import data

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    num_dim = 2
    rundata = data.ClawRunData(claw_pkg, num_dim)


    #------------------------------------------------------------------
    # Problem-specific parameters to be written to setprob.data:
    #------------------------------------------------------------------
    
    #probdata = rundata.new_UserData(name='probdata',fname='setprob.data')


    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------
    rundata = setgeo(rundata)

    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amr2ez.data for AMR)
    #------------------------------------------------------------------
    clawdata = rundata.clawdata  # initialized when rundata instantiated


    # Set single grid parameters first.
    # See below for AMR parameters.

    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.num_dim = num_dim

    # Lower and upper edge of computational domain:
    # note that x1,y1,x2,y2 are used in setting regions
    
    # SET "Computational Domain" (RED borders in Google Earth):
    
    clawdata.lower[0] = x1 = 231.0    # SET West longitude boundary
    clawdata.upper[0] = x2 = 237.0   # SET East longitude boundary

    clawdata.lower[1] = y1 = 39.0    # SET South latitude boundary
    clawdata.upper[1] = y2 = 49.0    # SET North latitude boundary

    # SET Level 1 Resolution = Number of grid cells: Coarsest grid
    clawdata.num_cells[0] = 7#int(x2-x1)  # SET Longitude resolution.  1 deg E-W cells  
    clawdata.num_cells[1] = 13#int(y2-y1)  # SET Latitude resolution.  1 deg N-S cells
    
    # SET Coarse run parameters
    #clawdata.num_cells[0] = 9  # SET coarse Longitude resolution.
    #clawdata.num_cells[1] = 5  # SET coarse Latitude resolution.

    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.num_aux = 4

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 2
    
    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0.0  # SET start time

    # Restart from checkpoint file of a previous run?
    # Note: If restarting, you must also change the Makefile to set:
    #    RESTART = True
    # If restarting, t0 above should be from original run, and the
    # restart_file 'fort.chkNNNNN' specified below should be in 
    # the OUTDIR indicated in Makefile.

    clawdata.restart = False               # True to restart from prior results
    clawdata.restart_file = 'fort.chk00025'  # File to use for restart data

    # -------------
    # Output times:
    #--------------

    # SET the times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = 1  # SET the style of the output

    if clawdata.output_style==1:
        # Output nout frames at equally spaced times up to tfinal:
        
        #tfinal_minutes = 1.9*60.+0.05   # SET end time (minutes)
        tfinal_minutes = 2.0*60
        t_out_minutes  = 30.
        clawdata.num_output_times = int(tfinal_minutes/t_out_minutes) # *** Integer only ?
        clawdata.tfinal           = tfinal_minutes*60.0
        clawdata.output_t0        = True     # output at initial (or restart) time?

    elif clawdata.output_style == 2:
        # Specify a list of output times.
        clawdata.output_times = [0.0,0.5,1.0,2.0,3,4,5,6,7,8,9,10]

    elif clawdata.output_style == 3:
        # Output every iout timesteps with a total of ntot time steps:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 3
        clawdata.output_t0 = True
        
    clawdata.output_format = 'binary'      # 'ascii' or 'binary' 

    clawdata.output_q_components = 'all'   # need all
    clawdata.output_aux_components = 'none'  # eta=h+B is in q
    clawdata.output_aux_onlyonce = False    # output aux arrays each frame


    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 4


    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==1: variable time steps used based on cfl_desired,
    # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
    clawdata.dt_variable = True

    # Initial time step for variable dt.
    # If dt_variable==0 then dt=dt_initial for all steps:
    clawdata.dt_initial = 1.0

    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99

    # Desired Courant number if variable dt used, and max to allow without
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.75
    clawdata.cfl_max = 1.0

    # Maximum number of time steps to allow between output times:
    clawdata.steps_max = 5000


    # ------------------
    # Method to be used:
    # ------------------

    # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
    clawdata.order = 2
    
    # Use dimensional splitting? (not yet available for AMR)
    clawdata.dimensional_split = 'unsplit'
    
    # For unsplit method, transverse_waves can be 
    #  0 or 'none'      ==> donor cell (only normal solver used)
    #  1 or 'increment' ==> corner transport of waves
    #  2 or 'all'       ==> corner transport of 2nd order corrections too
    clawdata.transverse_waves = 2

    # Number of waves in the Riemann solution:
    clawdata.num_waves = 3
    
    # List of limiters to use for each wave family:  
    # Required:  len(limiter) == num_waves
    # Some options:
    #   0 or 'none'     ==> no limiter (Lax-Wendroff)
    #   1 or 'minmod'   ==> minmod
    #   2 or 'superbee' ==> superbee
    #   3 or 'mc'       ==> MC limiter
    #   4 or 'vanleer'  ==> van Leer
    clawdata.limiter = ['mc', 'mc', 'mc']

    clawdata.use_fwaves = True    # True ==> use f-wave version of algorithms
    
    # Source terms splitting:
    #   src_split == 0 or 'none'    ==> no source term (src routine never called)
    #   src_split == 1 or 'godunov' ==> Godunov (1st order) splitting used, 
    #   src_split == 2 or 'strang'  ==> Strang (2nd order) splitting used,  not recommended.
    clawdata.source_split = 'godunov'


    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.num_ghost = 2

    # Choice of BCs at xlower and xupper:
    #   0 => user specified (must modify bcN.f to use this option)
    #   1 => extrapolation (non-reflecting outflow)
    #   2 => periodic (must specify this at both boundaries)
    #   3 => solid wall for systems where q(2) is normal velocity

    clawdata.bc_lower[0] = 'extrap'  # Longitude boundary
    clawdata.bc_upper[0] = 'extrap'  # Longitude boundary

    clawdata.bc_lower[1] = 'extrap'  # Latitude boundary
    clawdata.bc_upper[1] = 'extrap'  # Latitude boundary


    # --------------
    # Checkpointing:
    # --------------

    # Specify when checkpoint files should be created that can be
    # used to restart a computation.

    clawdata.checkpt_style = 2

    if clawdata.checkpt_style == 0:
        # Do not checkpoint at all
        pass

    elif clawdata.checkpt_style == 1:
        # Checkpoint only at tfinal.
        pass

    elif clawdata.checkpt_style == 2:
        # Specify a list of checkpoint times.  
        clawdata.checkpt_times = [60, 1.9*3600]

    elif clawdata.checkpt_style == 3:
        # Checkpoint every checkpt_interval timesteps (on Level 1)
        # and at the final time.
        clawdata.checkpt_interval = 5


    # ---------------
    # SET AMR parameters:
    # ---------------
    amrdata = rundata.amrdata
    
    # max number of refinement levels:
    # initial run use less levels to start  
    amrdata.amr_levels_max = 4  # SET Maximum number of refinement levels

    # Note: If use only 4 levels, the last two refinement ratios in the
    #       lists below are ignored
    
    # List of refinement ratios at each level (length at least mxnest-1)
    # Level 1 is 1 degree = 60' = 111.1 km = "Computational Domain", set above 
    # Level 2 is 6' = 360" = 11.1 km = 11,111 m
    # Level 3 is 1' = 60" = 1.85 km = 1850 m
    # Level 4 is 3.75" = 115.625 m
    
    #amrdata.refinement_ratios_x = [10,12,30]  # SET Levels 2,3, ... x Refinement ratios
    #amrdata.refinement_ratios_y = [10,12,30]  # SET Levels 2,3, ... y Refinement ratios
    #amrdata.refinement_ratios_t = [1,1,1]
    
    ratios = [10, 6, 15]
    amrdata.refinement_ratios_x = ratios
    amrdata.refinement_ratios_y = ratios
    
    #dummy, otherwise we get an error; uses automatic t refinement anyway
    amrdata.refinement_ratios_t = [1, 1, 1]

    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center','capacity','yleft','center']

    # Flag using refinement routine flag2refine rather than richardson error
    amrdata.flag_richardson = False    # use Richardson?
    amrdata.flag2refine = True

    # steps to take on each level L between regriddings of level L+1:
    amrdata.regrid_interval = 3

    # width of buffer zone around flagged points:
    # (typically the same as regrid_interval so waves don't escape):
    amrdata.regrid_buffer_width  = 3

    # clustering alg. cutoff for (# flagged pts) / (total # of cells refined)
    # (closer to 1.0 => more small grids may be needed to cover flagged cells)
    amrdata.clustering_cutoff = 0.700000

    # print info about each regridding up to this level:
    amrdata.verbosity_regrid = 0  

    #  ----- For developers ----- 
    # Toggle debugging print statements:
    amrdata.dprint = False      # print domain flags
    amrdata.eprint = False      # print err est flags
    amrdata.edebug = False      # even more err est flags
    amrdata.gprint = False      # grid bisection/clustering
    amrdata.nprint = False      # proper nesting output
    amrdata.pprint = False      # proj. of tagged points
    amrdata.rprint = False      # print regridding summary
    amrdata.sprint = False      # space/memory output
    amrdata.tprint = False      # time step reporting each level
    amrdata.uprint = False      # update/upbnd reporting
    
    # More AMR parameters can be set -- see the defaults in pyclaw/data.py

    # ---------------
    # SET the AMR Regions parameters: min and max resolution, time interval, extent
    # ---------------
    
    # See clawpack-5.2.2/WAcoast/python_tools/plotregions.py
    regions = rundata.regiondata.regions 
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2], the t1, t2 in seconds
    
    # List of refinement ratios at each level (length at least mxnest-1)
    # Level 1 is 1 degree = 60' = 111.1 km = "Computational Domain", set above 
    # Level 2 is 6' = 360" = 11.1 km = 11,111 m
    # Level 3 is 1' = 60" = 1.85 km = 1850 m
    # Level 4 is 3.75" = 115.625 m

    # SET Region 0 = Computational Domain + Extra Cells
    regions.append([1, 2, 0.*60., 1.e10, x1-1,x2+1,y1-1,y2+1])
    
    # SET Region 1 = Source
    #regions.append([2, 3, 0.*60., 120*60, -157.,-144.,54.,62.]) # alaska1964_ichinose.tt3
    regions.append([2, 3, 0*60., 1e10, -127,-123.5,max(39.5,y1),49.5]) # CSZ_L1.tt3

    # SET Region 2 = Medium (Rectangular) Computational Grids.  These must encompass
    #  the fixed grid areas, i.e., the FGmax grids, that may be more general
    #  quadrilateral shapes that are defined in script make_fgmax_grid.py
    #regions.append([3, 3, 120*60., 1e10, -124.5, -124.1, 47.1, 47.5])   # Walsh #11 Medium
    #Grays Harbor:
    regions.append([2,3,0*15*60,1e10,235.81,236.2,46.75,47.15])

    # Region 3 = Finest Computational Grid.  Shape & extent defined in script make_fgmax_grid.py 
    #regions.append([4, 4, 180*60.,1e10,-124.35,-124.15,47.25,47.35])  # Walsh #11 Fine    
    #Ocean Shores:
    regions.append([3,4,0*15*60,1e10,235.82,235.9,46.925,47.025])

    # ---------------
    # Gauges:
    # ---------------
    
    # SET gauge labels, positions, times
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]
    # rundata.gaugedata.add_gauge()
    
    #rundata.gaugedata.gauges.append([1101, -124.244725,  47.284000, 180.*60., 1.e10]) # SET Walsh #11
    #rundata.gaugedata.gauges.append([1102, -124.234, 47.284, 180.*60., 1.e10]) # SET Walsh #11
    #Ocean Shores
    #rundata.gaugedata.gauges.append([1101,-124.183139,47.015998,15.*60,1.e10])
    #Westport
    #rundata.gaugedata.gauges.append([1102,-124.132097,46.880604,15.*60,1.e10])
    #Aberdeen bridge
    #rundata.gaugedata.gauges.append([1103,-123.808347,46.972014,15.*60,1.e10])
    #east of Rennie Island
    #rundata.gaugedata.gauges.append([1104,-123.844931,46.957414,15.*60,1.e10])
    #Hoquiam
    #rundata.gaugedata.gauges.append([1105,-123.899454,46.970356,15.*60,1.e10])
    #Behind Westport
    #rundata.gaugedata.gauges.append([1106,-124.084365,46.886702,15.*60,1.e10])
    #Harbor mouth
    #rundata.gaugedata.gauges.append([1107,-124.128509,46.921531,15.*60,1.e10])

    return rundata
    # end of function setrun
    # ----------------------


#-------------------
def setgeo(rundata):
#-------------------
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    try:
        geo_data = rundata.geo_data
    except:
        print "*** Error, this rundata has no geo_data attribute"
        raise AttributeError("Missing geo_data attribute")
       
    # == Physics ==
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 2
    geo_data.earth_radius = 6367.5e3

    # == Forcing Options
    geo_data.coriolis_forcing = False

    # == Algorithm and Initial Conditions ==
    geo_data.sea_level = 0.0
    geo_data.dry_tolerance = 1.e-3
    geo_data.friction_forcing = True
    geo_data.manning_coefficient =.025
    geo_data.friction_depth = 1e6

    # Refinement settings
    refinement_data = rundata.refinement_data
    refinement_data.variable_dt_refinement_ratios = True
    refinement_data.wave_tolerance = 1.e-1
    refinement_data.deep_depth = 1e2
    refinement_data.max_level_deep = 3

    import os
    try:
        CLAW = os.environ['CLAW']
    except:
        raise Exception("Need to set CLAW environment variable")
        
    # == settopo.data values ==   
    # SET Path to topo files
    topo_data = rundata.topo_data
    # for topography, append lines of the form
    #    [topotype, minlevel, maxlevel, t1, t2, fname]
    
    #a hack to get to the topography files
    current_directory = os.getcwd()
    os.chdir('..')
    os.chdir('../data')
    topo_dir = os.path.join(os.getcwd(), 'topo')
    dtopo_dir = os.path.join(os.getcwd(), 'dtopo')
    os.chdir(current_directory)
    
    topo_file_1 = os.path.join(topo_dir, 'etopo1.tt3')
    topo_file_2 = os.path.join(topo_dir, 'N_GraysHarbor_1_3sec.tt3')
    
    dtopo_file = os.path.join(dtopo_dir, 'CSZ_L1.tt3')
    
    # SET N. Pacific topo
    topo_data.topofiles.append([3, 1, 4, 0., 1.e10, topo_file_1])
    
    #grays harbor topo file
    topo_data.topofiles.append([3,1,4,30.*60,1.e10, topo_file_2])

    
    # == setdtopo.data values ==
    # SET Path to dtopo (source) files
    dtopo_data = rundata.dtopo_data
    # for moving topography, append lines of the form :   (<= 1 allowed for now!)
    #   [topotype, minlevel,maxlevel,fname]
    # SET CSZ_L1.tt3
    dtopo_data.dtopofiles.append([3,1,3, dtopo_file])
    #rundata.dtopo_data.dt_max_dtopo = 1.0  # max time step while topo moving

    # == setqinit.data values ==
    rundata.qinit_data.qinit_type = 0
    rundata.qinit_data.qinitfiles = []
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [minlev, maxlev, fname]

    # == setfixedgrids.data values ==
    fixed_grids = rundata.fixed_grid_data
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]

    # == fgmax.data values ==
    
    # SET Fixed Grid (FG) parameters
    fgmax_files = rundata.fgmax_data.fgmax_files

    # rundata.fgmax_data.num_fgmax_val = 1  # SSET to ave depth only
    # rundata.fgmax_data.num_fgmax_val = 2  # SET to Save depth and speed
    rundata.fgmax_data.num_fgmax_val = 5  # SET to Save depth, speed, momentum, mom flux and min depth

    # SET Names of fixed grid files created by make_fgmax.py
    #fgmax_files.append('fgmax_grid11.txt')  # SET Walsh 11

    return rundata
    # end of function setgeo
    # ----------------------


if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys

    #execfile('make_fgmax.py')

    rundata = setrun(*sys.argv[1:])
    rundata.write()

    from clawpack.geoclaw import kmltools
    kmltools.regions2kml()
    kmltools.gauges2kml()
