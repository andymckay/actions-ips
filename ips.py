import re
import requests
import subprocess
import sys
import time

url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
lookup_regex = re.compile(r"https://download\.microsoft\.com/download/(.*?)\.json")

def cidrs():
    page = requests.get(url)
    page.raise_for_status()

    # You should never do a regex search on HTML, but I think in this case we'll be ok. Grep the page to find the download JSON file.
    searched = lookup_regex.search(page.content.decode("utf8"))
    # Couldn't find the regex on the page.
    assert searched
    url = searched.group()

    # Now go get the JSON data.
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    regions = [
        "AzureCloud.eastus2",  # EUS2
        "AzureCloud.eastus",  # EUS
        "AzureCloud.westus",  # WUS
        "AzureCloud.westus2",  # WUS2
        "AzureCloud.centralus",  # CUS
        "AzureCloud.southcentralus",  # SCUS
    ]

    ips = set()

    # Add in the hard coded Mac IPs in CIDR format to join the downloaded IPs.
    for line in open('macips.txt'):
        ips.add(line.strip())

    for line in data["values"]:
        if line["name"] in regions:
            for address in line["properties"]["addressPrefixes"]:
                ips.add(address)

    def sort(address):
        bits = address.split(".")
        # Lets split the last on the / to make it easy to order.
        last = bits[-1].split("/")
        return list(map(int, bits[:3] + last))

    ips = sorted(ips, key=sort)
    return ips

if __name__=='__main__':
    results = cidrs()
    for result in results:
        print(result)