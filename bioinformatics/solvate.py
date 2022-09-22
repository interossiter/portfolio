# IMPORTANT:
# this code derived from http://docs.openmm.org/latest/userguide/application/03_model_building_editing.html
# there are TONS of important notes there to be reviewed describing these functions and params and how to tailor analysis
import sys
import time
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.openmm import unit
import argparse
from sys import stdout

def main():

    tic = time.perf_counter()

    parser = argparse.ArgumentParser()
    parser.add_argument('--filein', help='Input PDB file path', required=True)
    parser.add_argument('--fileout', help='Output PDB file path', required=True)
    parser.add_argument('--fileout_system', help='Output system.xml file path', default='system.xml')
    parser.add_argument('--ff_file', help='Force field XML file path', default='amber99sb.xml')
    parser.add_argument('--water_file', help='Set your bar option string', default='tip3p.xml')
    parser.add_argument('--temp', help='Kelvin temp', type=float, default=310)
    parser.add_argument('--friction_coeff', help='friction_coeff', type=float, default=1) ## could be '1/s'
    parser.add_argument('--step_size', help='enter step size', type=float, default=0.002)
    #parser.add_argument('--print_every', help='enter', type=int, default=1000)
    #parser.add_argument('--total_steps', help='enter', type=int, default=3000)
    parser.add_argument('--box_x', help='enter', type=float, default=5.0)
    parser.add_argument('--box_y', help='enter', type=float, default=5.0)
    parser.add_argument('--box_z', help='enter', type=float, default=5.0)
    #parser.add_argument('--fix_res_first', help='enter', type=int, default=1)
    #parser.add_argument('--fix_res_last', help='enter', type=int, default=1)
    #parser.add_argument('--pull_res', help='enter', type=int, default=59159)
    #parser.add_argument('--force_left', help='enter', type=float, default=100.0)     #default -100kJ/nm
    #parser.add_argument('--force_right', help='enter', type=float, default=100.0)    #default 100kJ/nm
    parser.add_argument('--ionic_strength', help='enter', type=float, default=0.15)    #default 0.15

    args = parser.parse_args()

    print('filein = ' + args.filein)
    print('fileout = ' + args.fileout)
    print('fileout_system = ' + args.fileout_system)

    print('force field = ' + args.ff_file)
    print('water model = ' + args.water_file)
    print('temp = ' + str(args.temp))
    print('friction_coeff = ' + str(args.friction_coeff))
    print('step_size = ' + str(args.step_size))
    #print('print_every = ' + str(args.print_every))
    #print('total_steps = ' + str(args.total_steps))
    print('box_x = ' + str(args.box_x))
    print('box_y = ' + str(args.box_y))
    print('box_z = ' + str(args.box_z))
    #print('fix_res_first = ' + str(args.fix_res_first))
    #print('fix_res_last = ' + str(args.fix_res_last))
    #print('pull_res = ' + str(args.pull_res))
    #print('force_left = ' + str(args.force_left))
    #print('force_right = ' + str(args.force_right))
    print('ionic_strength = ' + str(args.ionic_strength))

    print('Loading...')
    pdb = PDBFile(args.filein)       #for PDB files
    #pdb = PDBxFile(filein)     #for mmCIF files

    forcefield = ForceField(args.ff_file, args.water_file)

    modeller = Modeller(pdb.topology, pdb.positions)

#SPECIFY CONAINER SHAPE / WATER BOX (many options)
    print('Adding solvent / container / water box')
    #modeller.addSolvent(forcefield, boxSize=Vec3(5.0, 3.5, 3.5)*unit.nanometers)    #square / RECTANGULAR box
    #modeller.addSolvent(forcefield, boxVectors=(avec, bvec, cvec))    #NON-RECTANGULAR box specify the three box vectors defining the unit cell
    #modeller.addSolvent(forcefield, padding=0.5*unit.nanometers)    #specify a PADDING DISTANCE
    #modeller.addSolvent(forcefield, numAdded=5000)  #specify NUMBER SOLVENT MOLECULES
    #modeller.addSolvent(forcefield, boxSize=Vec3(24.0, 6.0, 6.0)*unit.nanometers, ionicStrength=0.15*unit.molar)    #RECTANGULAR box 8x2x2 ratio fits 2X55.pdb
    modeller.addSolvent(forcefield, boxSize=Vec3(args.box_x, args.box_y, args.box_z)*unit.nanometers, ionicStrength=args.ionic_strength*unit.molar)    #RECTANGULAR box 8x2x2 ratio fits 2X55.pdb

#OPTIONAL SPECIFY IONIC STRENGHT
    #blood pH 7.4
    #blood ionic strength about 0.15 molar
    #modeller.addSolvent(forcefield, ionicStrength=0.1*molar)   #default is NaCl
    #modeller.addSolvent(forcefield, ionicStrength=0.1*molar, positiveIon='K+') #Specify IONS Allowed values for positiveIon are 'Cs+', 'K+', 'Li+', 'Na+', and 'Rb+'. Allowed values for negativeIon are 'Cl-', 'Br-', 'F-', and 'I-'.

    print('Building system')
    system = forcefield.createSystem(modeller.topology, nonbondedMethod=PME)

    x = XmlSerializer.serialize(system)
    f = open(args.fileout_system, 'w')
    f.write(x)
    f.close()

#SELECT INTEGRATOR AND MINIMIZE ENERGY FOR SPECIFIED SYSTEM
    print('Selecting integrator and running simulation')
    #integrator = VerletIntegrator(0.001*unit.picoseconds)
    #integrator = LangevinMiddleIntegrator(300*unit.kelvin, 1/unit.picosecond, 0.004*unit.picoseconds)
    integrator = LangevinIntegrator(args.temp*unit.kelvin, args.friction_coeff/unit.picosecond, args.step_size*unit.picoseconds)
    simulation = Simulation(modeller.topology, system, integrator)
    simulation.context.setPositions(modeller.positions)

#GENERATE OUTPUTS
    print('Saving...')

#simple dump to one output file
    positions = simulation.context.getState(getPositions=True).getPositions()
    PDBFile.writeFile(simulation.topology, positions, open(args.fileout, 'w'))

    print('Done')
    toc = time.perf_counter()
    print(f"Elapsed time {toc - tic:0.1f} seconds")

if __name__ == '__main__':
    main()
