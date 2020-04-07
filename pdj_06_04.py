def main():
    import os
    if os.path.exists('covis.csv'):
        if os.path.getmtime('covid.csv') >= 3600:
            getFile()
    else:
        getFile()
    if input("Do you want to see cases for specific country? ").lower()=="yes":
        graph('covid.csv',input("Enter the name of the country: ").capitalize())
    else:
        graph('covid.csv')


def getFile():
    import requests
    url = 'https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv'
    myfile = requests.get(url, allow_redirects=True)
    open('covid.csv', 'wb').write(myfile.content)


def sortDB(filename, country=None):
    import pandas as pd

    dataBase = pd.read_csv(filename)
    group = dataBase.groupby('Country/Region')
    byCountries = pd.concat([i[1].sum() for i in group], axis=1).T
    byCountries.pop('Province/State')
    byCountries.pop('Lat')
    byCountries.pop('Long')
    if country == None:
        byCountries.pop('Country/Region')
        return byCountries.sum(axis=0).to_frame().T
    else:
        byCountry = dataBase[dataBase['Country/Region'].eq(country)]
        byCountry.pop('Province/State')
        byCountry.pop('Lat')
        byCountry.pop('Long')
        group = byCountry.groupby('Country/Region')
        byCountry = pd.concat([i[1].sum() for i in group], axis=1).T
        byCountry.pop('Country/Region')
        return byCountry


def graph(filename, country=None):
    import matplotlib.pyplot as plt
    data = sortDB(filename, country)
    print(data)
    y = data.to_numpy().tolist()
    x = list(data)
    y = [element for sublist in y for element in sublist]
    y.pop(0)
    y = [int(element) for element in y]
    x.pop(0)
    x = [str(element) for element in x]
    plt.plot(x, y)
    plt.xlabel('Dates')
    plt.ylabel('Cases', rotation='vertical')
    plt.xticks(x, x, rotation='vertical')
    title = country if country != None else 'total'
    plt.title('Covid cases {0}'.format(title))
    plt.show()


main()
