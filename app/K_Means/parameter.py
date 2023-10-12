""" Module for handling parameters for the k-means algorithm """

import enum
from flask import Request

class Normmethod(enum.IntEnum):
    """ Represents possible values for normalization method """
    NONE = 0
    MIN_MAX = 1
    Z = 2

class DistanceMatrix(enum.IntEnum):
    """ Represents possible values for distance matrix """
    EUCLIDEAN = 0
    MANHATTAN = 1

class KMeansParameter:
    """ Class for handling parameters for the k-means algorithm  """

    # these default values are used if a parameter is not specified
    default_values = {
        'k': 0,
        'normMethod': Normmethod.NONE,
        'r': 5,
        'maxCentroidsAbort': 100,
        'minPctElbow': 0,
        'c': 0,
        'minPctAutoCycle': 0.5,
        'maxAutoCycleAbort': 25,
        'distance_matrix_int': DistanceMatrix.EUCLIDEAN,
        'parallelCalculations': 8,
        'csvDecimalSeparator': 'EU',
        'sheetName': 0
    }

    def __init__(self, param_distance_matrix, req: Request):
        # call the setter for each parameter, perform a plausibility check or use the default value
        self.set_k(req.args.get('k'))
        self.set_r(req.args.get('r'))
        self.set_max_centroids_abort(req.args.get('maxCentroidsAbort'))
        self.set_c(req.args.get('c'))
        self.set_max_auto_cycle_abort(req.args.get('maxAutoCycleAbort'))
        self.set_parallel_calculations(req.args.get('parallelCalculations'))
        self.set_min_pct_elbow(req.args.get('minPctElbow'))
        self.set_min_pct_auto_cycle(req.args.get('minPctAutoCycle'))
        self.set_norm_method(req.args.get('normMethod'))
        self.set_distance_matrix(param_distance_matrix)
        self.set_sheet_name(req.args.get('sheetName'))
        self.set_csv_decimal_separator(req.args.get('csvDecimalSeparator'))

    def set_k(self, param):
        """ Perform plausibility check and set parameter k or use default value """
        if self.check_for_pos_int(param, 'k'):
            self.k = int(param)
        else:
            self.k = self.default_values['k']

        self.use_elbow = 1 if self.k == 0 else 0

    def set_r(self, param):
        """ Perform plausibility check and set parameter r or use default value """
        if self.check_for_pos_int(param, 'r'):
            self.r = int(param)
        else:
            self.r = self.default_values['r']

    def set_max_centroids_abort(self, param):
        """ Perform plausibility check and set parameter max_centroids_abort or use default value """
        if self.check_for_pos_int(param, 'maxCentroidsAbort'):
            self.max_centroids_abort = int(param)
        else:
            self.max_centroids_abort = self.default_values['maxCentroidsAbort']

    def set_c(self, param):
        """ Perform plausibility check and set parameter c or use default value """
        if self.check_for_pos_int(param, 'c'):
            self.c = int(param)
        else:
            self.c = self.default_values['c']

        self.auto_cycle = 1 if self.c == 0 else 0

    def set_max_auto_cycle_abort(self, param):
        """ Perform plausibility check and set parameter max_auto_cycle_abort or use default value """
        if self.check_for_pos_int(param, 'maxAutoCycleAbort'):
            self.max_auto_cycle_abort = int(param)
        else:
            self.max_auto_cycle_abort = self.default_values['maxAutoCycleAbort']

    def set_parallel_calculations(self, param):
        """ Perform plausibility check and set parameter parallel_calculations or use default value """
        if self.check_for_pos_int(param, 'parallelCalculations'):
            self.parallel_calculations = int(param)
        else:
            self.parallel_calculations = self.default_values['parallelCalculations']

        self.parallel_calculating = 1 if self.parallel_calculations > 1 else 0

    def set_min_pct_elbow(self, param):
        """ Perform plausibility check and set parameter min_pct_elbow or use default value """
        if self.check_for_percentage_float(param, 'minPctElbow'):
            self.min_pct_elbow = float(param)
        else:
            self.min_pct_elbow = self.default_values['minPctElbow']

    def set_min_pct_auto_cycle(self, param):
        """ Perform plausibility check and set parameter min_pct_auto_cycle or use default value """
        if self.check_for_percentage_float(param, 'minPctAutoCycle'):
            self.min_pct_auto_cycle = float(param)
        else:
            self.min_pct_auto_cycle = self.default_values['minPctAutoCycle']

    def set_norm_method(self, param):
        """ Perform plausibility check and set parameter norm_method or use default value """
        if param is None:
            self.norm_method = self.default_values['normMethod']
        elif int(param) == 0:
            self.norm_method = Normmethod.NONE
        elif int(param) == 1:
            self.norm_method = Normmethod.MIN_MAX
        elif int(param) == 2:
            self.norm_method = Normmethod.Z
        else:
            raise ValueError('The passed parameter normMethod must be an integer with 0, 1 or 2.',
                             'normMethod', param)

    def set_distance_matrix(self, param):
        """ Perform plausibility check and set parameter distance_matrix or use default value """
        if param == "euclidean":
            self.distance_matrix = DistanceMatrix.EUCLIDEAN
        elif param == "manhattan":
            self.distance_matrix = DistanceMatrix.MANHATTAN
        else:
            raise ValueError('The distance matrix specified in the URL is invalid; accepted values are "euclidean" or "manhattan".',
                             'distanceMatrix', param)

    def set_sheet_name(self, param):
        """ Perform plausibility check and set parameter sheet_name or use default value """
        if param is None:
            self.sheet_name = self.default_values['sheetName']
        else:
            self.sheet_name = str(param)

    def set_csv_decimal_separator(self, param):
        """ Perform plausibility check and set parameter csv_decimal_separator or use default value """
        if param is None:
            self.csv_decimal_separator = self.default_values['csvDecimalSeparator']
        elif param == 'EU':
            self.csv_decimal_separator = 'EU'
        elif param == 'US':
            self.csv_decimal_separator = 'US'
        else:
            raise ValueError('The passed parameter csvDecimalSeparator must be "EU" or "US".',
                             'csvDecimalSeparator', param)

    def check_for_pos_int(self, param, name: str) -> bool:
        """ This method checks if the passed parameter is integer and greater than zero; returns False if the parameter is not specified """
        if param is not None:
            try:
                value = int(param)
                if value > 0:
                    return True
                raise ValueError("The passed parameter " + name + " must be an integer greater than zero.",
                                    name, param)
            except ValueError as e:
                raise ValueError("The passed parameter " + name + " must be an integer greater than zero.",
                                 name, param) from e
        else:
            return False

    def check_for_percentage_float(self, param, name: str) -> bool:
        """ This method checks if the passed parameter is a floating point number and is between 0 and 100; returns False if the parameter is not specified """
        if param is not None:
            try:
                value = float(param)
                if value >= 0 or value <= 100:
                    return True
                raise ValueError("The passed parameter " + name + " must be a floating point number from zero up to and including 100.",
                                    name, param)
            except ValueError as e:
                raise ValueError("The passed parameter " + name + " must be a floating point number from zero up to and including 100.",
                                 name, param) from e
        else:
            return False

    def get_values_str(self) -> str:
        """ Creates a formatted string with all values, for example for debug logging """
        msg = f'''
            'k': {self.k},
            'normMethod': {self.norm_method},
            'r': {self.r},
            'maxCentroidsAbort': {self.max_centroids_abort},
            'minPctElbow': {self.min_pct_elbow},
            'c': {self.c},
            'minPctAutoCycle': {self.min_pct_auto_cycle},
            'maxAutoCycleAbort': {self.max_auto_cycle_abort},
            'distance_matrix': {self.distance_matrix},
            'parallelCalculations': {self.parallel_calculations},
            'csvDecimalSeparator': {self.csv_decimal_separator},
            'sheetName': {self.sheet_name},
        '''

        return msg
