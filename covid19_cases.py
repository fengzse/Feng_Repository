import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Download current data and save it as local file
json_url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
req = requests.get(json_url)
with open('covid19_cases_trend.json', 'w', encoding="utf-8") as f:  # GBK encoding error,，set:encoding="utf-8"
    f.write(req.text)  # .text返回的是Unicode型的数据，一般用于返回的文本
req.json()  # 配合request调用，.json()解码json格式数据给Python

# Open the file, read datas
filename = 'covid19_cases_trend.json'
with open(filename) as fn:
    covid19 = json.load(fn)


class Cov19Cases:
    def __init__(self, states):
        self.states = states
        self.infections = {}
        self.deaths = {}
        self.state_cases = []
        self.state_deaths = []
        self.dates = {}
        self.state_dates = []
        self.sum_infections = {}
        self.sum_deaths = {}
        self.total_infections = 0
        self.total_deaths = 0

    def national_data(self):
        # states as keys，incretments and dates as values，recall: to sort by reverse
        for state in self.states:
            for cases in covid19['records']:
                if cases['countriesAndTerritories'] == state:
                    self.state_cases.append(int(cases['cases']))
                    self.state_deaths.append(int(cases['deaths']))
                    self.state_dates.append(datetime.strptime(cases['dateRep'], '%d/%m/%Y'))
                    self.dates[cases['countriesAndTerritories']] = self.state_dates
                    self.infections[cases['countriesAndTerritories']] = self.state_cases
                    self.deaths[cases['countriesAndTerritories']] = self.state_deaths
            self.state_cases = []
            self.state_deaths = []
            self.state_dates = []
        for key, value in self.infections.items():
            sort_value = value[::-1]
            self.infections[key] = sort_value

        for ky, val in self.deaths.items():
            sort_val = val[::-1]
            self.deaths[ky] = sort_val

        for state, date in self.dates.items():
            sort_date = date[::-1]
            self.dates[state] = sort_date
        return self.infections, self.deaths, self.dates

    # 此处调用注意，要调用下面两个函数必须先调用national_data，调用后infections，deaths和dates三个字典才有值
    def national_sum(self):
        # sort and sum the values
        for key, value in self.infections.items():
            self.sum_infections[key] = sum(value)
        for ky, val in self.deaths.items():
            self.sum_deaths[ky] = sum(val)
        print(self.sum_infections, self.sum_deaths)
        return self.sum_infections, self.sum_deaths


def world_sum():  # 应该计算所有的cases和deaths
    total_infc = 0
    total_dea = 0
    for wi in covid19['records']:
        total_infc += int(wi['cases'])
        total_dea += int(wi['deaths'])
    print('world sum: ', total_infc, total_dea)
    return [total_infc, total_dea]


def search_states():
    states = []
    print('For US enter us' + '\n' + 'For South Korea enter sk' + '\n' + 'For UK enter uk')
    state = ''
    while state != 'Q':
        state = input('Please enter names of states,enter q to quit: ').title()
        if state == 'Us':
            state = 'United_States_of_America'
        if state == 'Sk':
            state = 'South_Korea'
        if state == 'Uk':
            state = 'United_Kingdom'
        states.append(state)
    print(states)
    return states


def chart_infections():
    info = Cov19Cases(search_states())
    info.national_data()
    fig = plt.figure(dpi=128, figsize=(10, 6))
    for key in info.infections.keys():
        plt.plot(info.dates[key], info.infections[key])
        plt.legend(labels=info.infections.keys(), loc='upper left')
    plt.title('Daily Increment', fontsize=24)
    plt.xlabel('Dates', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('Daily Confirmed', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.grid(True)
    plt.show()


def chart_deaths():
    info = Cov19Cases(search_states())
    info.national_data()
    fig = plt.figure(dpi=128, figsize=(10, 6))
    for key in info.deaths.keys():
        plt.plot(info.dates[key], info.deaths[key])
        plt.legend(labels=info.deaths.keys(), loc='upper left')
    plt.title('Daily Deaths', fontsize=24)
    plt.xlabel('Dates', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('Daily Confirmed', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.grid(True)
    plt.show()


def chart_sum_infections():
    info = Cov19Cases(search_states())
    info.national_data()
    info.national_sum()
    world_sum()
    fig = plt.figure(dpi=128, figsize=(10, 6))
    for key in info.sum_infections.keys():
        plt.bar(key, info.sum_infections[key], width=0.35)
        plt.legend(labels=info.sum_infections.keys(), loc='upper left', fontsize=10)  # 为什么这里的label不能等于key？
    plt.title('Infections in Selected States\n'+'Global infected: '+str(world_sum()[0]), fontsize=20)
    plt.xlabel('States', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('Total Confirmed', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.grid(True)
    plt.show()


def chart_sum_death():
    info = Cov19Cases(search_states())
    info.national_data()
    info.national_sum()

    fig = plt.figure(dpi=128, figsize=(10, 6))
    for key in info.sum_deaths.keys():
        plt.bar(key, info.sum_deaths[key], width=0.35)
        plt.legend(labels=info.sum_deaths.keys(), loc='upper left', fontsize=10)  # 为什么这里的label不能等于key？
    plt.title('Deaths in Selected States\n'+'Global Deaths'+str(world_sum()[1]), fontsize=20)
    plt.xlabel('States', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('Amount', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.grid(True)
    plt.show()


chart_sum_infections()
