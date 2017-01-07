import argparse
import datetime
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
    expiration_date = w.expiration_date
    if type(expiration_date) == list:
        return expiration_date[0]
    return expiration_date

def fix_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'http://{0}'.format(url)
    return url

def is_paid_more_then_month(expiration_date):
    if not expiration_date:
        return
    month_forward = datetime.datetime.now() - datetime.timedelta(days=30)
    return expiration_date >= month_forward

def pretty_print_check(url, expiration_date, status, need_extend):
    print('Checking site: %s' % url)
    print('Site is: {0}'.format('Available' if status else 'Offline'))
    if expiration_date:
        print('Domain expiration date: {0}'.format(expiration_date.strftime('%Y-%m-%d')))
        if need_extend:
            print('Domain {0} expires in less than one month'.format(url))
        else:
            print('Domain {0} paid more then one month'.format(url))
    else:
        print('Domain {0} now free for registration.'.format(url))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get most frequent words")
    parser.add_argument("-p", "--path", type=str, dest="filepath", required=True)
    options = parser.parse_args()
    urls = load_urls4check(options.filepath)
    for url in urls:
        status = is_server_respond_with_200(url)
        expiration_date = get_domain_expiration_date(url)
        need_extend = not is_paid_more_then_month(expiration_date)
        pretty_print_check(url, expiration_date, status, need_extend)
