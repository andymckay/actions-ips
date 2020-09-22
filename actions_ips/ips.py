import re
import requests
import subprocess
import sys
import time

start_url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
lookup_regex = re.compile(r"https://download\.microsoft\.com/download/(.*?)\.json")

def cidrs():
    page = requests.get(start_url)
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

    zones = [
        "AzureCloud.eastus2",  # EUS2
        "AzureCloud.eastus",  # EUS
        "AzureCloud.westus",  # WUS
        "AzureCloud.westus2",  # WUS2
        "AzureCloud.centralus",  # CUS
        "AzureCloud.southcentralus",  # SCUS
    ]

    ips = set()

    # Add in the hard coded Mac IPs in CIDR format to join the downloaded IPs.
    ips.add("199.7.166.9/32")
    ips.add("199.7.166.10/31")
    ips.add("199.19.85.25/32")
    ips.add("199.19.85.26/31")
    ips.add("208.83.5.226/31")
    ips.add("208.83.5.228/31")
    ips.add("208.83.5.230/32")

    # MacCloud v2 IPs
    ips.add("143.55.64.0/23")

    for line in data["values"]:
        if line["name"] in zones:
            for address in line["properties"]["addressPrefixes"]:
                ips.add(address)

    def sort(address):
        version = "ipv6" if ":" in address else "ipv4"
        if version == "ipv4":
            bits = address.split(".")
            last = bits[-1].split("/")
            return list(map(int, bits[:3] + last))
        else:
            def int16(x):
                if not x:
                    return 0
                return int(x.replace('/', ''), 16)
            bits = address.split(":")
            return list(map(int16, bits))

    ips = sorted(ips, key=sort)
    return ips

if __name__=='__main__':
    results = cidrs()
    for result in results:
        print(result)