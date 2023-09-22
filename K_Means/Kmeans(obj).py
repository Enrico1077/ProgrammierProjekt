import Datenpunkt as dp
import numpy as np

ref = dp.Datenpunkt(np.array([2,3]))
print(ref.getPosition())
ref.setPosition(np.array([3,4]))
print(ref.getPosition())