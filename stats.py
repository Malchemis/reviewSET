import os
import pandas as pd
import ydata_profiling as ydp

data_folder = 'data'
json_folder = 'json'
save_folder = 'save'

# Check if the save folder exists, if not, create it
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

## Combine all the CSV files into a single DataFrame
df = pd.concat([pd.read_csv(f'{data_folder}/{file}') for file in os.listdir(data_folder) if file.endswith('.csv')])

# Save the DataFrame to a CSV file
df.to_csv(f'{save_folder}/sound_event_detection_reviews.csv', index=False)

# Generate a profile report
profile = ydp.ProfileReport(df, title='Sound Event Detection Reviews')
# save the report as an HTML file
profile.to_file(f'{save_folder}/sound_event_detection_reviews.html')