import sys
import requests


def get_video_id(url):

    # remove slash from the end of the url
    if url[-1] == '/':
        filtered_url = url[:-1]
    else:
        filtered_url = url

    # get video id from url
    result = filtered_url.split('/')[-1]

    return result


def get_video_config(id):
    # set video config url
    video_config_url = 'https://player.vimeo.com/video/' + id + '/config'

    # send get request to get video json config
    video_config_response = requests.get(video_config_url)

    # generate obj from json
    config = video_config_response.json()

    return config


def find_required_quality_height(video_config, required_quality):
    # video config
    target_video_config = None

    # check all video find the closest one
    for video_config in video_config['request']['files']['progressive']:

        # skip first video
        if target_video_config is None:
            target_video_config = video_config
            continue

        # get video height
        video_height = video_config['height']

        # check video height
        video_height_diff = abs(required_quality - video_height)
        target_video_height_diff = abs(required_quality - target_video_config['height'])

        # check video height diff
        if video_height_diff < target_video_height_diff:
            target_video_config = video_config

    return target_video_config


def download_video(download_url, file_name):
    # download video
    video_response = requests.get(download_url)

    # open file and write content there
    video_file = open(file_name, 'wb')
    video_file.write(video_response.content)
    video_file.close()


# main sequence of the program
target_video_url = sys.argv[1]
video_id = get_video_id(target_video_url)
video_config_json = get_video_config(video_id)
target_pr_config = find_required_quality_height(video_config_json, 480)
video_url = target_pr_config['url']
video_file_name = video_id + '_' + target_pr_config['quality'] + '.mp4'
download_video(video_url, video_file_name)
print('downloaded: ' + video_file_name)
