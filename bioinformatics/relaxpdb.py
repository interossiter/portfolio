# IMPORTANT:
# this code derived from http://docs.openmm.org/latest/userguide/application/03_model_building_editing.html
# there are TONS of important notes there to be reviewed describing these functions and params and how to tailor analysis
import sys
import time
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.openmm import unit
from sys import stdout

def main():

    tic = time.perf_counter()

    filein = sys.argv[1]
    fileout = sys.argv[2]
    ff_file = sys.argv[3]
    water_file =  sys.argv[4]

    print('filein = ' + filein)
    print('fileout = ' + fileout)
    print('force field = ' + ff_file)
    print('water model = ' + water_file)

    print('Loading...')
    pdb = PDBFile(filein)       #for PDB files
    #pdb = PDBxFile(filein)     #for mmCIF files

    forcefield = ForceField(ff_file, water_file)

#SPECIFY SYSTEM
    system = forcefield.createSystem(pdb.topology, nonbondedMethod=PME, nonbondedCutoff=1*unit.nanometer, constraints=HBonds)

#SELECT INTEGRATOR AND MINIMIZE ENERGY FOR SPECIFIED SYSTEM
    print('Selecting integrator and running simulation')
    integrator = LangevinMiddleIntegrator(300*unit.kelvin, 1/unit.picosecond, 0.004*unit.picoseconds)
    simulation = Simulation(pdb.topology, system, integrator)
    simulation.context.setPositions(pdb.positions)
    #simulation.minimizeEnergy(maxIterations=100)
    simulation.minimizeEnergy()

#GENERATE OUTPUTS
    print('Saving...')

#simple dump to one output file
    positions = simulation.context.getState(getPositions=True).getPositions()
    PDBFile.writeFile(simulation.topology, positions, open(fileout, 'w'))

    print('Done')
    toc = time.perf_counter()
    print(f"Elapsed time {toc - tic:0.1f} seconds")

if __name__ == '__main__':
    main()
