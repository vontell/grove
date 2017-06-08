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

# This file contains helpful methods for executing computations on the host
# computer (i.e. computation before sending a Quil program to Forest)

def gcd(a, b):
    '''
    Finds the greatest common denominator of a and b
    :param a: The first value to consider
    :param b: The second value to consider
    :return: The greatest common denominator of a and b
    '''
    
    while b != 0:
        bTemp = b
        b = a % b
        a = bTemp
    return a