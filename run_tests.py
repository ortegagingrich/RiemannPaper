"""
Executes the CLAWPACK runs necessary for the comparisons of different Riemann
solvers with different parameters.
"""
from trial import run
import os


def set_environ():
	""" Set environment variables, etc. needed for run """
	riemann_paper_directory = os.getcwd()


def run_tests():
    """For now, just run a single test"""
    
    #Control (full solver)
    full = run.RiemannRun("full", 1)
    full.setup_directory()
    full.execute()
    
    #Roedeep (depth tolerance only)
    depths = []
    depths = [5.0, 10.0, 20.0, 40.0, 70.0, 100.0]
    for depth in depths:
        roedeep = run.RiemannRun("roedeep_{}".format(round(depth)), 2)
        roedeep.roe_minimum_depth = depth
        roedeep.setup_directory()
        roedeep.execute()
    
    #RoeCone (phase plane cone)
    params = [
        (10.0, 0.25, 0.2),
        (50.0, 0.50, 0.2),
        (10.0, 0.50, 0.2),
        (50.0, 0.25, 0.2),
        (10.0, 0.25, 0.4)
    ]
    for i in range(len(params)):
        param = params[i]
        roecone = run.RiemannRun("roecone_{}".format(i), 3)
        roecone.roe_minimum_depth = param[0]
        roecone.roe_momentum_ratio = param[1]
        roecone.roe_depth_fraction = param[2]
        roecone.setup_directory()
        roecone.execute()
    

def clear_runs():
    """Delete all test runs (i.e. to save space); be very careful before doing this"""
    pass


if __name__ == "__main__":
	#set_environ()
    run_tests()
