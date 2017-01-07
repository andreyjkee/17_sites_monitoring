import argparse
import requests
from whois import whois


def load_urls4check(path):
    with open(path, 'r') as f:
        return [line.rstrip('\n') for line in f.readlines()]

def is_server_respond_with_200(url):
    url = fix_url(url)
    try:
        response = requests.head(url)
    except requests.ConnectionError:
        return False
    return response.status_code == 200

def get_domain_expiration_date(domain_name):
    w = whois(domain_name)
    return w.expiration_date

def fix_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'http://{0}'.format(url)
    return url

def pretty_print_check(url):
    print('Checking site: %s' % url)
    print('Site is: {0}'.format('Available' if is_server_respond_with_200(url) else 'Offline'))
    expiration_date = get_domain_expiration_date(url)
    if expiration_date:
        if type(expiration_date) == list:
            expiration_date = expiration_date[0]
        print('Domain expiration date: {0}'.format(expiration_date.strftime('%Y-%m-%d')))
    else:
        print('Domain {0} now free for registration.'.format(url))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get most frequent words")
    parser.add_argument("-p", "--path", type=str, dest="filepath", required=True)
    options = parser.parse_args()
    urls = load_urls4check(options.filepath)
    for url in urls:
        pretty_print_check(url)
