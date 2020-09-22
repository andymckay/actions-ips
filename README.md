This is a Python module to tell you the IP Addresses that GitHub Actions runs on. It does this by grabbing a file from Microsoft's site, parsing it and outputting the IP ranges in CIDR format for you to consume.

IP ranges are in both IPv4 and IPv6 formats.

The IP ranges are sorted for easier diffing.

The IP ranges for macOS runners are also included.

Installing:

```bash
pip install actions-ips
```

Example usage:

```python
>>> from actions_ips import ips
>>> ips.cidrs()
['13.64.0.0/16', '13.65.0.0/16'...
```

Useful links:
* [Help documentation](https://help.github.com/en/actions/reference/virtual-environments-for-github-hosted-runners)
* [Source file](https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519)
* [CIDR Format](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
* [IPv4](https://en.wikipedia.org/wiki/IPv4_address)
* [IPv6](https://en.wikipedia.org/wiki/IPv6_address)
