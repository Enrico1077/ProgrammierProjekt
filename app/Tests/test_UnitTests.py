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

    dp0=Kmeans.randArrData(1,2,[10,10],[0,0])
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

    for i in range (2):
        assert result1[i]==1
        assert result2[i]==0

def test_MatchDpZent():
    import numpy as np
    from app.K_Means import Datenpunkt as dp
    from app.K_Means import Kmeans

    dp0=dp.Datenpunkt(np.array([0,0,0]))
    dp1=dp.Datenpunkt(np.array([10,10,10]))
    zt0=dp.Datenpunkt(np.array([1,2,1]))
    zt1=dp.Datenpunkt(np.array([8,7,9]))

    Kmeans.MatchDpZent([dp0,dp1],[zt0,zt1],0)
    assert dp0.getNextCentroid()==zt0
    assert dp1.getNextCentroid()==zt1


