# distutils: language = c++

import numpy as np
from eigency.core cimport  *

from lambert_exponential_sinusoid cimport lambertExponentialSinusoid

cdef class ExponentialSinusoidFamily:
    cdef lambertExponentialSinusoid c_class

    def __cinit__(self,
                  double winding_parameter,
                  double radial_distance_at_departure,
                  double radial_distance_at_arrival,
                  double psi_angle_between_arrival_and_departure,
                  int number_of_revolutions):
        """
        
        :param winding_parameter: (k2)
        :param radial_distance_at_departure: (r1) 
        :param radial_distance_at_arrival: (r2)
        :param psi_angle_between_arrival_and_departure: (psi)
        :param number_of_revolutions: (N)
        :return: 
        """
        self.c_class = lambertExponentialSinusoid(winding_parameter,
                                                  radial_distance_at_departure,
                                                  radial_distance_at_arrival,
                                                  psi_angle_between_arrival_and_departure,
                                                  number_of_revolutions)

    @property
    def _winding_parameter(self):
        """
        Exponential sinusoid winding parameter (k2)
        :return:
        """
        return self.c_class._windingParameter

    @property
    def _radial_distance_at_departure(self):
        """
        :return: Exponential sinusoid winding parameter (k1) (double)
        """
        return self.c_class._radialDistanceAtDeparture

    @property
    def _radial_distance_at_arrival(self):
        """
        :return: Non-dimensionalised
        """
        return self.c_class._radialDistanceAtArrival

    @property
    def _psi_angle_between_departure_and_arrival(self):
        """

        :return:
        """
        return self.c_class._psiAngleBetweenArrivalAndDeparture

    @property
    def _n_revolutions(self):
        """

        :return:
        """
        return self.c_class._numberOfRevolutions

    def get_max_theta(self):
        """

        :return:
        """
        return self.c_class.get_thetaBar()

    def get_dynamic_range_parameter(self, initial_flight_path_angle)-> double:
        """
        :param initial_flight_path_angle: 
        :return: dynamic_range_parameter (k1)
        """
        return self.c_class.get_dynamicRangeParameter(initial_flight_path_angle)

    def get_phase_angle(self, initial_flight_path_angle)-> double:
        """
        :param initial_flight_path_angle: 
        :return: 
        """
        return self.c_class.get_phaseAngle(initial_flight_path_angle)

    def get_scale_parameter(self, initial_flight_path_angle)-> double:
        return self.c_class.get_scaleParameter(initial_flight_path_angle)

    def get_theta_array(self)-> np.ndarray:
        return ndarray(self.c_class.get_thetaArray())

    def get_radial_distance_array(self, initial_flight_path_angle, radial_distance_scale_factor=1)-> np.ndarray:
        return ndarray(self.c_class.get_radialDistanceArray(initial_flight_path_angle, radial_distance_scale_factor))

    def get_s_array(self, initial_flight_path_angle)-> np.ndarray:
        return ndarray(self.c_class.get_sArray(initial_flight_path_angle))

    def get_big_delta(self)-> double:
        return self.c_class.get_bigDelta()

    def get_flight_path_limits(self)-> double:
        # TODO: Clean this tuple cheat conversion.
        return tuple(ndarray(self.c_class.get_flightPathLimits()).flatten())

    def get_normalised_thrust_acceleration_array(self, initial_flight_path_angle)-> np.ndarray:
        # TODO: Refractor get_normalizedThrustAcceleration into get_normalizedThrustAccelerationArray in Cpp
        return ndarray(self.c_class.get_normalizedThrustAcceleration(initial_flight_path_angle))

    def get_flight_path_array(self, initial_flight_path_angle):
        return ndarray(self.c_class.get_flightPathArray(initial_flight_path_angle))

    def get_theta_time_derivative(self, initial_flight_path_angle, gravitational_parameter,
                                  radial_distance_scale_factor=1):
        return ndarray(self.c_class.get_thetaTimeDerivative(initial_flight_path_angle, gravitational_parameter,
                                                            radial_distance_scale_factor))

    # Prototyping
    # TODO: Investigate the correctness of this velocity and then implement it into C++.
    def test_velocity_array(self, initial_flight_path_angle, gravitational_parameter, radial_distance_scale_factor=1):
        _theta_derivative = self.get_theta_time_derivative(initial_flight_path_angle,
                                                           gravitational_parameter,
                                                           radial_distance_scale_factor)
        _r = self.get_radial_distance_array(initial_flight_path_angle,
                                            radial_distance_scale_factor)
        _fpa = self.get_flight_path_array(initial_flight_path_angle)
        return _r * _theta_derivative / np.cos(_fpa)
