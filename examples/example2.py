from ga.population import *
from ga.strategy import *
from ga.operators import *
from ga.gene import *
from lambert_exponential_sinusoid import ExponentialSinusoidFamily
from poliastro.bodies import Sun
from poliastro.bodies import Earth
from ga.chromosome import *
from astropy import units as u

if __name__ == "__main__":

    test_cases = {
        "Earth-Mars":
            {
                "name": "Earth-Mars Transfer",
                "scalar": u.AU.to("m"),
                "mu": Sun.k.si.value,
                "r1": 1.0,
                "r2": 1.5,
                "psi": np.pi * 0.95
            },
        "Earth-Mercury":
            {
                "name": "Earth-Mercury Transfer",
                "scalar": u.AU.to("m"),
                "mu": Sun.k.si.value,
                "r1": 1.0,
                "r2": 0.74,
                "psi": np.pi
            },
        "LEO-GEO":
            {
                "name": "LEO-GEO Transfer",
                "scalar": (300 * 10 ** 3),
                "mu": Earth.k.si.value,
                "r1": 1.0,
                "r2": (35786 + 300) / 300,
                "psi": np.pi
            }
    }

    case = test_cases["LEO-GEO"]


    def fitness_function(winding_parameter, number_of_revolutions, initial_flight_path):
        try:
            sinusoid = ExponentialSinusoidFamily(winding_parameter, case["r1"], case["r2"], case["psi"],
                                                 number_of_revolutions)
            radial_distance = sinusoid.get_radial_distance_array(initial_flight_path)
            normalized_thrust = sinusoid.get_normalised_thrust_acceleration(initial_flight_path)
            cost = radial_distance * normalized_thrust
            if np.isnan(radial_distance).any():
                raise OverflowError
            return 100 - np.sum(abs(cost))
        except KeyboardInterrupt:
            pass
        except OverflowError:
            return -1e15
        except RuntimeWarning:
            return -1e15


    # Define the Chromosome which maps to a solution.
    ChromosomePart2 = Chromosome(
        [
            DenaryGeneFloat(limits=(0, 1), n_bits_exponent=1, n_bits_fraction=10, signed=False),  # k2
            DenaryGeneFloat(limits=(1, 16), n_bits_exponent=4, n_bits_fraction=None, signed=False),  # N
            DenaryGeneFloat(limits=(-0.3, 0.3), n_bits_exponent=1, n_bits_fraction=7, signed=True),  # gamm0
        ],
    )
    # Population definition
    population = Population(100, 100, ChromosomePart2)

    # Define termination class
    TerminationCriteriaOptim6 = TerminationCriteria()
    TerminationCriteriaOptim6.add_convergence_limit(0.1)  # Limit to 0.1% convergence in population.
    TerminationCriteriaOptim6.add_generation_limit(20)  # Limit to 100 Generations.

    # Evolutionary Strategy Tests
    EvolutionaryStrategyTest = EvolutionaryStrategy(population=population,
                                                    fitness_function=fitness_function,
                                                    crossover_function=CrossoverOperator.random_polygamous,
                                                    selection_function=SelectionOperator.supremacy,
                                                    termination_criteria=TerminationCriteriaOptim6.check,
                                                    mutation_rate=0.1,
                                                    )

    # Evolve for solution.
    EvolutionaryStrategyTest.evolve(verbose=True)

    # Retrieve fittest solution.
    sol = EvolutionaryStrategyTest.get_fittest_solution()[0]

    # Calculate polar-coordinates with inbuilt method.
    ExponentialSinusoidBest = ExponentialSinusoidFamily(sol[0], case["r1"], case["r2"], case["psi"], sol[1])

    _r_real = ExponentialSinusoidBest.get_radial_distance_array(sol[2], case["scalar"])

    a = ExponentialSinusoidBest.get_normalised_thrust_acceleration(sol[2])  # * (case["mu"] / (_r_real ** 2))

    theta = ExponentialSinusoidBest.get_theta_array()

    theta_dot = ExponentialSinusoidBest.get_theta_time_derivative(sol[2], case["mu"], case["scalar"])

    velocity = ExponentialSinusoidBest.test_velocity_array(sol[2], case["mu"], case["scalar"])

plt.figure(figsize=(7, 7), dpi=300)

ax = plt.subplot(111, projection='polar')
ax.set_title(case["name"] + "\n$k_2={};     $".format(np.round(sol[0], 2))
             + "$r_1={};      $".format(np.round(case["r1"], 2))
             + "$r_2={};      $".format(np.round(case["r2"], 2))
             + "$\phi={};     $".format(np.round(np.rad2deg(case["psi"]), 2))
             + "$N={};    $".format(sol[1])
             )
ax.plot(theta, _r_real, linewidth=2.0)
ax.grid(True)
# ax.set_title("Practicing with exponential sinusoids", va='bottom')
plt.show()

plt.figure(figsize=(7, 7), dpi=300)
plt.ylabel("Gravity Normalised Thrust [$\hat{N}$]")
plt.xlabel("True Anomaly [rad]")
plt.grid(which="both")
plt.title(case["name"] + "\n$k_2={};     $".format(np.round(sol[0], 2))
          + "$r_1={};      $".format(np.round(case["r1"], 2))
          + "$r_2={};      $".format(np.round(case["r2"], 2))
          + "$\phi={};     $".format(np.round(np.rad2deg(case["psi"]), 2))
          + "$N={};    $".format(sol[1])
          )
plt.plot(theta, a)
plt.show()

# Velocity
plt.figure(figsize=(7, 7), dpi=300)
plt.ylabel("Velocity (V) [m/s]")
plt.xlabel("True Anomaly [rad]")
plt.grid(which="both")
plt.title(case["name"] + "\n$k_2={};     $".format(np.round(sol[0], 2))
          + "$r_1={};      $".format(np.round(case["r1"], 2))
          + "$r_2={};      $".format(np.round(case["r2"], 2))
          + "$\phi={};     $".format(np.round(np.rad2deg(case["psi"]), 2))
          + "$N={};    $".format(sol[1])
          )
plt.plot(theta, velocity)
plt.show()

# plt.figure(figsize=(7, 7), dpi=300)
# plt.ylabel("Velocity (V) [m/s]")
# plt.xlabel("True Anomaly [rad]")
# plt.grid(which="both")
# plt.title(case["name"] + "\n$k_2={};     $".format(np.round(sol[0], 2))
#           + "$r_1={};      $".format(np.round(case["r1"], 2))
#           + "$r_2={};      $".format(np.round(case["r2"], 2))
#           + "$\phi={};     $".format(np.round(np.rad2deg(case["psi"]), 2))
#           + "$N={};    $".format(sol[1])
#           )
# bars = ax.bar(bins[:bins_number], n, width=width, bottom=0.0)
# plt.show()

degrees = np.random.randint(0, 360, size=200)
radians = np.deg2rad(degrees)

bin_size = 20

N = 36
import matplotlib.cm as cm

theta = theta % (2 * np.pi)
n = 10
thing = [np.sum(a[(theta > (i * 2 * np.pi / n)) & (theta < (i + 1) * 2 * np.pi / n)]) for i in
         np.linspace(0, 2 * np.pi, n)]
# width = np.pi / 4 * np.random.rand(N)
x = np.linspace(0, 2 * np.pi, 10) + 2 * np.pi / 20

plt.plot(x, thing)

plt.show()
