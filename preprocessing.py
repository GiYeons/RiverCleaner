import pandas as pd
import numpy as np

path = "data/outlier_processed_data.csv"

data = pd.read_csv(path, header=0)
data = data.drop(data.columns[0], axis=1)
data = data.drop(['Name', 'Widths', 'Hights'], axis=1)


# 위경도를 기준으로 요약한 데이터 for scheduler
data_4_scheduler = pd.DataFrame.copy(data)
data_4_scheduler['Latitude'] = data_4_scheduler['Latitude'] * 10
data_4_scheduler['Latitude'] = data_4_scheduler['Latitude'].apply(np.floor) / 10
data_4_scheduler['Longitude'] = data_4_scheduler['Longitude'] * 10
data_4_scheduler['Longitude'] = data_4_scheduler['Longitude'].apply(np.floor) / 10
data_4_scheduler['total'] = data_4_scheduler[['Rubbish', 'Plastics', 'Cans', 'Glass', 'Papers']].sum(axis=1)

grouped_4_scheduler = data_4_scheduler.groupby(['Latitude', 'Longitude']).agg('sum')
grouped_4_scheduler = grouped_4_scheduler.reset_index()
grouped_4_scheduler = grouped_4_scheduler.drop_duplicates(['total'])    # 총 쓰레기량이 중복이면 제거(용이한 연산을 위해)
# print(grouped_4_scheduler)

# grouped_4_scheduler.to_csv("data/scheduler_data.csv", index=False)


# 위경도를 기준으로 정렬 및 합산된 데이터 for collecter_bot
grouped_4_cb = data.groupby(['Latitude', 'Longitude']).agg('sum')
data_4_cb = grouped_4_cb.reset_index()
print(data_4_cb)
data_4_cb.to_csv("data/collect_data.csv", index=False, mode='w')