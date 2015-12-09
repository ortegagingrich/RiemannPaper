""" 
Handles retrieving data necessary for these runs 
Not meant to be imported, call directly from the shell.
"""

import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__))


def __download_topo__():
	""" Retrieves necessary topography files from the clawpack site """
	from clawpack.geoclaw import topotools
	from clawpack.clawutil.data import get_remote_file
	
	
	topo_dir = os.path.join(DATA_DIR, 'topo')
	print 'Downloading topo data to {}'.format(topo_dir)
	
	baseurl = 'http://depts.washington.edu/clawpack/geoclaw/topo/'
	
	etopo_fname = 'etopo1-230250035050.asc'
	etopo_url = baseurl + 'etopo/' + etopo_fname
	
	grays_harbor_fname = 'N_GraysHarbor_1_3sec.tt3'
	grays_harbor_url = baseurl + 'WA/' + grays_harbor_fname
	
	#retrieve files
	get_remote_file(grays_harbor_url, output_dir=topo_dir,
	                file_name=grays_harbor_fname)
	get_remote_file(etopo_url, output_dir=topo_dir, file_name=etopo_fname)
	
	#invert the etopofile
	etopo = topotools.Topography(os.path.join(topo_dir, etopo_fname))
	etopo.Z = -etopo.Z
	etopo.write(os.path.join(topo_dir,'etopo1.tt3'), topo_type=3)


def __download_dtopo__():
	""" Retrieves necessary earthquake source files from the clawpack site """
	from clawpack.clawutil.data import get_remote_file
	
	dtopo_fname = 'CSZ_L1.tt3'
	url = 'http://www.geoclaw.org/dtopo/CSZ/' + dtopo_fname
	dtopo_dir = os.path.join(DATA_DIR, 'dtopo')
	print 'Downloading dtopo data to {}'.format(dtopo_dir)
	
	#retrieve file
	get_remote_file(url, output_dir=dtopo_dir, file_name=dtopo_fname)


def download_data():
	""" Retrieves necessary topo and dtopo files from the clawpack site """
	__download_topo__()
	__download_dtopo__()


if __name__ == '__main__':
	download_data()
