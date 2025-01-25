import csv
import pandas as pd
# # 
# f = open("./filtered_output.csv", "a")
# writer = csv.DictWriter(
#     f, fieldnames=['archived', 'author', 'author_flair_background_color', 'author_flair_css_class', 'author_flair_richtext', 'author_flair_text', 'author_flair_text_color', 'author_flair_type', 'brand_safe', 'can_gild', 'contest_mode', 'created_utc', 'distinguished', 'domain', 'edited', 'gilded', 'hidden', 'hide_score', 'id', 'is_crosspostable', 'is_original_content', 'is_reddit_media_domain', 'is_self', 'is_video', 'link_flair_css_class', 'link_flair_richtext', 'link_flair_text', 'link_flair_text_color', 'link_flair_type', 'locked', 'media', 'media_embed', 'no_follow', 'num_comments', 'num_crossposts', 'over_18', 'parent_whitelist_status', 'permalink', 'retrieved_on', 'rte_mode', 'score', 'secure_media', 'secure_media_embed', 'selftext', 'send_replies', 'spoiler', 'stickied', 'subreddit', 'subreddit_id', 'subreddit_name_prefixed', 'subreddit_type', 'suggested_sort', 'thumbnail', 'thumbnail_height', 'thumbnail_width', 'title', 'url', 'whitelist_status'])
# writer.writeheader()
# f.close()

# data = pd.read_csv('./filtered_output.csv') 
# print(data.dtypes)
# importing python package 
import pandas as pd 

# # read contents of csv file 
# file = pd.read_csv("./filtered_output.csv", on_bad_lines='skip')
# # print("\nOriginal file:") 
# # print(file) 
# print(file)
# # adding header 
# headerList = ["index","date", "title","author","link", "content"]
# # converting data frame to csv 
# file.to_csv("filtered_output2.csv", header =headerList, index=False) 

# Function to remove line breaks from a string
def remove_line_breaks(text):
    return text.replace('\n', ' ').replace('\r', ' ')

# Input and output CSV file paths
input_csv = './reddit.csv'
output_csv = './filtered_reddit.csv'

# Read the CSV file, process each row, and write to the output file
with open(input_csv, 'r', newline='') as infile, open(output_csv, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        # Remove line breaks from each element in the row
        processed_row = [remove_line_breaks(cell) for cell in row]
        writer.writerow(processed_row)

print(f"Line breaks removed and saved to {output_csv}")

def convert_to_parquet(file):
    
    if file == "filtered_reddits.csv":
        data_type = {"index": int,"date": str , "title": str,"author": str,"link": str, "content": str, "score":int, "num_comment": int}
        df = pd.read_csv(file,dtype=data_type)    
    
    else:
        data_type = {"user_name": str,"user_location": str, "date": str,"text": str ,"hashtags": str}
        df = pd.read_csv(file,dtype=data_type)    
        df = df.drop(columns=["user_description","user_created","user_followers", "user_friends", "user_favourites","user_verified","source","is_retweet" ])
    parquet = df.to_parquet(f'./{file[:-4]}.parquet.gzip',compression='gzip')  
    return 

convert_to_parquet("filtered_reddits.csv")
# # display modified csv file 
# file2 = pd.read_csv("gfg2.csv") 
# print('\nModified file:') 
# print(file2) 
