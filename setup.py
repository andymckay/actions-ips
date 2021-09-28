from setuptools import setup, find_packages

install_requires = [
    "requests"
]

setup(
    name="actions-ips",
    version="0.3.5",
    description="A list of the GitHub Actions IP Addresses",
    author="Andy McKay",
    author_email="andymckay@github.com",
    license="MIT",
    url="https://github.com/andymckay/actions-ips",
    zip_safe=True,
    packages=['actions_ips'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ]
)
