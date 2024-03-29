import re
import requests

start_url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
lookup_regex = re.compile(r"https://download\.microsoft\.com/download/(.*?)\.json")
mac_ip_source = "https://maccloudipresources.z13.web.core.windows.net/resources.json"


def cidrs():
    ips = set()

    mac_ips_page = requests.get(mac_ip_source)
    mac_ips_page.raise_for_status()

    mac_ips_json = mac_ips_page.json()

    ips.update(mac_ips_json["addresses"])

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
        "AzureCloud.westus3",  # WUS3
        "AzureCloud.centralus",  # CUS
        "AzureCloud.southcentralus",  # SCUS
    ]
        
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
