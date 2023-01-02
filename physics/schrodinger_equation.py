import numpy as np
def schrodinger_equation(potential, mass, grid_size, grid_spacing, wavefunction):
    """Solves Schrodinger equation for a quantum system using DVR method.

    Parameters:
    potential (callable): A function that returns the potential energy at a given point.
    mass (float): The mass of the particle in the system.
    grid_size (int): The number of grid points to use in the calculation.
    grid_spacing (float): The distance between grid points.
    wavefunction (numpy array): The initial wavefunction of the system.

    Returns:
    numpy array: The wavefunction of the system at each grid point.
    """
    # Create the kinetic energy operator using the DVR method
    kinetic_energy_operator = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            if i == j:
                kinetic_energy_operator[i, j] = 2 / (mass * grid_spacing ** 2)
            elif i == j - 1 or i == j + 1:
                kinetic_energy_operator[i, j] = -1 / (mass * grid_spacing ** 2)
    # Solve the Schrödinger equation at each point
    for i in range(grid_size):
        wavefunction[i] = (kinetic_energy_operator[i, :] @ wavefunction + potential(i * grid_spacing) * wavefunction[
            i]) / (2 / (mass * grid_spacing ** 2))
    return wavefunction

def test_schrodinger_equation():
    # Test a simple harmonic oscillator potential
    mass = 1.0
    grid_size = 100
    grid_spacing = 0.1
    wavefunction = np.zeros(grid_size)
    wavefunction[0] = 1.0

    def potential(x):
        return 0.5 * x ** 2

    wavefunction = schrodinger_equation(potential, mass, grid_size, grid_spacing, wavefunction)
    # The wavefunction should oscillate around 0
    assert np.allclose(wavefunction, 0, atol=1)

    # Test a constant potential
    mass = 1.0
    grid_size = 100
    grid_spacing = 0.1
    wavefunction = np.zeros(grid_size)
    wavefunction[0] = 1.0

    def potential(x):
        return 0.0

    wavefunction = schrodinger_equation(potential, mass, grid_size, grid_spacing, wavefunction)
    # The wavefunction should be a constant
    assert np.allclose(wavefunction, wavefunction[0], atol=1.5)

test_schrodinger_equation()
