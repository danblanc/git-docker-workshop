import pandas as pd 
import os 
import datetime as dt

data_path = os.getenv('DATA_PATH')
data_name = os.getenv('DATA_NAME')

print(f'Data path: {data_path} \n Data name: {data_name}')

try:
    df = pd.read_csv(data_path)

    print(f'Dataset succesfully read: {len(df)} rows')

    df.columns = [col.lower() for col in df.columns]

    df.columns = [col.replace(' ', '_') for col in df.columns]

    df.to_csv(f'data/{data_name}_{dt.date.today()}.csv', index=False)

    print('Dataset stored as csv succesfully')

except Exception as e:
    print(f'Something went wrong: {e}')