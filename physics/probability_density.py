import numpy as np

def probability_density(wavefunction):
    """Calculates the probability density of a wavefunction.

    Parameters:
    wavefunction (numpy array): The wavefunction of the system.

    Returns:
    numpy array: The probability density of the wavefunction at each point.
    """
    return np.conj(wavefunction) * wavefunction


def test_probability_density():
    # Test a wavefunction with constant probability density
    wavefunction = np.ones(100)
    density = probability_density(wavefunction)
    # The probability density should be a constant
    assert np.allclose(density, 1.0, atol=1e-6)

    # Test a wavefunction with alternating positive and negative values
    wavefunction = np.array([1.0, -1.0, 1.0, -1.0])
    density = probability_density(wavefunction)
    # The probability density should be a constant
    assert np.allclose(density, 1.0, atol=1e-6)


test_probability_density()
