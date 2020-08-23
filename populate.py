import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracking_board_project.settings')

import django

django.setup()

from tracker.crawler import store_detail_data,store_country_data


def populate():
    store_country_data()
    store_detail_data(300)



if __name__ == '__main__':
    print('Starting Population Script...')
    populate()