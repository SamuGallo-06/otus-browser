[![Qt](https://img.shields.io/badge/Qt-2CDE85?logo=Qt&logoColor=fff)](#)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)


<img src="src/resources/otus_logo.png" alt="Otus Browser Logo" width="200"/>

# Otus Browser

Otus is a lightweight, privacy-first Linux browser built with Python and Qt, with no telemetry, trackers, or Google services. Named after the scops owl: quiet, discreet, and hard to spot.

## Features

- **Privacy-first**: No telemetry, trackers, or Google services.
- **Minimal, but retro**: A simple, clean interface reminiscent of early web browsers like Internet Explorer, without the bloat of modern browsers.
- **Crypted profiles**: Each user profile can be encrypted with gocryptfs, ensuring that your browsing data remains private and secure. This feature is optional, and you can choose to use unencrypted profiles if you prefer.

## Dependencies

- Python 3.10 or higher
- Python modules listed in `requirements.txt` (run `pip install -r requirements.txt` to install)
- gocryptfs
