<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#installation">Installation</a></li>
  </ol>
</details>



## About The Project

Social media subscribers/followers count tracker for crypto currency projects.

Fetches top 250 crypto projects from Coingecko API. Processes relevant datapoints. Detects missing social media platfrom links and scrapes them either from official homepages of the projects or from google search. Validates all links. Stores all the data into the SQLite database. Data not specifically relevant for the subscribers tracker is also included and saved, i.e. market data, coingecko ratings, developer stats etc. which can be used for other purposes with further development of the project.

This app is published for showcase, it doesn't have a user interface, it's a small part/service of a bigger cryptocurrency trading bot project. It runs as a command line process, which invokes several routines in set intervals which perform the steps mentioned above.

</br>

### Built With
- Python 3.11.3
- SQLite
- SQLAlchemy

- Beautiful Soup
- Playwright
- Tweepy


</br>



## Getting Started

For demonstration purposes the app can be run as a stand alone script. The results can be observed in the SQLite database by querying the database from the terminal or using any GUI tool. Demo version only tracks subscribers for top 10 crypto currencies and doesn't include twitter followers, because Twitter API tokens are required for it to work.

</br>



## Prerequisites

An SQLite installation is required on your local machine.

### Debian/Ubuntu
```sh
apt-get install sqlite3
```

###  **Arch**
```sh
sudo pacman -S sqlite
```

### **Windows**

Follow the instructions on the official website:

https://www.sqlite.org/download.html

</br>



## Installation

1. Clone the repo.
   ```sh
   git clone https://github.com/dkzn1/crypto-subscribers-count-tracker
   ```
2. Create and activate a virtual environment.
   ```sh
   python3 -m venv venv
   ```
   ```sh
   source venv/bin/activate
   ```
3. Install dependency packages.
   ```sh
   pip install -r requirements.txt
   ```

   </br>



## Usage

1. Switch to the project directory.
   ```sh
   cd .../crypto-subscribers-count-tracker
   ```
2. Run the process from your terminal.
   ```sh
   python3 src/main.py
   ```
3. Open SQLite database.
   ```sh
   sqlite3 data/database.db
   ```
