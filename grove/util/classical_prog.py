##############################################################################
# Copyright 2016-2017 Rigetti Computing
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##############################################################################

# This file contains methods to create Quil programs with common classical
# instructions (for example, the gcd, addition, etc...)

import pyquil.quil as pq

def gcd(a, b, classical_regs, result_regs):
    '''
    Returns a Quil program to find the greatest common denominator of a and b.
    Note that the gcd_reqs method in classical_host may be useful for
    determining the number of registers that you may need.
    :param a: The first value to consider
    :param b: The second value to consider
    :param classical_regs: A list of classical registers to use during the GCD
                           computation
    :param result_regs: A list of classical registers to save the result in
    :return: Program to find the greatest common denominator of a and b
    '''
    
    pass