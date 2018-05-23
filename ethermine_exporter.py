#!/usr/bin/python

import os
import json
import re
import sys
import time
import requests
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from web3 import Web3


class EthermineCollector(object):
    def __init__(self, target):
        self._currentStats = "https://api.ethermine.org/miner/{}/currentStats".format(target)

    def collect(self):
        # GET request to Ethermine API
        r = requests.get(self._currentStats)
        result = r.json()

        # Sanity check
        if result['data'] == "NO DATA":
            sys.stderr.write("Error: No data for this Ethereum address. Exiting. ")
            sys.exit(1)

        # Parse result
        for item in result['data']:
            if result['data'][item] is not None:
                # Create metric name
                snake_case = re.sub('([A-Z])', '_\\1', item).lower()

                # Create metric
                metrics = {
                    'value': GaugeMetricFamily('ethermine_{0}'.format(snake_case), 'Ethermine current statistic: {0}'.format(item))
                }
                metrics['value'].add_metric([snake_case], float(result['data'][item]))
                yield metrics['value']


if __name__ == "__main__":
    if not Web3.isAddress(os.environ['ADDRESS']):
        sys.stderr.write("Error: Invalid Ethereum address. Exiting. ")
        sys.exit(1)
    REGISTRY.register(EthermineCollector(os.environ['ADDRESS']))
    start_http_server(9118)
    while True: time.sleep(1)
