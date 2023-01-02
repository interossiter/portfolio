import numpy as np

def photoelectric_equation(frequency, work_function):
    """Calculates the kinetic energy of an emitted electron in the photoelectric effect.
    Parameters:
    frequency (float): The frequency of the incident light, in Hz.
    work_function (float): The work function of the material, in J.

    Returns:
    float: The kinetic energy of the emitted electron, in J.
    """

    # Planck's constant
    h = 6.62607015e-34
    # electron mass (kg)
    m = 9.1093837e-31
    # speed of light (m/s)
    c = 2.99792458e8

    # Calculate the kinetic energy using the photoelectric equation
    return work_function + h * frequency - (h * frequency) ** 2 / (2 * m * c ** 2)


def test_photoelectric_equation():
    # Test a low frequency
    frequency = 5e14
    work_function = 2.0
    kinetic_energy = photoelectric_equation(frequency, work_function)
    # The kinetic energy should be close to the work function
    assert np.isclose(kinetic_energy, work_function, rtol=1e-6)

    # Test a high frequency
    frequency = 5e16
    work_function = 2.0
    kinetic_energy = photoelectric_equation(frequency, work_function)
    # The kinetic energy should be significantly greater than the work function
    assert kinetic_energy >= work_function


test_photoelectric_equation()
