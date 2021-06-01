# -*- coding: utf-8 -*-
"""
Created on Fri May 21 20:22:57 2021

@author: todor
"""

import  numpy as np
cimport numpy as np


                
cdef np.ndarray eyes = np.random.random_integers(1, 6)

#print(eyes)