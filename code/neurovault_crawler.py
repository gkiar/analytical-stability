#!/usr/bin/env python

from argparse import ArgumentParser
import requests
import json
import os.path as op
import os

baseurl = "https://neurovault.org/api/images/"


def gen_neurovault_getter(limit=1, offset=0, record=[], verb=False):
    # Create a function for getting data easily
    def nv_getter(next_url=None):
        # Creating request URLs
        record_urls = list()
        # Case 1: a specific record ID was provided
        if record:
            for rec in record:
                record_urls.append("{0}{1}/".format(baseurl, rec))

        else:
            # Case 2: a specific URL was provided
            if next_url:
                record_urls.append(next_url)

            # Case 3: we need to create a url with offset an limit parameters
            else:
                record_urls.append("{0}/?limit={1}&offset={2}".format(baseurl,
                                                                      limit,
                                                                      offset))
        # Once URLs are established, crawl them
        record_data = list()
        if verb:
            print(">> Preparing to request {0} URLs".format(len(record_urls)))
        for record_url in record_urls:
            if verb:
                print(">>   Requesting URL: {0}".format(record_url))
            tmp_data = requests.get(record_url).json()
            next_url = tmp_data.get("next") or None

            # In the listing mode, data is in a field called "results"
            if record:
                record_data.append(tmp_data)
            if not record:
                tmp_data = [t for t in tmp_data['results']]
                record_data += tmp_data

        return next_url, record_data
    return nv_getter


def grab_info(results):
    verb = results.verbose
    nv_meta_getter = gen_neurovault_meta_getter(limit=results.limit,
                                                offset=results.offset,
                                                record=results.record,
                                                verb=verb)

    image_data = list()
    next_url = None
    counter = 0
    #  until full or the list stops growing
    while len(image_data) < results.total and counter < results.max_iter:
        next_url, tmp_data = nv_meta_getter(next_url)
        image_data += tmp_data
        counter += 1
        if verb:
            print("Records Retrieved: {0}".format(len(image_data)))
            print("========================")

    # Print output to screen...
    if not results.metadata:
        print(json.dumps(image_data, indent=4))

    # ... Or save it to a file
    else:
        with open(results.metadata, 'w') as fhandle:
            fhandle.write(json.dumps(image_data, indent=2))

def grab_images(results):
    verb = results.verbose

    with open(results.metadata) as fhandle:
        image_info_list = json.loads(fhandle.read())

    os.system("mkdir -p {0}".format(results.outdir))
    for idx, meta_image in enumerate(image_info_list):
        if idx >= results.max_iter:
            break

        tmp_dir = op.join(results.outdir, str(meta_image['id']))
        os.system("mkdir -p {0}".format(tmp_dir))
        file_data = requests.get(meta_image["file"])

        ofile = op.join(tmp_dir, op.basename(meta_image['file']))
        with open(ofile, 'wb') as fhandle:
            fhandle.write(file_data.content)


def driver():
    parser = ArgumentParser(__file__,
                            description="Crawler for Neurovault image maps.")
    parser.add_argument("mode", choices=["info", "images"], default="info",
                        help="Mode of operation for the crawler. The 'info' "
                             "mode must be run first, as it will grab the "
                             "metadata for all files of interest. The 'images'"
                             " mode will then grab the Nifti file for each.")
    parser.add_argument("--record", "-r", action="store", type=int, default=[],
                        nargs="+",
                        help="Specific image ID. Only used by 'info'.")
    parser.add_argument("--limit", "-l", action="store", type=int,
                        default=1,
                        help="Number of records to get per API call.")
    parser.add_argument("--total", "-t", action="store", type=int,
                        default=1,
                        help="Number of total records to get. Only used by "
                             "'info'.")
    parser.add_argument("--offset", "-o", action="store", type=int,
                        default=0,
                        help="Record offset for getting records. Only used by "
                             "'info'.")
    parser.add_argument("--max_iter", "-i", action="store", type=int,
                        default=10000,
                        help="Maximum number of API calls to make.")
    parser.add_argument("--metadata", "-m", action="store", type=str,
                        help="File for saving the acquired metadata.")
    parser.add_argument("--outdir", "-d", action="store", type=str,
                        help="Directory for storing output maps. Only used by "
                             "'images'.")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Toggles verbose print statements.")
    results = parser.parse_args()

    if results.mode == "info":
        grab_info(results)
    elif results.mode == "images":
        grab_images(results)


if __name__ == "__main__":
    driver()
