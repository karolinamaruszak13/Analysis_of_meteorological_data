import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class DailyAverageMeteorologicalData:
    def __init__(self, *args):
        header_list = ["STATION_ID", "STATION_NAME", "YEAR", "MONTH", "DAY", "AVERAGE_DAILY_TEMPERATURE", "WIND_SPEED"]
        dfs = [
            pd.read_csv(filename, header=None, usecols=[0, 1, 2, 3, 4, 5, 9], names=header_list, sep=',',
                        engine='python')
            for filename in args]
        self.df = pd.concat(dfs, ignore_index=True)
        self.df['DATE_TIME'] = self.df['YEAR'].map(str) + '-' + self.df['MONTH'].map(str) + '-' + self.df['DAY'].map(
            str)
        self.df['DATE_TIME'] = pd.to_datetime(self.df['DATE_TIME']).dt.strftime('%Y-%m-%d')
        del self.df['YEAR']

    def _month_to_string(self, MONTH):
        if MONTH == 1:
            return "January"
        elif MONTH == 2:
            return "February"
        elif MONTH == 3:
            return "March"
        elif MONTH == 4:
            return "April"
        elif MONTH == 5:
            return "May"
        elif MONTH == 6:
            return "June"
        elif MONTH == 7:
            return "July"
        elif MONTH == 8:
            return "August"
        elif MONTH == 9:
            return "September"
        elif MONTH == 10:
            return "October"
        elif MONTH == 11:
            return "November"
        elif MONTH == 12:
            return "December"

    def set_df_index(self):
        return self.df.set_index(['STATION_ID', 'MONTH', 'DATE_TIME'])

    def daily_temperature_plot(self, STATION_ID, MONTH):
        df = self.set_df_index()
        x_values = pd.DataFrame(df.groupby(['DAY'])).values[:, 0]
        x_length = np.arange(len(x_values))
        stationName = df['STATION_NAME'][STATION_ID].values[0]

        if MONTH < 10:
            df.loc[STATION_ID, MONTH]['AVERAGE_DAILY_TEMPERATURE'][f'2019-0{MONTH}-01':f'2019-0{MONTH}-31'] \
                .plot(xlabel="DAYS", color='g', linewidth=2, ylabel="TEMPERATURE(°C)",
                      label=f'ID:{STATION_ID}', fontsize=8)
        else:
            df.loc[STATION_ID, MONTH]['AVERAGE_DAILY_TEMPERATURE'][f'2019-{MONTH}-01':f'2019-{MONTH}-31'] \
                .plot(xlabel="DAYS", color='g', linewidth=2, ylabel="TEMPERATURE(°C)",
                      label=f'ID:{STATION_ID}', fontsize=10)
        plt.xticks(x_length, x_values, fontsize=7)
        plt.title(f'Average daily temperature \n in {self._month_to_string(MONTH)} for {stationName} ', fontsize=10)
        plt.legend()

    def daily_wind_speed_plot(self, STATION_ID, MONTH):
        df = self.set_df_index()
        x_values = pd.DataFrame(df.groupby(['DAY'])).values[:, 0]
        x_length = np.arange(len(x_values))
        stationName = df['STATION_NAME'][STATION_ID].values[0]

        if MONTH < 10:
            df.loc[STATION_ID, MONTH]['WIND_SPEED'][f'2019-0{MONTH}-01':f'2019-0{MONTH}-31'] \
                .plot(xlabel="DAYS", color='black', linewidth=2, ylabel="WIND SPEED[m/s]",
                      label=f'ID:{STATION_ID}', fontsize=8)
        else:
            df.loc[STATION_ID, MONTH]['WIND_SPEED'][f'2019-{MONTH}-01':f'2019-{MONTH}-31'] \
                .plot(xlabel="DAYS", color='black', linewidth=2, ylabel="WIND SPEED[m/s]",
                      label=f'ID:{STATION_ID}', fontsize=10)
        plt.xticks(x_length, x_values, fontsize=7)
        plt.title(f'Average daily wind speed \n in {self._month_to_string(MONTH)} for {stationName} ', fontsize=10)
        plt.legend()

    def daily_temperature_sub_plots(self):
        f = plt.figure(figsize=(15, 8))

        plt.subplot(221)
        self.daily_temperature_plot(250210050, 2)
        plt.grid(True)

        plt.subplot(222)
        self.daily_temperature_plot(249200130, 9)
        plt.grid(True)

        plt.subplot(223)
        self.daily_temperature_plot(254180090, 6)
        plt.grid(True)

        plt.subplot(224)
        self.daily_temperature_plot(249220150, 12)
        plt.grid(True)

        plt.subplots_adjust(left=0.05, right=1, hspace=1, wspace=0.5)
        f.suptitle("Average daily temperature \n for selected stations in the selected month")

        plt.show()

    def daily_wind_speed_sub_plots(self):
        f = plt.figure(figsize=(15, 8))

        plt.subplot(221)
        self.daily_wind_speed_plot(250210050, 2)
        plt.grid(True)

        plt.subplot(222)
        self.daily_wind_speed_plot(249200130, 9)
        plt.grid(True)

        plt.subplot(223)
        self.daily_wind_speed_plot(254180090, 6)
        plt.grid(True)

        plt.subplot(224)
        self.daily_wind_speed_plot(249220150, 12)
        plt.grid(True)

        plt.subplots_adjust(left=0.05, right=1, hspace=1, wspace=0.5)
        f.suptitle("Average daily wind speed \n for selected stations in the selected month")

        plt.show()


d = DailyAverageMeteorologicalData('k_d_t_01_2019.csv', 'k_d_t_02_2019.csv', 'k_d_t_03_2019.csv', 'k_d_t_04_2019.csv',
                                   'k_d_t_05_2019.csv', 'k_d_t_06_2019.csv', 'k_d_t_07_2019.csv', 'k_d_t_08_2019.csv',
                                   'k_d_t_09_2019.csv', 'k_d_t_10_2019.csv', 'k_d_t_11_2019.csv', 'k_d_t_12_2019.csv')

d.daily_temperature_sub_plots()
d.daily_wind_speed_sub_plots()
