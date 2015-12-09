"""
Executes the CLAWPACK runs necessary for the comparisons of different Riemann
solvers with different parameters.
"""
from trial import run
import os


def download_data():
	""" Downloads topo and dtopo data """
	from data import data
	data.download_data()


def generate_restart_data():
	""" Do initial full run to generate restart data for trials """
	top_directory = os.getcwd()
	os.chdir('run_files/restart_data')
	
	print 'Attempting to generate restart run data'
	try:
		os.system('make .output')
	except:
		print 'Failed to generate restart run data'
		raise
	print 'Finished restart run'
	os.chdir(top_directory)
	


def run_tests():
    """For now, just run a single test"""
    download_data()
    generate_restart_data()
    
    runlist = []
    
    #Control (full solver)
    full = run.RiemannRun("full", 1)
    full.setup_directory()
    runlist.append(full)
    
    
    
    #Roedeep (depth tolerance only)
    #depths = [5.0, 10.0, 20.0]
    depths = [5.0, 10.0, 20.0, 40.0, 70.0, 100.0]
    for depth in depths:
        roedeep = run.RiemannRun("roedeep_{}".format(round(depth)), 2)
        roedeep.roe_minimum_depth = depth
        roedeep.setup_directory()
        runlist.append(roedeep)
    
    
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
        runlist.append(roecone)
    
    #determine number of processes to use (by default, use same number as OMP)
    try:
    	np = int(os.environ['OMP_NUM_THREADS'])
    except:
    	np = 1
    
    #execute all runs
    run.run_trials(runlist, n_processes=np)
    

def clear_runs():
    """Delete all test runs (i.e. to save space); be very careful before doing this"""
    pass


if __name__ == "__main__":
	#set_environ()
    run_tests()
