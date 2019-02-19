/*    Copyright (c) 2010-2018, Delft University of Technology
 *    All rigths reserved
 *
 *    This file is part of the Tudat. Redistribution and use in source and
 *    binary forms, with or without modification, are permitted exclusively
 *    under the terms of the Modified BSD license. You should have received
 *    a copy of the license with this file. If not, please or visit:
 *    http://tudat.tudelft.nl/LICENSE.
 *
 *    References
 *      Izzo, D. (2006). Lambert's Problem for Exponential Sinusoids.
 *      Journal Of Guidance, Control, And Dynamics, 29(5), 1242-1245. doi: 10.2514/1.21796
 *
 *    Notes
 *      Code implementation by Geoffrey Garrett - geoffreygarrett@space.com
 *
 *
 *
 *
 *
 */

#include <Eigen/Core>
#include "Tudat/Mathematics/BasicMathematics/mathematicalConstants.h"

#ifndef TUDAT_LAMBERT_EXPONENTIAL_SINUSOID_H
#define TUDAT_LAMBERT_EXPONENTIAL_SINUSOID_H

namespace tudat {

    namespace mission_segments {

        namespace low_thrust {

            class lambertExponentialSinusoid {
            public:

                lambertExponentialSinusoid() {};

                // Constructor
                lambertExponentialSinusoid(
                        const double windingParameter,
                        const double radialDistanceAtDeparture,
                        const double radialDistanceAtArrival,
                        const double psiAngleBetweenArrivalAndDeparture,
                        const int numberOfRevolutions) {

                    // TODO: Add error catches to see if any solutions of this ExpSinusoid class exist for r1 & r2.
                    _windingParameter = windingParameter;
                    _radialDistanceAtDeparture = radialDistanceAtDeparture;
                    _radialDistanceAtArrival = radialDistanceAtArrival;
                    _psiAngleBetweenArrivalAndDeparture = psiAngleBetweenArrivalAndDeparture;
                    _numberOfRevolutions = numberOfRevolutions;
                    _pointsPerRadian = 100;
                }

                Eigen::ArrayXd get_radialDistanceArray(double initialFlightPathAngle, double radialDistanceScaleFactor);

//
                Eigen::ArrayXd get_thetaArray();

                double _windingParameter;
                double _radialDistanceAtDeparture;
                double _radialDistanceAtArrival;
                double _psiAngleBetweenArrivalAndDeparture;
                int _numberOfRevolutions;
                int _pointsPerRadian;

                double get_thetaBar();
                // Total angular distance.

                double get_dynamicRangeParameter(double initialFlightPathAngle);

                double get_phaseAngle(double initialFlightPathAngle);

                double get_scaleParameter(double initialFlightPathAngle);

                Eigen::ArrayXd get_sArray(double initialFlightPathAngle);

                // Normalized by the local gravitational acceleration.
                Eigen::ArrayXd get_normalizedThrustAcceleration(double initialFlightPathAngle);

                Eigen::ArrayXd get_flightPathArray(double initialFlightPathAngle);

                Eigen::ArrayXd get_thetaTimeDerivative(const double initialFlightPathAngle,
                                                       const double gravitationalConstant,
                                                       double radialDistanceScaleFactor = 1);

                Eigen::Vector2d get_flightPathLimits();

                double get_bigDelta();

                bool onlyTangentialThrust(double initialFlightPathAngle);

            };
        }
    }
}
#endif //SRC_LAMBERTEXPONENTIALSINUSOID_H
