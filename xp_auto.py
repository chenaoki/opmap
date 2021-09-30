try:
    import cupy as xp
    print("xp_auto.py: import cupy")
except ImportError:
    import numpy as xp
    def asnumpy(arr):                                                                                    return xp.asarray(arr)                                                             
    xp.asnumpy = asnumpy
    print("xp_auto.py: import numpy")