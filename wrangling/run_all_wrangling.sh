#!/bin/bash
# usage: ./run_all_wrangling.sh

log_file=data_wrangling.log

if [ -f "$log_file" ]; then
  rm "$log_file"
fi

python construct_formatted_dataset.py -i ../data/videos_json -o ../data/formatted_videos >> "$log_file"

sleep 2
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++' >> "$log_file"

python extract_engagement_map.py -i ../data/formatted_videos -o ../data/engagement_map.p >> "$log_file"

sleep 2
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++' >> "$log_file"

python split_dataset_and_append_relative_engagement.py -i ../data/formatted_videos -o ../output >> "$log_file"

