import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import zipfile
from pathlib import Path


def unzip(f, encoding, v):
    with zipfile.ZipFile(f) as z:
        for i in z.namelist():
            n = Path(i.encode('cp437').decode(encoding))
            if v:
                print(n)
            if i[-1] == '/':
                if not n.exists():
                    n.mkdir()
            else:
                with n.open('wb') as w:
                    w.write(z.read(i))


class MonthlyAverageMeteorologicalData:
    def __init__(self, url, download=False):
        header_list = ["STATION_ID", "STATION_NAME", "YEAR", "MONTH", "AVERAGE_MONTHLY_TEMPERATURE", "WIND_SPEED"]
        postfixes1 = [i for i in range(2001, 2021)]
        postfixes2 = []
        for i in range(1951, 2001, 5):
            postfixes2.append(f"{i}_{i + 4}")
        postfixes = postfixes1 + postfixes2
        if download:
            for postfix in postfixes:
                r = requests.get(url + f"{postfix}/{postfix}_m_k.zip")
                open(f'{postfix}.zip', 'wb').write(r.content)
                unzip(f"{postfix}.zip", 'cp932', 1)
        result = pd.DataFrame()
        for i in postfixes:
            d = pd.read_csv(f'k_m_t_{i}.csv', header=None, usecols=[0, 1, 2, 3, 4, 8], names=header_list, sep=',',
                            engine='python', encoding='unicode_escape')
            result = result.append(d)
        self.df = result
        self.df['DATE_TIME'] = self.df['YEAR'].map(str) + '-' + self.df['MONTH'].map(str)
        self.df['DATE_TIME'] = pd.to_datetime(self.df['DATE_TIME']).dt.strftime('%Y-%m')
        del self.df['MONTH']

    def _change_index(self):
        return self.df.set_index(['STATION_ID', 'DATE_TIME'])

    def monthly_temperature_plot(self, STATION_ID, YEAR):
        df = self._change_index()
        stationName = df['STATION_NAME'][STATION_ID].values[0]
        x_values = pd.DataFrame(
            df.loc[STATION_ID]['AVERAGE_MONTHLY_TEMPERATURE'][f'{YEAR}-01':f'{YEAR}-12'].groupby(['DATE_TIME'])).values[
                   :, 0]
        x_length = np.arange(len(x_values))
        df.loc[STATION_ID]['AVERAGE_MONTHLY_TEMPERATURE'][f'{YEAR}-01':f'{YEAR}-12'] \
            .plot(xlabel="DATE_TIME", color='lightcoral', linewidth=2, ylabel="TEMPERATURE(°C)",
                  label=f'ID:{STATION_ID}', fontsize=10)
        plt.xticks(x_length, x_values, rotation=30)

        plt.title(f'Average monthly temperature \nfor {stationName} station in {YEAR}', fontsize=10)
        plt.legend()

    def monthly_wind_speed_plot(self, STATION_ID, YEAR):
        df = self._change_index()
        stationName = df['STATION_NAME'][STATION_ID].values[0]
        x_values = pd.DataFrame(
            df.loc[STATION_ID]['AVERAGE_MONTHLY_TEMPERATURE'][f'{YEAR}-01':f'{YEAR}-12'].groupby(['DATE_TIME'])).values[
                   :, 0]
        x_length = np.arange(len(x_values))
        df.loc[STATION_ID]['WIND_SPEED'][f'{YEAR}-01':f'{YEAR}-12'] \
            .plot(xlabel="DATE_TIME", color='orange', linewidth=2, ylabel="WIND SPEED[m/s]",
                  label=f'ID:{STATION_ID}', fontsize=10)
        plt.xticks(x_length, x_values, rotation=30)

        plt.title(f'Average monthly wind speed \n for {stationName} station in {YEAR}', fontsize=10)
        plt.legend()

    def calculate_correlation(self, STATION_ID, YEAR):
        df = self._change_index()
        stationName = df['STATION_NAME'][STATION_ID].values[0]

        x = df.loc[STATION_ID]['AVERAGE_MONTHLY_TEMPERATURE'][f'{YEAR}-01':f'{YEAR}-12']
        y = df.loc[STATION_ID]['WIND_SPEED']['2019-01':'2019-12']

        plt.title(
            f'Correlation between average monthly wind speed\n and average monthly temperature  for {stationName} in {YEAR} ',
            fontsize=10)

        plt.scatter(x, y)
        plt.xlabel('AVERAGE_DAILY_TEMPERATURE')
        plt.ylabel('WIND_SPEED')

    def monthly_temperature_sub_plots(self):
        f = plt.figure(figsize=(10, 8))

        plt.subplot(221)
        self.monthly_temperature_plot(250210050, 2001)
        plt.grid(True)

        plt.subplot(222)
        self.monthly_temperature_plot(249200130, 2001)
        plt.grid(True)

        plt.subplot(223)
        self.monthly_temperature_plot(254180090, 2001)
        plt.grid(True)

        plt.subplot(224)
        self.monthly_temperature_plot(249220150, 2001)
        plt.grid(True)

        plt.subplots_adjust(left=0.08, right=0.95, hspace=1, wspace=0.5)
        f.suptitle("Average monthly temperature \n for selected stations")

        plt.show()

    def monthly_wind_speed_sub_plots(self):
        f = plt.figure(figsize=(10, 8))
        plt.subplot(221)
        self.monthly_wind_speed_plot(250210050, 2001)
        plt.grid(True)

        plt.subplot(222)
        self.monthly_wind_speed_plot(249200130, 2001)
        plt.grid(True)

        plt.subplot(223)
        self.monthly_wind_speed_plot(254180090, 2001)
        plt.grid(True)

        plt.subplot(224)
        self.monthly_wind_speed_plot(249220150, 2001)
        plt.grid(True)

        plt.subplots_adjust(left=0.08, right=0.95, hspace=1, wspace=0.5)
        f.suptitle("Average monthly wind speed \n for selected stations")

    def corellations_sub_plots(self):
        f = plt.figure(figsize=(10, 8))

        plt.subplot(221)
        self.calculate_correlation(250210050, 2001)
        plt.grid(True)

        plt.subplot(222)
        self.calculate_correlation(249200130, 2001)
        plt.grid(True)

        plt.subplot(223)
        self.calculate_correlation(254180090, 2001)
        plt.grid(True)

        plt.subplot(224)
        self.calculate_correlation(249220150, 2001)
        plt.grid(True)

        plt.subplots_adjust(left=0.08, right=0.95, hspace=1, wspace=0.5)
        f.suptitle(
            "Corellations between average monthly wind speed \n and average monthly temperature  for selected stations")

        plt.show()

    def calculate_anomaly(self):
        f = plt.figure(figsize=(10, 8))

        plt.subplot(111)
        anomaly = self.df.groupby("YEAR")["AVERAGE_MONTHLY_TEMPERATURE"].mean() - self.df.groupby("YEAR")["AVERAGE_MONTHLY_TEMPERATURE"].mean().mean()
        anomaly.plot(ylabel='TEMPERATURE(°C)', kind="bar")
        plt.locator_params(axis='x', nbins=20)
        plt.subplots_adjust(left=0.08, right=0.95, hspace=1, wspace=0.5)
        plt.show()




m = MonthlyAverageMeteorologicalData(
    "https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/miesieczne/klimat/")

m.monthly_temperature_sub_plots()
m.monthly_wind_speed_sub_plots()
m.corellations_sub_plots()
m.calculate_anomaly()
