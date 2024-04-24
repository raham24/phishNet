import socket
import urllib.parse
import requests
from bs4 import BeautifulSoup
import whois
import datetime
import numpy as np
import pandas as pd

def check_url(url):
    # Having IP Address
    try:
        ip = urllib.parse.urlparse(url).netloc
        ip_address = socket.gethostbyname(ip)
        if ip_address:
            having_IP_Address = 1
        else:
            having_IP_Address = -1
    except:
        having_IP_Address = -1

    # URL Length
    if len(url) < 54:
        URL_Length = 1
    elif 54 <= len(url) <= 70:
        URL_Length = 0
    else:
        URL_Length = -1

    # Shortining Service
    try:
        response = requests.get(url)
        if response.history:
            Shortining_Service = 1
        else:
            Shortining_Service = -1
    except:
        Shortining_Service = -1
    # Having At Symbol
    if "@" in urllib.parse.urlparse(url).netloc:
        having_At_Symbol = 1
    else:
        having_At_Symbol = -1

    # Double Slash Redirecting
    if "//" in urllib.parse.urlparse(url).path:
        double_slash_redirecting = 1
    else:
        double_slash_redirecting = -1

    # Having Sub Domain
    if len(urllib.parse.urlparse(url).netloc.split(".")) > 2:
        having_Sub_Domain = 1
    else:
        having_Sub_Domain = -1

    # SSLfinal State
    try:
        response = requests.get(url, verify=True)
        if response.status_code == 200:
            SSLfinal_State = 1
        else:
            SSLfinal_State = -1
    except:
        SSLfinal_State = -1

    # Abnormal URL
    if any(char.isdigit() for char in urllib.parse.urlparse(url).netloc) and \
        not urllib.parse.urlparse(url).netloc.startswith('www.'):
        Abnormal_URL = 1
    else:
        Abnormal_URL = -1

    # Age of Domain
    try:
        domain = whois.whois(urllib.parse.urlparse(url).netloc)
        if datetime.datetime.now().year - domain.creation_date.year > 1:
            age_of_domain = 1
        else:
            age_of_domain = -1
    except:
        age_of_domain = -1

    # Page Rank
    try:
        response = requests.get("https://www.webpageanalyse.com/checkpagerank.php?url="+url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rank = soup.find('div', {'class': 'col-md-4'}).text.strip()
        if rank != "":
            Page_Rank = int(rank)
        else:
            Page_Rank = -1
    except:
        Page_Rank = -1

    # Google Index
    try:
        response = requests.get("https://www.google.com/search?q=site:"+urllib.parse.urlparse(url).netloc)
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find('div', {'class': 'g'}):
            Google_Index = 1
        else:
            Google_Index = -1
    except:
        Google_Index = -1


    # convert list to numpy array
    df = pd.DataFrame({
        'id' : [1],
        'having_IP_Address' : [having_IP_Address], #
        'URL_Length' : [URL_Length], #
        'Shortining_Service' : [Shortining_Service],
        'having_At_Symbol' : [having_At_Symbol], #
        'double_slash_redirecting' : [double_slash_redirecting], 
        'having_Sub_Domain' : [having_Sub_Domain], #
        'SSLfinal_State' : [SSLfinal_State], #
        'Abnormal_URL' : [Abnormal_URL],#
        'age_of_domain' : [age_of_domain],
        'Page_Rank' : [Page_Rank],
        'Google_Index' : [Google_Index]
    })

    return df

if __name__ == "__main__":
    url = "https://mail.google.com/"
    df = check_url(url)
    print(df.to_string())

