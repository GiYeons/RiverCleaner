from scheduler import *
from collect_manager import *
import numpy as np
import pandas as pd
import logging

if __name__=="__main__":
    # 로깅 설정
    logger = logging.getLogger("log")
    fileHandler = logging.FileHandler('./log/test.log')
    logger.addHandler(fileHandler)
    logger.setLevel(level=logging.DEBUG)


    sch_path = 'data/scheduler_data.csv'
    col_path = 'data/collect_data.csv'
    sch_data = pd.read_csv(sch_path, header=None, index_col=None).values
    col_data = pd.read_csv(col_path, header=0, index_col=None, dtype=float)
    header = sch_data[0]
    sch_data = np.delete(sch_data, 0, axis=0).astype(float)

    # RBTree를 활용하면 총 쓰레기량이 많은 순으로 경도.위도를 반환받을 수 있습니다.
    rbt = RBTree()
    for i, data in enumerate(sch_data):
        rbt.insertNode(i, data[0], data[1], data[2], data[3], data[4], data[5], data[6])

    # 쓰레기 수거 매니저 호출
    manager = CollectManager(col_data, logger)

    while not rbt.isEmpty():
        total1, lat, long = rbt.get_max()
        rbt.delete_node(total1)
        logger.info('\n------------------------------------------')
        logger.info("경도 %.1f, 위도 %.1f의 부유 쓰레기를 수거합니다... 총 쓰레기량은 %d입니다.\n" %(lat, long, total1))
        # print('\n------------------------------------------')
        # print("경도 %.1f, 위도 %.1f의 부유 쓰레기를 수거합니다... 총 쓰레기량은 %d입니다.\n" %(lat, long, total1))
        manager.clean(lat, long)
