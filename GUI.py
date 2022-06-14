import requests, json
import time


def make_json(url):

    # make GET request to json file
    text = requests.get(url).json()
    with open('json.json', 'w') as file:
        # write data to json file
        file.write(json.dumps(text, indent=4))

    return text     # json data


def make_currency(date: str = time.strftime("%d-%m-%Y", time.localtime())):
    # dict to write json file
    currency = {}

    # get only currency from json data => '(CURRENCY: len(3))': (value: int)
    try:
        for i in make_json(f'https://api.minfin.com.ua/currency/rates/nbu?locale=ru&date={date}')['data']:
            currency[i['code']] = i['rate']
    except Exception as e:
        print(e)
    # add UAH
    currency['UAH'] = 1

    # add crypto
    for k, v in get_crypto_currency().items():
        currency[k] = v

    # make date of json file
    currency['date'] = date

    # last update
    currency['update'] = time.strftime('%H:%M:%S')

    with open('currency.json', 'w') as file:
        file.write(json.dumps(currency, indent=4))


def dependence(c1, c2, value=1, date: str = time.strftime("%d-%m-%Y", time.localtime())):
    file = open('currency.json')
    currency = json.load(file)
    file.close()

    if date != currency['date']:
        make_currency(date)

    file = open('currency.json')
    currency = json.load(file)
    file.close()
    try:
        result = currency[c1.upper()] / currency[c2.upper()] * value
        return round(result, 4)
    except KeyError:
        print('Invalid input data')
        return 0


def get_currency(cur: str = 'usd'.upper(), date: str = time.strftime("%d-%m-%Y", time.localtime())):
    file = open('currency.json')
    currency = json.load(file)
    file.close()

    if date != currency['date']:
        make_currency(date)

    file = open('currency.json')
    currency = json.load(file)
    file.close()

    try:
        result = currency[cur.upper()]
        return round(result, 4)
    except KeyError:
        print('Invalid input data')
        return 0


def get_crypto():
    url = 'https://www.coinbase.com/api/v2/assets/search?base=UAH&country=UA&filter=all&include_prices=true&limit=30&order=asc&page=1&query=&resolution=day&sort=rank'
    text = requests.get(url).json()
    with open('crypto.json', 'w') as file:
        file.write(json.dumps(text, indent=4))


def get_crypto_currency():
    get_crypto()
    crypto = {}
    file = json.load(open('crypto.json'))

    crypto['BTC'] = float(file['data'][0]['latest'])
    crypto['ETH'] = float(file['data'][1]['latest'])

    return crypto


def main():
    print(get_currency('eur'))


if __name__ == '__main__':
    main()
