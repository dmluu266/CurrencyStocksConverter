import requests
import sys
# pip install pandas
import pandas as pd
# pip install yfinance
import yfinance as yf
# pip install plotly
import plotly.graph_objs as go

def main():
    # check for valid base currency
    base = base_currency()
    # declare new currency and its rate from old currency
    new_currency, rate = convert(base)
    #print(rate)
    # declare amount and its conversion to new currency
    amount, conversion = balance(rate)
    print(f"Amount in {new_currency}: ${conversion}")

    # dataframe of stock
    data = pd.DataFrame()
    while data.empty:
        tick = input("Stock: ")
        data = yf.download(tickers=tick, period='1d', interval='1m')


    # declare figure
    fig = go.Figure()

    # if to_currency == USD, dont change df plot values; title: "You can buy {conversion/stockprice} {stock}"
    if new_currency == "USD":
        amt = conversion / data['Close'][-1]
        print(f"You can buy {amt:.4f} {tick} at closing price")
        # Candlestick
        fig.add_trace(go.Candlestick(x=data.index,
                        open=(data['Open']),
                        high=(data['High']),
                        low=(data['Low']),
                        close=(data['Close']), name = 'market data'))

        # Add titles
        fig.update_layout(
            title=f'{tick} live share price evolution | You can buy {amt:.4f} {tick} at closing price',
            yaxis_title='Stock Price (USD per Shares)')

    # if base == USD, you can just use 'rate' to change plot values; title: "You can buy {amount/stockprice} {stock}"
    elif base == "USD":
        amt = float(amount) / data['Close'][-1]
        print(f"You can buy {amt:.4f} {tick} at closing price")

        # Candlestick
        fig.add_trace(go.Candlestick(x=data.index,
                        open=(data['Open']*rate),
                        high=(data['High']*rate),
                        low=(data['Low']*rate),
                        close=(data['Close']*rate), name = 'market data'))
        # Add titles
        fig.update_layout(
            title=f"{tick} live share price evolution | You can buy {amt:.4f} {tick} at closing price",
            yaxis_title=f"Stock Price ({new_currency} per Shares)")

    # if none === USD, adjust rate, adjust amount; title: "you can buy {conversion / stockprice * new_rate} {stock}"
    else:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        rate = response.json()["rates"][new_currency]
        amt = float(conversion) / (data['Close'][-1] * rate)
        print(f"You can buy {amt:.4f} {tick} at closing price")

        # Candlestick
        fig.add_trace(go.Candlestick(x=data.index,
                        open=(data['Open']*rate),
                        high=(data['High']*rate),
                        low=(data['Low']*rate),
                        close=(data['Close']*rate), name = 'market data'))
        # Add titles
        fig.update_layout(
            title=f"{tick} live share price evolution | You can buy {amt:.4f} {tick} at closing price",
            yaxis_title=f"Stock Price ({new_currency} per Shares)")


    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    # Show
    fig.show()

# check if base currency is valid
def base_currency():
    while True:
        b = input("From Currency: ")
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/" + b)
            if response.json()['result'] == 'error':
                print("Invalid currency")
                pass

        except ValueError:
            print("Invalid Currency(VE)")
            pass
        except KeyError:
            break
        except requests.RequestException:
            print("Request Exception")
            sys.exit(1)

    return b

# find conversion rate
def convert(b):
    response = requests.get("https://api.exchangerate-api.com/v4/latest/" + b)
    o = response.json()

    while True:
        to_currency = input("To Currency: ")
        # check if new currency is valid
        if to_currency in o['rates']:
            break
        else:
            pass

    return [to_currency, o['rates'][to_currency]]

# ask for balance and convert
def balance(rate):
    while True:
        try:
            bal = input("Enter Amount: ")
            if int(bal) > 0:
                break
        except (ValueError, TypeError):
            print("Invalid input")
            pass


    return [bal, round((float(bal) * rate), 2)]


if __name__ == "__main__":
    main()