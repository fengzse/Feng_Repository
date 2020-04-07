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
        self.states = states  # 将带入的国家列表参数
        self.infections = {}  # 每个国家的每日新增汇总，记录的是每天当天数据
        self.deaths = {}  # 每个国家的每日新增死亡，记录的是每天当天数据
        self.state_cases = []  # 用于在遍历中存储每天的感染数据，最后作为value，国家作为key添加进self.infections = {}
        self.state_deaths = []  # 用于在遍历中存储每天的死亡数据，最后作为value，国家作为key添加进self.deaths = {}
        self.dates = {}  # key为国家，value记录时间
        self.state_dates = []  # 用于在遍历中存储每天的时间数据，最后作为value，国家作为key添加进self.dates = {}
        self.sum_infections = {}  # 记录截至调用数据当天每个国家的感染总数
        self.sum_deaths = {}  # 记录截至调用数据当天每个国家的死亡总数
        self.total_infections = 0  # 用于计算world_sum的初始变量
        self.total_deaths = 0  # 用于计算world_sum的初始变量
        self.daily_sum_infc = {}  # 用于记录随时间线的阶段性感染总数
        self.daily_sum_dea = {}  # 用于记录随时间线的阶段性死亡总数

    # 收集添加所有需要的数据，依国别建立字典，所有的value全部重新反序排列
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
            sort_value = value[::-1]  # 原value的值按时间是从后往前排的，要获得正确的时间顺序，要反序排列value
            self.infections[key] = sort_value

        for ky, val in self.deaths.items():
            sort_val = val[::-1]  # 同上
            self.deaths[ky] = sort_val

        for state, date in self.dates.items():
            sort_date = date[::-1]  # 同上
            self.dates[state] = sort_date
        return self.infections, self.deaths, self.dates

    # 此处调用注意，要调用下面2个函数必须先调用national_data，调用后self的那些字典才有值

    # 原来想要通过时间线比对和国家比对后再逐天计算阶段性总量，见代码后面的大段注释，但是效率太低
    # 通过下面遍历列表，并用value[i] = value[i] + value[i - 1]的方式逐个增加赋值，实现每天对每天以前的所有值阶段性加总
    # 特别注意，这个方法调用后会改变self.infections和self.deaths这两个字典的value值，因为方法中对value进行了修改
    # 因此，不要和另外两个方法放在一起调用，代码语法没错，但是会导致绘图错误属于逻辑错误
    def daily_national_sum(self):
        daily_sum = []
        for key, value in self.infections.items():
            for i in range(len(value)):
                if i == 0:
                    daily_sum.append(value[i])
                else:
                    value[i] = value[i] + value[i - 1]
                    daily_sum.append(value[i])
            self.daily_sum_infc[key] = daily_sum
            daily_sum = []

        for key, value in self.deaths.items():
            for i in range(len(value)):
                if i == 0:
                    daily_sum.append(value[i])
                else:
                    value[i] = value[i] + value[i - 1]
                    daily_sum.append(value[i])
            self.daily_sum_dea[key] = daily_sum
            daily_sum = []
        print(self.daily_sum_infc, self.daily_sum_dea)
        return self.daily_sum_infc, self.daily_sum_dea

    def national_sum(self):
        # sort and sum the values
        for key, value in self.infections.items():
            self.sum_infections[key] = sum(value)
        for ky, val in self.deaths.items():
            self.sum_deaths[ky] = sum(val)
        print(self.sum_infections, self.sum_deaths)
        return self.sum_infections, self.sum_deaths


def world_sum():  # 计算所有cases和deaths的总量，得到总值
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


# 要实现x坐标轴是递增总量，y是单日增量，要如下调用
#    info = Cov19Cases(search_states())
#    info.national_data()
#    info.daily_national_sum()
#    info.national_data()  上一层调用会改变value值，因此必须把value改回来。但上层调用后修改值已经被存储到相应字典里，因此
#      把value值改回来不会影响self.daily_sum_infc和self.daily_sum_dea的values里的值
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
    for key in info.deaths.keys():  # 这里的key可以迭代出国家名，放入info.dates[key]，可以找出相同国家的时间线
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
    plt.title('Infections in Selected States\n' + 'Global infected: ' + str(world_sum()[0]), fontsize=20)
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
    plt.title('Deaths in Selected States\n' + 'Global Deaths: ' + str(world_sum()[1]), fontsize=20)
    plt.xlabel('States', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('Amount', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.grid(True)
    plt.show()


chart_infections()
chart_deaths()

'''
# 这一部分运行效率太低，舍弃，但是部分写法以后可以借鉴
def world_wide():
    # 单日全球感染汇总:
    world_infc = []
    world_dea = []
    daily_infc_sum = []
    daily_dea_sum = []
    # 提取所有的时间，转换成整数时间戳，反序，最后排除重复的元素
    dates_lst = [int(time.mktime(time.strptime(world['dateRep'], '%d/%m/%Y'))) for world in covid19['records']][::-1]
    set_dates_lst = [dates_lst[j] for j in range(len(dates_lst)) if dates_lst[j] != dates_lst[j:]]
    print(set_dates_lst)

    for i in range(len(set_dates_lst)):  # 遍历时间列表，按时间分类
        daily_in = [(int(world['cases'])) for world in covid19['records'] if set_dates_lst[i] ==
                    int(time.mktime(time.strptime(world['dateRep'], '%d/%m/%Y')))]  # 每日全球各国新增汇总
        daily_d = [(int(world['deaths'])) for world in covid19['records'] if set_dates_lst[i] ==
                   int(time.mktime(time.strptime(world['dateRep'], '%d/%m/%Y')))]
        daily_infc_sum.append(sum(daily_in))  # 每天的cases加总
        daily_dea_sum.append(sum(daily_d))
    print(daily_infc_sum)

    world_infc.append(reduce(lambda x, y: x + y, daily_infc_sum[::-1]))  # 随日期加总
    world_dea.append(reduce(lambda x, y: x + y, daily_dea_sum[::-1]))  # 随日期加总
    return world_infc, world_dea


print(world_wide())'''
