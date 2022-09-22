import io
import sys
import time
from sys import stdout
import argparse
import uuid
from alphafold.relax import cleanup
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.openmm import unit

def main():

    print('START: READING PARAMS')
    tic = time.perf_counter()
    parser = argparse.ArgumentParser()

# PARAMS IN
    parser.add_argument('--working_folder', help='Working Folder', default='.')
    #parser.add_argument('--run_guid', help='UID for the run', required=True)

    parser.add_argument('--filein', help='Input PDB file path', required=True)
    # parser.add_argument('--fileout', help='Output PDB file path', required=True)
    parser.add_argument('--ff_file', help='Force field XML file path', default='amber99sb.xml')
    parser.add_argument('--water_file', help='Set your bar option string', default='tip3p.xml')
    parser.add_argument('--temp', help='Kelvin temp', type=float, default=310)
    parser.add_argument('--friction_coeff', help='Kelvin temp', type=float, default=1) ## could be '1/s'
    parser.add_argument('--step_size', help='enter step size', type=float, default=0.002)
    parser.add_argument('--print_every', help='enter', type=int, default=1000)
    parser.add_argument('--total_steps', help='enter', type=int, default=10000)
    parser.add_argument('--box_x', help='solvent box X dimension (nm)', type=float)
    parser.add_argument('--box_y', help='solvent box Y dimension (nm)', type=float)
    parser.add_argument('--box_z', help='solvent box Z dimension (nm)', type=float)
    parser.add_argument('--box_margin', help='solvent box margin (nm)', type=float, default=0.5)
    parser.add_argument('--fix_res_first', help='fix_res_first', type=int, default=1)
    parser.add_argument('--fix_res_last', help='fix_res_last', type=int, default=1)
    parser.add_argument('--pull_res', help='enter', type=int, default=9971)
    parser.add_argument('--force_left', help='enter', type=float, default=0.0)     #default -100kJ/nm
    parser.add_argument('--force_right', help='enter', type=float, default=10000.0)    #default 100kJ/nm
    parser.add_argument('--ionic_strength', help='enter', type=float, default=0.15)    #default 0.15

    args = parser.parse_args()

    print('working_folder = ' + args.working_folder)
    print('filein = ' + args.filein)
    # print('fileout = ' + args.fileout)
    print('force field = ' + args.ff_file)
    print('water model = ' + args.water_file)
    print('temp = ' + str(args.temp))
    print('friction_coeff = ' + str(args.friction_coeff))
    print('step_size = ' + str(args.step_size))
    print('print_every = ' + str(args.print_every))
    print('total_steps = ' + str(args.total_steps))

    if args.box_x==None or args.box_y==None or args.box_z==None:
        print('use default box')
        print('box_margin = ' + str(args.box_margin))
    else:
        print('box_x = ' + str(args.box_x))
        print('box_y = ' + str(args.box_y))
        print('box_z = ' + str(args.box_z))

    print('fix_res_first = ' + str(args.fix_res_first))
    print('fix_res_last = ' + str(args.fix_res_last))
    print('pull_res = ' + str(args.pull_res))
    print('force_left = ' + str(args.force_left))
    print('force_right = ' + str(args.force_right))
    print('ionic_strength = ' + str(args.ionic_strength))

# PRE-RUN PREPARATION
    guid = str(uuid.uuid1())
    print('guid = ' + guid)

# SAVE ARGS TO FILE
    f = open(args.working_folder + '/' + guid + '_args.txt', 'a')
    n = f.write('Script:' + sys.argv[0])
    n = f.write('NumberArgs:'+  str(len(sys.argv)))
    n = f.write('Args:' + str(sys.argv))
    f.close()

# PDB PREP
    print('PDB PREP')
    f = open(args.filein, "r")
    pdb_str = f.read()
    f.close()
    input_handle = io.StringIO(pdb_str)
    alterations = {}
    result = cleanup.fix_pdb(input_handle, alterations)

    pdbfixedfile = args.working_folder + '/' + guid + '_pdbfixed.pdb'
    f = open(pdbfixedfile, 'w')
    n = f.write(result)
    f.close()

# SYSTEM CREATE
    print('SYSTEM CREATE')
    pdb = PDBFile(pdbfixedfile)
    forcefield = ForceField(args.ff_file, args.water_file)
    modeller = Modeller(pdb.topology, pdb.positions)

    if args.box_x==None or args.box_y==None or args.box_z==None:
        modeller.addSolvent(forcefield, padding=args.box_margin*unit.nanometers)    #specify a PADDING DISTANCE
    else:
        modeller.addSolvent(forcefield, boxSize=Vec3(args.box_x, args.box_y, args.box_z)*unit.nanometers, ionicStrength=args.ionic_strength*unit.molar)    #RECTANGULAR box 8x2x2 ratio fits 2X55.pdb

    system = forcefield.createSystem(modeller.topology)

# ADD FORCES AND CONSTRAINTS
    print('ADD FORCES AND CONSTRAINTS')
    for i in range(args.fix_res_first, args.fix_res_last, 1):
        system.setParticleMass(i, 1e10*unit.amu)

#SPECIFY SYSTEM AND CUSTOM FORCE MODEL AND APPLY FORCE MODEL TO EACH PARTICLE
    print('SPECIFY SYSTEM AND CUSTOM FORCE MODEL AND APPLY FORCE MODEL TO EACH PARTICLE')
    external = CustomExternalForce('-fx*x-fy*y-fz*z')
    system.addForce(external)
    external.addPerParticleParameter('fx')
    external.addPerParticleParameter('fy')
    external.addPerParticleParameter('fz')
    external.addParticle(args.fix_res_first, (args.force_left, 0, 0)*unit.kilojoules_per_mole/unit.nanometer)
    external.addParticle(args.pull_res, (args.force_right, 0, 0)*unit.kilojoules_per_mole/unit.nanometer)

# SYSTEM SAVE TO XML
    print('SYSTEM SAVE TO XML')
    x = XmlSerializer.serialize(system)
    f = open(args.working_folder + '/' + guid + '_sys.xml', 'w')
    f.write(x)
    f.close()

# SELECT INTEGRATOR
    print('SELECT INTEGRATOR')
    integrator = LangevinIntegrator(args.temp*unit.kelvin, args.friction_coeff/unit.picosecond, args.step_size*unit.picoseconds)
    #integrator = GeodesicBAOABIntegrator()

# PLATFORM CREATE
    print('PLATFORM CREATE')
    platform = openmm.Platform.getPlatformByName('CUDA')
    properties = {'CudaPrecision': 'mixed'}
    properties['DeviceIndex'] = '0'
    #properties['DisablePmeStream'] = 'true'

# SIMULATION CREATE
    print('SIMULATION CREATE')
    simulation = Simulation(modeller.topology, system, integrator, platform)
    simulation.context.setPositions(modeller.positions)

# SIMULATION minimizeEnergy()
    print('SIMULATION minimizeEnergy()')
    f = open(args.working_folder + '/' + guid + '_energy.txt', 'a')
    energy = simulation.context.getState(getEnergy=True).getPotentialEnergy()
    f.write(str(energy))

    #simulation.minimizeEnergy(maxIterations=100)
    simulation.minimizeEnergy()

    energy = simulation.context.getState(getEnergy=True).getPotentialEnergy()
    f.write(str(energy))
    f.close()

#report results to output
    simulation.reporters.append(PDBReporter(args.working_folder + '/' + guid + '.pdb', args.print_every))     #report to PDB out every n steps
    simulation.reporters.append(StateDataReporter(stdout, args.print_every, step=True, potentialEnergy=True, temperature=True))
    simulation.step(args.total_steps)      #how many simulation steps to run

# SAVE / SERIALIZE OBJECTS
    print('SAVE / SERIALIZE OBJECTS')
    simulation.saveState(args.working_folder + '/' + guid + '_sim.xml')

    print('Done')
    toc = time.perf_counter()
    print(f"Elapsed time {toc - tic:0.1f} seconds")

if __name__ == '__main__':
    main()
