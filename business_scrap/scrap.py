import argparse
import sys
import urllib.request
import json
import math
import csv
import datetime

def parsing_args_and_run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--term', type=str, default='restaurants', help='Type of business you want to find')
    parser.add_argument('--location', type=str, default='Toronto', help='Business city location')
    parser.add_argument('--sortingBy', type=str, default='rating', help='Sort order for searching')
    parser.add_argument('--resultsLimit', type=float, default=200, help='Max length of list search results')
    args = parser.parse_args()
    send_request(args)

def send_request(args):
    api_key = 'Bearer IS8ZVzuJTIwSgmJ21J4IPvtt1mwkhnpJm4VlLbk88ZFD4Q4cRdHfSeVCWsVFpOg5-lE2wZqeZDjlpIoPE713bIucsBrqox85vRziSRLfss9-dGwtWWqQRMHxl_x9W3Yx'
    authorization_header = {'Authorization', api_key}
    endpoint = 'https://api.yelp.com/v3/businesses/search?'
    request_url = endpoint + 'term=' + args.term + '&location=' + args.location

    filename = str(args.resultsLimit) + args.term + datetime.datetime.today().strftime('%Y-%m-%d') + '.csv'
    init_file(args, filename)

    total_count = get_count_of_page(args)

    number_of_pages = math.ceil(total_count/50)
    print(number_of_pages)
    for index in range(0,number_of_pages):
        page_number = 50*index
        request_url = endpoint + 'term=' + args.term + '&location=' + args.location + '&sort_by=' + str(args.sortingBy) +  '&limit=50&offset=' + str(page_number)
        req = urllib.request.Request(request_url)
        req.add_header('Authorization', api_key)
        resp = urllib.request.urlopen(req)
        resp_data = resp.read()
        j = json.loads(resp_data.decode('utf-8'))
        file =  open(filename, 'a', encoding='utf-8')
        writer = csv.writer(file)
        i=index*50
        for business in j['businesses']:
            writer.writerow([str(i) ,str(business['name']), str(business['url']), str(business['phone']),str(business['rating']), str(business['location']['address1']), str(business['coordinates']['latitude']), str(business['coordinates']['longitude'])])
            i = i + 1
        file.close()


def init_file(args, filename):
    print(filename)
    file = open(filename, 'w+', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(['index','name', 'url', 'phone', 'rating', 'address', 'latitude', 'longitude'])
    file.close()

def get_count_of_page(args):
    api_key = 'Bearer IS8ZVzuJTIwSgmJ21J4IPvtt1mwkhnpJm4VlLbk88ZFD4Q4cRdHfSeVCWsVFpOg5-lE2wZqeZDjlpIoPE713bIucsBrqox85vRziSRLfss9-dGwtWWqQRMHxl_x9W3Yx'
    authorization_header = {'Authorization', api_key}
    endpoint = 'https://api.yelp.com/v3/businesses/search?'
    request_url = endpoint + 'term=' + args.term + '&location=' + args.location

    req = urllib.request.Request(request_url)
    req.add_header('Authorization', api_key)
    resp = urllib.request.urlopen(req)
    resp_data = resp.read()
    j = json.loads(resp_data.decode('utf-8'))

    total_count = j['total']
    if (args.resultsLimit != 0.0 and args.resultsLimit < total_count):
        total_count = args.resultsLimit
    return total_count


if __name__=='__main__':
    parsing_args_and_run()