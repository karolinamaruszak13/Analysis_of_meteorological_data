import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class MonthlyAverageMeteorologicalData:
    def __init__(self, filename):
        header_list = ["STATION_ID", "STATION_NAME", "YEAR", "MONTH", "AVERAGE_MONTHLY_TEMPERATURE", "WIND_SPEED"]
        self.df = pd.read_csv(filename, header=None, usecols=[0, 1, 2, 3, 4, 8], names=header_list, sep=',',
                              engine='python')
        self.df['DATE_TIME'] = self.df['YEAR'].map(str) + '-' + self.df['MONTH'].map(str)
        self.df['DATE_TIME'] = pd.to_datetime(self.df['DATE_TIME']).dt.strftime('%Y-%m')
        del self.df['YEAR']
        del self.df['MONTH']

    def _change_index(self):
        return self.df.set_index(['STATION_ID', 'DATE_TIME'])

    def monthly_temperature_plot(self, STATION_ID):
        df = self._change_index()
        stationName = df['STATION_NAME'][STATION_ID].values[0]
        x_values = pd.DataFrame(df.groupby(['DATE_TIME'])).values[:, 0]
        x_length = np.arange(len(x_values))
        df.loc[STATION_ID]['AVERAGE_MONTHLY_TEMPERATURE']['2019-01':'2019-12'] \
            .plot(xlabel="DATE_TIME", color='lightcoral', linewidth=2, ylabel="TEMPERATURE(°C)",
                  label=f'ID:{STATION_ID}', fontsize=10)
        plt.xticks(x_length, x_values, rotation='vertical')

        plt.title(f'Average monthly temperature \nfor {stationName} station', fontsize=10)
        plt.legend()

    def monthly_wind_speed_plot(self, STATION_ID):
        df = self._change_index()
        stationName = df['STATION_NAME'][STATION_ID].values[0]
        x_values = pd.DataFrame(df.groupby(['DATE_TIME'])).values[:, 0]
        x_length = np.arange(len(x_values))
        df.loc[STATION_ID]['WIND_SPEED']['2019-01':'2019-12'] \
            .plot(xlabel="DATE_TIME", color='orange', linewidth=2, ylabel="WIND SPEED[m/s]",
                  label=f'ID:{STATION_ID}', fontsize=10)
        plt.xticks(x_length, x_values, rotation='vertical')

        plt.title(f'Average monthly wind speed \n for {stationName} station', fontsize=10)
        plt.legend()

    def monthly_temperature_sub_plots(self):
        f = plt.figure(figsize=(10, 8))

        plt.subplot(221)
        self.monthly_temperature_plot(250210050)
        plt.grid(True)

        plt.subplot(222)
        self.monthly_temperature_plot(249200130)
        plt.grid(True)

        plt.subplot(223)
        self.monthly_temperature_plot(254180090)
        plt.grid(True)

        plt.subplot(224)
        self.monthly_temperature_plot(249220150)
        plt.grid(True)

        plt.subplots_adjust(left=0.05, right=1, hspace=1, wspace=0.5)
        f.suptitle("Average monthly temperature \n for selected stations in 2019")

        plt.show()

    def monthly_wind_speed_sub_plots(self):
        f = plt.figure(figsize=(10, 8))

        plt.subplot(221)
        self.monthly_wind_speed_plot(250210050)
        plt.grid(True)

        plt.subplot(222)
        self.monthly_wind_speed_plot(249200130)
        plt.grid(True)

        plt.subplot(223)
        self.monthly_wind_speed_plot(254180090)
        plt.grid(True)

        plt.subplot(224)
        self.monthly_wind_speed_plot(249220150)
        plt.grid(True)

        plt.subplots_adjust(left=0.05, right=1, hspace=1, wspace=0.5)
        f.suptitle("Average monthly wind speed \n for selected stations in 2019")

        plt.show()


m = MonthlyAverageMeteorologicalData('k_m_t_2019.csv')

m.monthly_temperature_sub_plots()
m.monthly_wind_speed_sub_plots()
