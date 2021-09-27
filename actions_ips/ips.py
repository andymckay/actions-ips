import re
import requests
import subprocess
import sys
import time

start_url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
lookup_regex = re.compile(r"https://download\.microsoft\.com/download/(.*?)\.json")
mac_ips = """13.105.49.106/31
13.105.49.96/31
13.105.49.46/31
13.105.49.180/31
13.105.49.80/31
13.105.49.52/31
13.105.49.154/31
13.105.49.38/31
13.105.49.108/31
13.105.49.2/31
13.105.49.182/31
13.105.49.16/31
13.105.49.30/31
13.105.49.48/31
13.105.49.66/31
13.105.49.174/31
13.105.49.24/31
13.105.49.98/31
13.105.49.50/31
13.105.49.164/31
13.105.49.40/31
13.105.49.12/31
13.105.49.84/31
13.105.49.158/31
13.105.49.42/31
13.105.49.26/31
13.105.49.94/31
13.105.49.88/31
13.105.49.32/31
13.105.49.20/31
13.105.49.6/31
13.105.49.104/31
13.105.49.22/31
13.105.49.102/31
13.105.49.10/31
13.105.49.14/31
13.105.49.160/31
13.105.49.170/31
13.105.49.34/31
13.105.49.68/31
13.105.49.60/31
13.105.49.156/31
13.105.49.162/31
13.105.49.152/31
13.105.49.56/31
13.105.49.4/31
13.105.49.168/31
13.105.49.100/31
13.105.49.28/31
13.105.49.36/31
13.105.49.58/31
13.105.49.126/31
13.105.49.64/31
13.105.49.18/31
13.105.49.112/31
13.105.49.74/31
13.105.49.54/31
13.105.49.166/31
13.105.49.70/31
13.105.49.172/31
13.105.49.178/31
13.105.49.110/31
13.105.49.86/31
13.105.49.62/31
13.105.49.90/31
13.105.49.44/31
13.105.49.82/31
13.105.49.76/31
13.105.49.176/31
13.105.49.114/31
13.105.49.8/31
13.105.49.92/31
13.105.49.0/31
13.105.49.72/31
13.105.49.78/31
199.7.166.8/29
199.19.85.24/29
199.19.85.224/29
208.83.5.224/29
199.19.85.64/29
208.78.110.56/29"""

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
    for ip in mac_ips.split("\n"):
        ips.add(ip)
        
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
