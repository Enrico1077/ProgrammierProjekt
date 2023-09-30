####In dieser Datei können Tests definiert werden######
 

def test_DpExcential():
    import numpy as np
    from app.K_Means import Datenpunkt as dp

    dp0 = dp.Datenpunkt(np.array([2,3]))
    location= dp0.getPosition()
    diff=location[0]-location[1]
    assert diff==-1


def test_EuklidDistance():
    import numpy as np
    from app.K_Means import Datenpunkt as dp
    from app.K_Means import Kmeans

    dp0=dp.Datenpunkt(np.array([0,0]))
    dp1=dp.Datenpunkt(np.array([2,2]))
    result=Kmeans.EuklidDistance(dp0,dp1)
    assert result==8**0.5


def test_ranData():
    import numpy as np
    from app.K_Means import Datenpunkt as dp
    from app.K_Means import Kmeans

    dp0=Kmeans.randArrData(1,2,[10],[0])
    location=dp0.getPostion()
    assert location.size==2
    assert location[0]>=0 and location[1]>=0
    assert location[0]<=10 and location[1]<=10

def test_ManhattenDistance():
    import numpy as np
    from app.K_Means import Datenpunkt as dp
    from app.K_Means import Kmeans

    dp0=dp.Datenpunkt(np.array([0,0]))
    dp1=dp.Datenpunkt(np.array([2,2]))
    result=Kmeans.ManhattenDistance(dp0,dp1)
    assert result==4


def test_FindMid():
    import numpy as np
    from app.K_Means import Datenpunkt as dp
    from app.K_Means import Kmeans

    dp0=dp.Datenpunkt(np.array([0,0,0]))
    dp1=dp.Datenpunkt(np.array([2,2,2]))
    result1=Kmeans.FindMid([dp0,dp1])
    result2=Kmeans.FindMid([dp0,dp0])

    assert result1==[1,1,1]
    assert result2==[0,0,0]
    

