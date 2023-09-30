####In dieser Datei können Tests definiert werden######
import numpy as np
from app.K_Means import Datenpunkt as dp
from app.K_Means import Kmeans 


def test_DpExcential():
    dp0 = dp.Datenpunkt(np.array([2,3]))
    location= dp0.getPosition()
    diff=location[0]-location[1]
    assert diff==-1


def test_EuklidDistance():
    dp0=dp.Datenpunkt(np.array([0,0]))
    dp1=dp.Datenpunkt(np.array([2,2]))
    result=Kmeans.EuklidDistance(dp0,dp1)
    assert result==8**0.5


def test_ranData():
    dp0=Kmeans.randArrData(1,2,[10,10],[0,0])
    location=dp0[0].getPosition()
    assert location.size==2
    assert location[0]>=0 and location[1]>=0
    assert location[0]<=10 and location[1]<=10

def test_ManhattenDistance():
    dp0=dp.Datenpunkt(np.array([0,0]))
    dp1=dp.Datenpunkt(np.array([2,2]))

    result=Kmeans.ManhattenDistance(dp0,dp1)
    assert result==4


def test_FindMid():
    dp0=dp.Datenpunkt(np.array([0,0,0]))
    dp1=dp.Datenpunkt(np.array([2,2,2]))

    result1=Kmeans.FindMid([dp0,dp1])
    result2=Kmeans.FindMid([dp0,dp0])   
    for i in range (2):
        assert result1[i]==1
        assert result2[i]==0


def test_MatchDpZent():
    dp0=dp.Datenpunkt(np.array([0,0,0]))
    dp1=dp.Datenpunkt(np.array([10,10,10]))
    zt0=dp.Datenpunkt(np.array([1,2,1]))
    zt1=dp.Datenpunkt(np.array([8,7,9]))

    Kmeans.MatchDpZent([dp0,dp1],[zt0,zt1],0)
    assert dp0.getNextCentroid()==zt0
    assert dp1.getNextCentroid()==zt1


def test_newCentroids():
    dp0 = dp.Datenpunkt(np.array([0, 0, 0]))
    dp1 = dp.Datenpunkt(np.array([2, 2, 2]))
    dp2 = dp.Datenpunkt(np.array([4, 4, 4]))
    centroid1 = dp.Datenpunkt(np.array([1, 1, 1]))
    centroid2 = dp.Datenpunkt(np.array([3, 3, 3]))
    Datenpunkte = [dp0, dp1, dp2]
    Zentroide = [centroid1, centroid2]

    Kmeans.newCentroids(Datenpunkte, Zentroide)
    assert np.array_equal(centroid1.getPosition(), np.array([1.0, 1.0, 1.0]))
    assert np.array_equal(centroid2.getPosition(), np.array([3.0, 3.0, 3.0]))


def test_maxLocation():
    dp0 = dp.Datenpunkt(np.array([0, 0, 0]))
    dp1 = dp.Datenpunkt(np.array([2, 2, 2]))
    dp2 = dp.Datenpunkt(np.array([4, 4, 4]))
    DataPoints = [dp0, dp1, dp2]

    result = Kmeans.maxLocation(DataPoints)
    expected_result = np.array([4.0, 4.0, 4.0])
    assert np.array_equal(result, expected_result)


def test_minLocation():
    dp0 = dp.Datenpunkt(np.array([0, 0, 0]))
    dp1 = dp.Datenpunkt(np.array([2, 2, 2]))
    dp2 = dp.Datenpunkt(np.array([-1, -1, -1]))
    DataPoints = [dp0, dp1, dp2]

    result = Kmeans.minLocation(DataPoints)
    expected_result = np.array([-1.0, -1.0, -1.0])
    assert np.array_equal(result, expected_result)


def test_MinMaxNorm():
    dp0 = dp.Datenpunkt(np.array([0, 0, 0]))
    dp1 = dp.Datenpunkt(np.array([2, 2, 2]))
    dp2 = dp.Datenpunkt(np.array([4, 4, 4]))
    DataPoints = [dp0, dp1, dp2]

    Kmeans.MinMaxNorm(DataPoints)
    expected_dp0 = np.array([0.0, 0.0, 0.0])
    expected_dp1 = np.array([0.5, 0.5, 0.5])
    expected_dp2 = np.array([1.0, 1.0, 1.0])    
    assert np.allclose(dp0.getPosition(), expected_dp0)
    assert np.allclose(dp1.getPosition(), expected_dp1)
    assert np.allclose(dp2.getPosition(), expected_dp2)


def test_z_Norm():
    dp0 = dp.Datenpunkt(np.array([0, 0, 0]))
    dp1 = dp.Datenpunkt(np.array([2, 2, 2]))
    dp2 = dp.Datenpunkt(np.array([4, 4, 4]))
    DataPoints = [dp0, dp1, dp2]

    Kmeans.z_Norm(DataPoints)
    expected_dp0 = np.array([-1.22474487, -1.22474487, -1.22474487])
    expected_dp1 = np.array([0.0, 0.0, 0.0])
    expected_dp2 = np.array([1.22474487, 1.22474487, 1.22474487])
    for dp in DataPoints:
        assert np.allclose(np.std(dp.getPosition()), 1.62993161855452, rtol=1e-9)
    assert np.allclose(dp0.getPosition(), expected_dp0)
    assert np.allclose(dp1.getPosition(), expected_dp1)
    assert np.allclose(dp2.getPosition(), expected_dp2)



def test_retAllPos():  
    dp0 = dp.Datenpunkt(np.array([0, 0, 0]))
    dp1 = dp.Datenpunkt(np.array([2, 2, 2]))
    dp2 = dp.Datenpunkt(np.array([4, 4, 4]))
    DataPoints = [dp0, dp1, dp2]

    result = Kmeans.retAllPos(DataPoints)
    expected_result = np.array([[0.0, 0.0, 0.0], [2.0, 2.0, 2.0], [4.0, 4.0, 4.0]])
    assert np.array_equal(result, expected_result)