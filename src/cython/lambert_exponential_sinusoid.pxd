from eigency.core cimport *

cdef extern from "lambertExponentialSinusoid.h" namespace "tudat::mission_segments::low_thrust":
    cdef cppclass lambertExponentialSinusoid:
        # Constructors
        lambertExponentialSinusoid() except +
        lambertExponentialSinusoid(double, double, double, double, int) except +

        # Attributes
        double _windingParameter
        double _radialDistanceAtDeparture
        double _radialDistanceAtArrival
        double _psiAngleBetweenArrivalAndDeparture
        double _numberOfRevolutions

        # Methods
        double get_thetaBar()
        double get_dynamicRangeParameter(double)
        double get_phaseAngle(double)
        double get_scaleParameter(double)
        double get_bigDelta()

        Vector2d get_flightPathLimits()
        ArrayXd get_radialDistanceArray(double, double)
        ArrayXd get_flightPathArray(double)
        ArrayXd get_thetaArray()
        ArrayXd get_sArray(double)
        ArrayXd get_normalizedThrustAcceleration(double)
        ArrayXd get_thetaTimeDerivative(double, double, double)

