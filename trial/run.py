# -*- coding: utf-8 -*-


class RiemannRun(object):
    """
    Object containing data necessary for a single Riemann trial
    """
    
    def __init__(self, identifier, run_type):
        """Set necessary parameters (default values) for the run"""
        self.identifier = identifier #string identifying this run
        self.run_type = run_type     #1, 2 or 3;
        
        if run_type == 1:
            """Full Run"""
            
        elif run_type == 2:
            """Depth Tolerance"""
            self.roe_minimum_depth = 100.0
        elif run_type == 3:
            """Cone Condition"""
            self.roe_minimum_depth = 10.0
            self.roe_depth_fraction = 0.2
            self.roe_momentum_ratio = 0.25
        else:
            """Run type not recognized"""
            raise ValueError("Invalid run type: {}".format(run_type))
        pass
    
    
    def setup_directory(self):
        """
        Creates a run directory for this run, deleting one if it already exists,
        and copies/generates the neccessary files, based on the run type.
        """
        import os, shutil, glob
        
        run_directory_path = "runs/run_{}".format(self.identifier)
        
        #clear the run directory, if it already exists, then make a new one
        try:
            shutil.rmtree(run_directory_path)
        except OSError:
            pass
        os.mkdir(run_directory_path)
        
        #make directory for and copy source files for the run
        source_path = os.path.join(run_directory_path, "src")
        os.mkdir(source_path)
        
        #common fortran files
        for common_source in glob.glob(r'src/*.f*'):
            shutil.copy(common_source, source_path)
        
        #Riemann solver
        if self.run_type == 2:
            riemann_source = "src/riemann/roedeep/rpn2_geoclaw.f"
        elif self.run_type == 3:
            riemann_source = "src/riemann/roecone/rpn2_geoclaw.f"
        else:
            riemann_source = "src/riemann/full/rpn2_geoclaw.f"
        shutil.copy(riemann_source, source_path)
        
        #parameter file
        self.__generate_parameter_file(source_path)
        
        #copy run files
        run_files = ["Makefile", "setplot.py", "setrun.py"]
        for rf in run_files:
            shutil.copy("run_files/{}".format(rf), run_directory_path)
        
        #copy existing output directory
        output_path = os.path.join(run_directory_path, "_output")
        os.mkdir(output_path)
        restart_data_path = os.path.join(os.getcwd(), 'run_files',
                                         'restart_data','_output')
        if not os.path.exists(restart_data_path):
        	print 'Must run restart data run first.'
        	print 'Please execute run_tests.generate_restart_data()'
        	raise Exception('No Restart Data')
        for outdir_file in glob.glob(restart_data_path + '/*'):
            shutil.copy(outdir_file, output_path)
        
        
        #if all has gone well so far, set run directory strings
        self.run_directory_path = run_directory_path
        self.output_path = output_path
    
    
    def execute(self):
        """Command to do run"""
        import os
        old_directory = os.getcwd()
        os.chdir(self.run_directory_path)
        
        #execute in a new process
        os.system("make all >> console.out &")
        
        os.chdir(old_directory)
        
        
    
    def __generate_parameter_file(self, source_path):
        """
        Generates FORTRAN file to set parameters for the Riemann solver
        """
        import os
        
        #make code to set variables
        front_matter = [
            "subroutine hybrid_parameters()",
            "use amr_module, only: roe_depth_frac, roe_min_depth, roe_mom_rat"
        ]
        middle_matter = []
        end_matter = ["end subroutine"]
        
        #based on Riemann solver type, set parameters
        if self.run_type == 2:
            middle_matter.extend([
                "roe_min_depth = {}d0".format(self.roe_minimum_depth)
            ])
        elif self.run_type == 3:
            middle_matter.extend([
                "roe_depth_frac = {}d0".format(self.roe_depth_fraction),
                "roe_min_depth = {}d0".format(self.roe_minimum_depth),
                "roe_mom_rat = {}d0".format(self.roe_momentum_ratio)
            ])
        
        code = front_matter + middle_matter + end_matter
        
        #write code to file
        param_path = os.path.join(source_path, "hybrid_parameters.f90")
        with open(param_path, 'w') as param_file:
            for line in code:
                param_file.write(line + '\n')
        

if __name__ == "__main__":
    import os
    olddir =  os.getcwd()
    print olddir
    os.chdir("..")
    print os.getcwd()
    os.chdir(olddir)
    print os.getcwd()

