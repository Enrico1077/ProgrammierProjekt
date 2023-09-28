####In dieser Datei können Tests definiert werden######
 



def test_BeispielTest():
    add = 1+1
    assert 2
    return add

def test_DpExcential():
    import numpy as np
    import Datenpunkt as dp

    dp0 = dp.Datenpunkt(np.array([2,3]))
    location= dp0.getPosition()
    assert np.array([2,3])
    return location


