# Makefile for Clawpack code in this directory.
# This version only sets the local files and frequently changed
# options, and then includes the standard makefile pointed to by CLAWMAKE.
CLAWMAKE = Makefile.common

# See the above file for details and a list of make options, or type
#   make .help
# at the unix prompt.


# Adjust these variables if desired:
# ----------------------------------

CLAW_PKG = geoclaw                  # Clawpack package to use
EXE = xgeoclaw                 # Executable to create
SETRUN_FILE = setrun.py        # File containing function to make data
OUTDIR = _output               # Directory for output
SETPLOT_FILE = setplot.py      # File containing function to set plots
PLOTDIR = _plots               # Directory for plots

OVERWRITE ?= True                   # False ==> make a copy of OUTDIR first
RESTART ?= True                  # Should = clawdata.restart in setrun

# make sure only one thread is used
OMP_NUM_THREADS = 1

# Environment variable FC should be set to fortran compiler, e.g. gfortran

# Compiler flags can be specified here or set as an environment variable
FFLAGS ?=

# ---------------------------------
# List of sources for this program:
# ---------------------------------

AMRLIB = $(CLAW)/amrclaw/src/2d
GEOLIB = $(CLAW)/geoclaw/src/2d/shallow

include Makefile.geoclaw

EXCLUDE_SOURCES = \

MODULES = \
  src/amr_module.f90 \
  src/gauges_module.f90 \

SOURCES = \
  src/amr2.f90 \
  src/hybrid_parameters.f90 \
  src/rpn2_geoclaw.f \
  src/check.f \
  src/restrt.f \
  $(CLAW)/riemann/src/rpt2_geoclaw.f \
  $(CLAW)/riemann/src/geoclaw_riemann_utils.f \

#-------------------------------------------------------------------
# Include Makefile containing standard definitions and make options:
include $(CLAWMAKE)

part:
	python make_fgmax.py
	nice -n7 $(MAKE) .output
	nice -n7 $(MAKE) plots

all:
	#python make_fgmax.py
	#echo $(SOURCES)
	nice -n7 $(MAKE) .output
	#python plot_fgmax.py
	nice -n7 $(MAKE) plots
	#$(MAKE) .htmls
