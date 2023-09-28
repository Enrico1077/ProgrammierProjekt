####In dieser Datei können Tests definiert werden######
 



def test_BeispielTest():
    add = 1+1
    assert add ==2

def test_DpExcential():
    import numpy as np
    import sys
    sys.path.append("//home//runner//work//ProgrammierProjekt//ProgrammierProjekt//app//K_Means")
    import Datenpunkt as dp
    dp0 = dp.Datenpunkt(np.array([2,3]))
    location= dp0.getPosition()
    diff=location[0]-location[1]
    assert diff==-1

def test_ranData():
    import sys
    sys.path.append("//home//runner//work//ProgrammierProjekt//ProgrammierProjekt//app//K_Means")
    import numpy as np
    import Datenpunkt as dp
    from Kmeans import randArrData
    dp0=randArrData(1,2,10,0)
    location=dp0.getPostion()
    assert location.size==2
    assert location[0]>=0 and location[1]>=0
    assert location[0]<=10 and location[1]<=10


