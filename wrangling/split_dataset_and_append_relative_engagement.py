#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Scripts to append relative engagement to VIDEOS dataset and split into train/test dataset.
Usage: python split_dataset_and_append_relative_engagement.py -i ../data/formatted_videos -o ../output
"""

import os, sys, time, datetime, pickle, argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.converter import to_relative_engagement


def extract_info(input_path, output_loc):
    """ Append relative engagement to formatted VIDEOS dataset
    :param input_path: input file path
    :param output_loc: output root dir path
    :return:
    """
    f_train = open(os.path.join(output_loc, 'train_data', os.path.basename(input_path)), 'w')
    f_train.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\n'
                  .format('id', 'publish', 'duration', 'definition', 'category', 'channel', 'topics',
                          'view30', 'watch30', 'wp30', 're30', 'days', 'daily_view', 'daily_watch'))

    with open(input_path, 'r') as fin:
        fin.readline()
        for line in fin:
            head, days, daily_view, daily_watch = line.rsplit('\t', 3)
            line_content = line.rstrip().split('\t')
            published_at = line_content[1]
            duration = int(line_content[2])
            wp30 = float(line_content[9])
            re30 = to_relative_engagement(lookup_table=engagement_map, duration=duration, wp_score=wp30, lookup_keys=split_keys)
            f_train.write('{0}\t{1}\t{2}\t{3}\t{4}'.format(head, re30, days, daily_view, daily_watch))

    f_train.close()

if __name__ == '__main__':
    # == == == == == == == == Part 1: Set up experiment parameters == == == == == == == == #
    # setting parameters
    print('>>> Start to append relative engagement and split to train dataset...')
    start_time = time.time()

    # == == == == == == == == Part 2: Load dataset == == == == == == == == #
    engagement_map_path = '../data/engagement_map.p'
    if not os.path.exists(engagement_map_path):
        print('>>> No engagement map found! Run extract_engagement_map.py first!')
        sys.exit(1)

    # load engagement map
    engagement_map = pickle.load(open(engagement_map_path, 'rb'))
    split_keys = engagement_map['duration']

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file dir of formatted VIDEOS dataset', required=True)
    parser.add_argument('-o', '--output', help='output file dir of train', required=True)
    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output

    if not os.path.exists(os.path.join(output_dir, 'train_data')):
        os.makedirs(os.path.join(output_dir, 'train_data'))
        
    # == == == == == == == == Part 3: Construct dataset == == == == == == == == #
    for subdir, _, files in os.walk(input_dir):
        for f in files:
            print('>>> Start to extract file {0}...'.format(os.path.join(subdir, f)))
            extract_info(os.path.join(subdir, f), output_dir)
    print('>>> Finish extracting all files!')

    # get running time
    print('\n>>> Total running time: {0}'.format(str(datetime.timedelta(seconds=time.time() - start_time)))[:-3])
