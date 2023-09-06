import os
import panda as pd
import ydata_profiling as ydp

data_folder = 'data'
json_folder = 'json'

## Combine all the CSV files into a single DataFrame
df = pd.concat([pd.read_csv(f'{data_folder}/{file}') for file in os.listdir(data_folder) if file.endswith('.csv')])

# Generate a profile report
profile = ydp.ProfileReport(df, title='Sound Event Detection Reviews')