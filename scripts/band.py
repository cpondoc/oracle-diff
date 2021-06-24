import requests


def main():
   symbols = ['BTC']
   payload = {'symbols': list(symbols), 'ask_count': 16, 'min_count': 10}
   r = requests.get('https://api-gm-lb.bandchain.org/oracle/v1/request_prices', params=payload)
   print(r.url)
   print(r.json())


if __name__ == "__main__":
    main()