import os
from datetime import date

import requests
import pandas as pd
from bs4 import BeautifulSoup


def main():
    url = 'https://guineasalud.org/estadisticas/'
    location = "Equatorial Guinea"
    output_file = f'automated_sheets/{location}.csv'

    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    stats = soup.find_all('tr')
    count = int(stats[9].find_all('td')[-1].text)
    # print(count)

    date_str = date.today().strftime("%Y-%m-%d")
    df = pd.DataFrame({
        'Country': location,
        'Date': [date_str],
        'Cumulative total': count,
        'Source URL': url,
        'Source label': 'Ministerio de Sanidad y Bienestar Social',
        'Units': 'tests performed'
    })

    if os.path.isfile(output_file):
        existing = pd.read_csv(output_file)
        df = pd.concat([df, existing]).sort_values('Date', ascending=False)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
