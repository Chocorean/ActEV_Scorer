# ./wrapper/__init__.py
# Author(s): Baptiste Chocot

# This software was developed by employees of the National Institute of
# Standards and Technology (NIST), an agency of the Federal
# Government. Pursuant to title 17 United States Code Section 105, works
# of NIST employees are not subject to copyright protection in the
# United States and are considered to be in the public
# domain. Permission to freely use, copy, modify, and distribute this
# software and its documentation without fee is hereby granted, provided
# that this notice and disclaimer of warranty appears in all copies.

# THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT ANY WARRANTY OF ANY KIND,
# EITHER EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED
# TO, ANY WARRANTY THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY
# IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, AND FREEDOM FROM INFRINGEMENT, AND ANY WARRANTY THAT THE
# DOCUMENTATION WILL CONFORM TO THE SOFTWARE, OR ANY WARRANTY THAT THE
# SOFTWARE WILL BE ERROR FREE. IN NO EVENT SHALL NIST BE LIABLE FOR ANY
# DAMAGES, INCLUDING, BUT NOT LIMITED TO, DIRECT, INDIRECT, SPECIAL OR
# CONSEQUENTIAL DAMAGES, ARISING OUT OF, RESULTING FROM, OR IN ANY WAY
# CONNECTED WITH THIS SOFTWARE, WHETHER OR NOT BASED UPON WARRANTY,
# CONTRACT, TORT, OR OTHERWISE, WHETHER OR NOT INJURY WAS SUSTAINED BY
# PERSONS OR PROPERTY OR OTHERWISE, AND WHETHER OR NOT LOSS WAS
# SUSTAINED FROM, OR AROSE OUT OF THE RESULTS OF, OR USE OF, THE
# SOFTWARE OR SERVICES PROVIDED HEREUNDER.

# Distributions of NIST software should also include copyright and
# licensing statements of any third-party software that are legally
# bundled with the code in compliance with the conditions of those
# licenses.

import os
import importlib

#ALGORITHM = 'munkres'
#ALGORITHM = 'lapjv_lapjv'
#ALGORITHM = 'lap_lapjv'

class UnknowAlgorithmError(Exception):
    """
    Exception raised when an unknown algorithm is specified.
    """
    def __init__(self, algorithm):
        super.__init__(self)
        self.algorithm = algorithm

    def __str__(self):
        return "Algorithm `{}` not known. Check ./wrapper/ directory.".format(self.algorithm)


def _get_algos_list():
    """
    Return the list of the known algorithms names.
    """
    algo_path = os.path.dirname(os.path.abspath(__file__))
    algos_list = os.listdir(algo_path)
    algos_list.remove('__init__.py')
    for i in range(len(algos_list)):
        algos_list[i] = algos_list[i][:-3:]
    return algos_list


def _check_algorithm(algorithm):
    """
    Check if the specified algorithm is defined in the ./wrapper/ directory.
    """
    return algorithm in _get_algos_list()


def update_algorith(algorithm):
    """
    Update the algorithm used to score a system output.
    """
    if _check_algorithm(algorithm):
        global ALGORITHM
        ALGORITHM = algorithm
    else:
        raise UnknowAlgorithmError


def _get_lib():
    """
    Return the module corresponding to the current selected algorithm.
    """
    global ALGORITHM
    algo_path = os.path.dirname(os.path.abspath(__file__))
    algos_list = os.listdir(algo_path)
    algos_list.remove('__init__.py')
    for algo in algos_list:
        file_name = "{}.py".format(ALGORITHM)
        if file_name == algo:
            return importlib.import_module(".{}".format(ALGORITHM), package="wrapper")


def get_compute():
    """
    Return corresponding compute function.
    """
    return _get_lib().compute

##### #####

__all__ = [
    'get_compute'
]