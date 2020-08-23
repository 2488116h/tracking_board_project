from tracker import crawler


def populate():
    crawler.store_country_data()
    crawler.store_detail_data(300)
    print('Finished!')


if __name__ == '__main__':
    print('Starting Population Script...')
    populate()