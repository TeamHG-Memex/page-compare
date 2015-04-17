#!/bin/bash

import base64
import json
import os
import requests
import sys


def main():
    if len(sys.argv) == 5:
        splash_url = sys.argv[1]
        sites_path = sys.argv[2]
        run_number = int(sys.argv[3])
        output_path = sys.argv[4]
    else:
        msg = 'Usage: %s <splash url> <sites JSON> <run number> <output path>\n'
        sys.stderr.write(msg % sys.argv[0])
        sys.exit(1)

    try:
        os.makedirs(output_path)
    except OSError:
        pass

    with open(sites_path, 'r') as sites_file:
        sites = json.load(sites_file)

    os.chdir(output_path)
    splash_url = splash_url.rstrip('/') + '/render.json'
    headers = {'content-type': 'application/json'}
    params = {
        'html': 1,
        'png': 1,
        'width': 400,
        'height': 300,
        'timeout': 10,
        'images': 0,
    }

    for site, url in sites.items():
        print('Requesting %s (%s).' % (site, url))
        params['url'] = url
        response = requests.get(splash_url, headers=headers, params=params)

        if response.status_code != 200:
            print("Requested failed: %d" % response.status_code)
            continue

        body = json.loads(response.text)
        encoding = response.encoding or 'utf-8'
        filename = '%s-%d' % (site, run_number)

        with open('%s.html' % filename, 'wb') as htmlfile:
            htmlfile.write(body['html'].encode(encoding))

        with open('%s.png' % filename, 'wb') as pngfile:
            pngfile.write(base64.b64decode(body['png']))


if __name__ == '__main__':
    main()
