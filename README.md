This is a Python module to tell you the IP Addresses that GitHub Actions runs on. It does this by grabbing a file from Microsoft's site, parsing it and outputting the IP ranges in CIDR format for you to consume.

The IP ranges are sorted for easier diffing.

Source file is gotten from: https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519
CIDR Format: https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing