import cmath
import math
from numpy import dot
from numpy.linalg import inv, det, solve as asolve
from cmath import rect as rec, polar as pol, phase
from numpy import cross
import numpy as np
from itertools import accumulate as cum, combinations as com, permutations as per
from statistics import mean, median as med, geometric_mean as gmean, harmonic_mean as hmean, stdev, pstdev, variance as var, pvariance as pvar
from math import degrees as deg, radians as rad, sin, cos, tan, asin, acos, atan, hypot, atan2, sqrt, pi, isclose,log
from .load import ldi,ldie,lda,ldae,ldc,ldf,ldfe
from .stat import *
from .listelemop import *
from .degRad import dsin,dcos,dtan
from .vec import drec,drec3d,dpol,dpol3d,rec3d,pol3d,v3d
from .matrix import Mat,AugMat
from .geometry import line,plane
from .regression import LinReg