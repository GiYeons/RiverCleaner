from algorithm.prim import *
import pandas as pd
import numpy as np
from haversine import haversine
from algorithm.dfs import Graph as DFS
import logging
np.set_printoptions(precision=4, suppress=True)

class Node:
    def __init__(self, lat, long, rubbish=0, plastics=0, cans=0, glass=0, papers=0):
        self.latitude = lat
        self.longitude = long
        self.rubbish = int(rubbish)
        self.plastics= int(plastics)
        self.cans = int(cans)
        self.glass = int(glass)
        self.papers = int(papers)

    def __str__(self):
        return f'경도 {self.latitude}, 위도 {self.longitude}'

# 로봇은 인수로 받은 정점과 간선을 prim 알고리즘으로 최적화하고
# 해당 그래프를 따라 청소를 진행합니다.
class CollectorBot:
    def __init__(self, bot_num=1, logger=None):
        self.vertices = None
        self.edges = None
        self.route = []
        self.bot_num = bot_num
        self.logger = logger

    # prim 그래프 생성
    def create_prim(self, vertices, edges):
        prim = Graph(vertices)
        prim.graph = edges
        return prim.primMST()

    def exec_bot(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        prim = self.create_prim(vertices, edges)

        dfs = DFS(len(vertices), 0)     # 2번째 인수는 쓰이지 않으므로 0 처리
        dfs.addGraph(prim)
        visited = [False] * len(vertices)
        self.route = dfs.DFS(0, visited)
        # print(f"정점 개수 {len(self.route)}, {self.route}")

        for i in self.route:
            v = self.vertices[i]
            lat = v.latitude
            long = v.longitude
            # print(f"로봇{self.bot_num}, {i:3}번째 정점({lat:11}, {long:11})을 청소.    "
            #       f"### 일반쓰레기 {v.rubbish:3}개, 플라스틱 {v.plastics:3}개, 캔 {v.cans:3}개,"
            #       f"유리 {v.glass:3}개, 종이류 {v.papers:3}개 회수. ###")
            self.logger.info(f"로봇{self.bot_num}, {i:3}번째 정점({lat:11}, {long:11})을 청소.    "
                  f"### 일반쓰레기 {v.rubbish:3}개, 플라스틱 {v.plastics:3}개, 캔 {v.cans:3}개,"
                  f"유리 {v.glass:3}개, 종이류 {v.papers:3}개 회수. ###")


# CollectManager는 청소 로봇을 관리합니다. 먼저 collect_data 형식의 데이터가 필요합니다.
# clean 함수에 청소가 필요한 경도.위도를 인수로 넘기면, 해당 구역의 쓰레기 데이터를 선별하여
# 로봇 1~2대에게 수거를 지시합니다.
class CollectManager:
    def __init__(self, csv_data, logger=None):
        self.csv_data = csv_data
        self.latitude = 0.
        self.longitude = 0.
        self.logger = logger

    def create_vertices(self, arr):     # arr: 각 정점 정보가 담긴 numpy 배열
        vertices = []
        for a in arr:
            vertices.append(Node(a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
        return vertices

    # 정점 정보를 가지고 인접행렬 생성
    def create_edges(self, vertices):   #  vertices: Node 배열
        edges = np.zeros((len(vertices), len(vertices)))
        for i in range(len(vertices)):
            for j in range(len(vertices)):
                if i==j:
                    pass
                else:
                    loc1 = vertices[i].latitude, vertices[i].longitude
                    loc2 = vertices[j].latitude, vertices[j].longitude
                    edges[i, j] = haversine(loc1, loc2)  * 1000     # m 단위
        return edges

    def clean(self, lat, long):
        self.latitude = lat
        self.longitude = long
        bot1 = CollectorBot(1, self.logger)
        bot2 = CollectorBot(2, self.logger)

        # 파일의 데이터와 인자로 받은 경위도를 비교, 청소해야 하는 위치의 데이터만 남긴다
        data = pd.DataFrame.copy(self.csv_data)
        data['Latitude2'] = data['Latitude'] * 10
        data['Latitude2'] = data['Latitude2'].apply(np.floor) / 10
        data['Longitude2'] = data['Longitude'] * 10
        data['Longitude2'] = data['Longitude2'].apply(np.floor) / 10

        data = data[(data['Latitude2'] == self.latitude) & (data['Longitude2'] == self.longitude)]
        data = data.reset_index()
        data = data.drop(['Latitude2', 'Longitude2', 'index'], axis=1)

        # 데이터의 크기가 100이상이면 1:1 분할 (2대의 로봇에게 분배하기 위해)
        if len(data)>90:
            data1 = data.loc[:len(data)/2, :]
            data2 = data.drop(data1.index)
            data1 = data1.values
            data2 = data2.values
            # e.g. [37.3, 127.7, 0, 1, 2, 9, 0]

            # 정점 및 간선 생성
            ver1 = self.create_vertices(data1)
            ver2 = self.create_vertices(data2)
            edg1 = self.create_edges(ver1)
            edg2 = self.create_edges(ver2)

            # 로봇 가동
            bot1.exec_bot(ver1, edg1)
            bot2.exec_bot(ver2, edg2)
        else:
            data1 = data.values
            ver = self.create_vertices(data1)
            edg = self.create_edges(ver)

            bot1.exec_bot(ver, edg)


if __name__=="__main__":
    path = 'data/collect_data.csv'
    data = pd.read_csv(path, header=0, index_col=None, dtype=float)
    manager = CollectManager(data)
    manager.clean(37.4, 127.0)

