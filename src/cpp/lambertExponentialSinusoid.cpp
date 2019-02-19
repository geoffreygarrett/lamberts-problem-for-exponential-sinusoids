//
// Created by ggarrett on 17/02/19.
//

#include "lambertExponentialSinusoid.h"


namespace tudat {

    namespace mission_segments {

        namespace low_thrust {


            Eigen::ArrayXd lambertExponentialSinusoid::get_thetaArray() {
                double _maxTheta = get_thetaBar();
                int _points = static_cast<int>(_maxTheta * _pointsPerRadian);
                return Eigen::ArrayXd::LinSpaced(_points, 0, static_cast<float>(_maxTheta));
            };

            Eigen::ArrayXd lambertExponentialSinusoid::get_radialDistanceArray(double initialFlightPathAngle,
                                                                               double radialDistanceScaleFactor = 1.0) {
                double _dynamicRangeParameter = // k1
                        get_dynamicRangeParameter(initialFlightPathAngle
                        );
                double _phaseAngle = // phi
                        get_phaseAngle(initialFlightPathAngle
                        );
                double _scaleParameter = // k0
                        get_scaleParameter(initialFlightPathAngle
                        );
                Eigen::ArrayXd _thetaArray = get_thetaArray();
                return radialDistanceScaleFactor * _scaleParameter *
                       (_dynamicRangeParameter * (_windingParameter * _thetaArray.array() + _phaseAngle).sin()).exp();
            };

            double lambertExponentialSinusoid::get_thetaBar() {
                return _psiAngleBetweenArrivalAndDeparture +
                       _numberOfRevolutions * 2 *
                       mathematical_constants::PI;
            }

            double lambertExponentialSinusoid::get_dynamicRangeParameter(const double initialFlightPathAngle) {
                const double _thetaMax = get_thetaBar();
                // Determine k1 sign
                const double _numeratorEq7 = log(_radialDistanceAtDeparture / _radialDistanceAtArrival)
                                             + (tan(initialFlightPathAngle) / _windingParameter) *
                                               sin(_windingParameter * _thetaMax);
                const double _denominatorEq7 = 1 - cos(_windingParameter * _thetaMax);
                const double _resultEq7 = _numeratorEq7 / _denominatorEq7;

                // Determine k1 magnitude
                const double _dynamicRangeParameter = sqrt(
                        pow(_resultEq7, 2) + pow(tan(initialFlightPathAngle) / _windingParameter, 2));

                return (_resultEq7 > 0) ? _dynamicRangeParameter : -_dynamicRangeParameter;
            }

            double lambertExponentialSinusoid::get_phaseAngle(const double initialFlightPathAngle) {
                return acos(tan(initialFlightPathAngle) /
                            (get_dynamicRangeParameter(initialFlightPathAngle) * _windingParameter));
            }

            double lambertExponentialSinusoid::get_scaleParameter(const double initialFlightPathAngle) {
                return _radialDistanceAtDeparture /
                       (exp(get_dynamicRangeParameter(initialFlightPathAngle) *
                            sin(get_phaseAngle(initialFlightPathAngle))));

            }

            Eigen::ArrayXd lambertExponentialSinusoid::get_sArray(const double initialFlightPathAngle) {
                return (get_phaseAngle(initialFlightPathAngle) + _windingParameter * get_thetaArray()).sin().atan();
            };

            double lambertExponentialSinusoid::get_bigDelta() {
                return (2 * (1 - cos(_windingParameter * get_thetaBar()))) / (pow(_windingParameter, 4)) -
                       pow(log(_radialDistanceAtDeparture / _radialDistanceAtArrival), 2);
            };

            Eigen::Vector2d lambertExponentialSinusoid::get_flightPathLimits() {
                double _Delta = get_bigDelta();
                double _thetaMax = get_thetaBar();
                double _oneLimit = atan(
                        _windingParameter / 2 * (-log(_radialDistanceAtDeparture / _radialDistanceAtArrival) /
                                                 tan((_windingParameter * _thetaMax) / 2) + sqrt(_Delta)));
                double _otherLimit = atan(
                        _windingParameter / 2 * (-log(_radialDistanceAtDeparture / _radialDistanceAtArrival) /
                                                 tan((_windingParameter * _thetaMax) / 2) - sqrt(_Delta)));
                double lowerLimit = (_oneLimit < _otherLimit) ? _oneLimit : _otherLimit;
                double upperLimit = (_oneLimit > _otherLimit) ? _oneLimit : _otherLimit;
                Eigen::Vector2d _ret = {lowerLimit, upperLimit};
                return _ret;
            };

            Eigen::ArrayXd lambertExponentialSinusoid::get_flightPathArray(const double initialFlightPathAngle) {
                return (get_dynamicRangeParameter(initialFlightPathAngle) * _windingParameter *
                        (_windingParameter * get_thetaArray() + get_phaseAngle(initialFlightPathAngle)).cos()).atan();
            };

            Eigen::ArrayXd lambertExponentialSinusoid::get_thetaTimeDerivative(const double initialFlightPathAngle,
                                                                               const double gravitationalConstant,
                                                                               double radialDistanceScaleFactor) {
                return ((gravitationalConstant /
                         ((get_radialDistanceArray(initialFlightPathAngle) * radialDistanceScaleFactor).cube()))
                        /
                        (get_flightPathArray(initialFlightPathAngle).tan().square() +
                         get_dynamicRangeParameter(initialFlightPathAngle) * pow(_windingParameter, 2) *
                         get_sArray(initialFlightPathAngle) + 1)
                ).sqrt();
            };

            // Normalized by the local gravitational acceleration.
            Eigen::ArrayXd
            lambertExponentialSinusoid::get_normalizedThrustAcceleration(const double initialFlightPathAngle) {
                Eigen::ArrayXd _flightPathAngleArray = get_flightPathArray(initialFlightPathAngle);
                double _dynamicRangeParameter = get_dynamicRangeParameter(initialFlightPathAngle);
                Eigen::ArrayXd _sArray = get_sArray(initialFlightPathAngle);
                return _flightPathAngleArray.tan() / (2 * _flightPathAngleArray.cos()) * (
                        (1) /
                        (pow(_flightPathAngleArray.tan(), 2) +
                         _dynamicRangeParameter * pow(_windingParameter, 2) * _sArray + 1)
                        -
                        (pow(_windingParameter, 2) * (1 - 2 * _dynamicRangeParameter * _sArray)) /
                        pow(
                                pow(_flightPathAngleArray.tan(), 2) +
                                _dynamicRangeParameter * pow(_windingParameter, 2) * _sArray + 1,
                                2));
            };

            bool lambertExponentialSinusoid::onlyTangentialThrust(const double initialFlightPathAngle) {
                return abs(get_dynamicRangeParameter(initialFlightPathAngle) * pow(_windingParameter, 2)) < 1;
                // TODO: Check discrepancy between ACT INTERNAL REPORT and Engineering Notes
                // it appears that it was initially stated as > 1 incorrectly.
            }

        }


    }
}
