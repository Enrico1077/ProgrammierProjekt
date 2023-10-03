import requests
import time
import threading
import Datenpunkt as dp
import numpy as np
import matplotlib.pyplot as plt
import random





def send_test():
    url = 'https://programmierprojekt-ujgmkp4tpq-ez.a.run.app/kmeans/csv?k=10'  
    csv_filename = 'app\K_Means\Examples\snakes_count.csv'  

    start_time = time.time()
    with open(csv_filename, 'rb') as csv_file:
        files = {'file': (csv_filename, csv_file)}
        response = requests.post(url, files=files,)
        end_time = time.time()
        elapsed_time = end_time - start_time

    if response.status_code == 200:
        calculated_data = response.json()
        print("Dauer in s: "+str(elapsed_time))
        return(calculated_data[1])   
    else:
        return(f"Fehler: {response.status_code} - {response.text}")



def visualize_clusters(data_points):
    # Extrahieren Sie die Positionen der Datenpunkte und ihre Cluster-Zuordnungen
    positions = np.array([dp.getPosition() for dp in data_points])
    cluster_ids = [dp.getNextCentroid().getPosition() if dp.getNextCentroid() is not None else None for dp in data_points]

    # Erstellen Sie eine Liste von eindeutigen Cluster-IDs
    unique_clusters = np.unique(cluster_ids, axis=0)

    # Erstellen Sie eine Farbpalette für die Cluster
    colors = plt.cm.get_cmap('tab10', len(unique_clusters))

    # Erstellen Sie ein Streudiagramm für die Datenpunkte und verwenden Sie Farben basierend auf den Clustern
    for i, cluster_id in enumerate(unique_clusters):
        # Filtern Sie die Datenpunkte, die zu diesem Cluster gehören
        cluster_indices = [j for j, c_id in enumerate(cluster_ids) if np.array_equal(c_id, cluster_id)]
        cluster_points = positions[cluster_indices]

        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {i}', c=colors(i), alpha=0.5, marker='o')

    # Extrahieren Sie die Positionen der Zentroide aus den Datenpunkten
    centroid_positions = np.array([dp.getNextCentroid().getPosition() for dp in data_points if dp.getNextCentroid() is not None])

    # Fügen Sie die Zentroide hinzu
    plt.scatter(centroid_positions[:, 0], centroid_positions[:, 1], marker='x', color='red', s=100, label='Zentroide')

    plt.xlabel('X-Achse')
    plt.ylabel('Y-Achse')
    plt.title('k-Means Clustering Ergebnisse mit Farben pro Cluster und Zentroiden')

    # Fügen Sie eine Legende hinzu
    plt.legend()

    # Zeigen Sie das Diagramm an
    plt.show()



def send_post_request(filename,url):
    start_time = time.time()
    with open(filename, 'rb') as csv_file:
        files = {'file': (filename, csv_file)}
        response = requests.post(url, files=files)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return response.status_code, response.json(), elapsed_time

def process_request(filename,url):
    status_code, calculated_data, elapsed_time = send_post_request(filename,url)
    if status_code == 200:   
        print("Info: "+str(calculated_data[0]))
        print("Fertig in: " + str(elapsed_time) +" s")
      
    else:
        print("Fehler nach: " + str(elapsed_time))

def create_data_points(result_data):
    data_points = []
    for result_item in result_data:
        position = (result_item['PunktDimension0'], result_item['PunktDimension1'])
        data_point = dp.Datenpunkt(position)
        next_centroid_position = (result_item['ZentDimension0'], result_item['ZentDimension1'])
        next_centroid = dp.Datenpunkt(next_centroid_position)
        data_point.setNextCentroid(next_centroid)
        data_points.append(data_point)
    return data_points

def sendmultiTest():
    url = 'https://programmierprojekt-ujgmkp4tpq-ez.a.run.app/kmeans/csv?k=10'
    csv_filenames = []
    for i in range(5):
        csv_filenames.append('app\K_Means\Examples\cities.csv')

    threads = []
    for filename in csv_filenames:
        thread = threading.Thread(target=process_request, args=(filename,url,))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()


#data=create_data_points(send_test())
#visualize_clusters(data)

sendmultiTest()