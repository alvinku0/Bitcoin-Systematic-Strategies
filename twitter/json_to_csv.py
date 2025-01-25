
import pandas as pd
from datetime import datetime
import json
JSON_FILE = './Bitcoin_tweets.jsonl'
JSON_FILE2 = "./Bitcoin_tweets_dataset_2.jsonl"
# enter the csv filename you wish to save it as
CSV_FILE = './filtered_tweet.csv'

file_list = [JSON_FILE, JSON_FILE2]

dfs = [] # an empty list to store the data frames
for file in file_list:
    data = pd.read_json(file, lines=True) # read data frame from json file
    dfs.append(data) # append the data frame to the list
    print(f"{file} into Dataframe completed")

temp = pd.concat(dfs, ignore_index=True) # concatenate all the data frames in the list.

# with open(JSON_FILE, encoding = 'utf-8') as f :
# 	df = pd.read_json(f, lines=True)

# with open(JSON_FILE2, encoding = 'utf-8') as f :
# 	df += pd.read_json(f, lines=True)

print(temp.dtypes)

# Convert the 'date' column to datetime
temp['date'] = pd.to_datetime(temp['date'], errors='coerce')

# Filter the DataFrame by date
start_date = '2021-01-01'
end_date = '2024-12-31'
filtered_df = temp[(temp['date'] >= start_date) & (temp['date'] <= end_date)]
path = "./filtered_tweets.csv"
filtered_df.to_csv(path, encoding = 'utf-8', index = False)

filtered_df = pd.read_csv(path)
filtered_df.to_parquet(f'filtered_tweet.parquet.gzip',compression='gzip')
# filtered_df.drop(columns=)
# print(results)

# df = filter_data_by_date(df,start_date,end_date)
# filtered_df.to_csv(path, encoding = 'utf-8', index = False)


# with open(CSV_FILE, mode='w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=filtered_data[0].keys())
#     writer.writeheader()
#     writer.writerows(filtered_data)
# print(filtered_df)

print("COMPLETED")
# import pandas as pd
# from datetime import datetime
# import json
# import csv
# df = pd.read_json (r'Bitcoin_tweets.jsonl', lines=True)


# filtered_data = filter_data_by_date(df, start_date,end_date)
# print(filtered_data)
# filtered_data.to_csv (r'Bitcoin_tweets.csv', index = None)



# # Convert filtered JSON to CSV
# output_file = 'output.csv'
# print(f"CSV file '{output_file}' created successfully with filtered data.")
