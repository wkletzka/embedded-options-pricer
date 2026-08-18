import finnhub
import os
import yfinance as yf
import time
import serial

# Serial constants
SERIAL_PORT = "COM3" # Update to match your Elegoo UNO port
BAUD_RATE = 9600

def main():
    try:
        # Initialize Serial connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) # Give the Elegoo time to reset after opening serial

        # Repeatedly query user
        while True:
            # Grab API key from environment var
            api_key = os.getenv("FINNHUB_API_KEY")

            # Setup client
            finnhub_client = finnhub.Client(api_key=api_key)

            # Grab ticker from user
            ticker = input("Enter a stock ticker to initialize options pricer: ").strip().upper()

            # Pull stock price for ticker
            price = get_live_price(ticker)

            # Pull the IV of the nearest ATM call for a semi-accuate estimate
            iv = get_baseline_iv(ticker, price)

            print(f"Price: " + str(price)) # price from Finnhub, IV from yahoofinance (soonest ATM call)
            print(f"IV: " + str(iv))

            # Format data: "PRICE,VOLATILITY\n"; decimals specify how many places to use
            data_string = f"{price:.2f},{iv:.4f}\n"

            # Send data to Elegoo board via serial transmission
            ser.write(data_string.encode('utf-8'))
            
            print(f"Streamed to MCU -> Price: ${price:.2f} | IV: {iv:.1%}")
            print("You may now adjust Strike and DTE on the hardware.")

    except KeyboardInterrupt:
        print("\nClosing connection.")
        ser.close()

# Fetch Front-Month At-The-Money Implied Volatility for calls via yfinance
def get_baseline_iv(ticker, current_price):
    tk = yf.Ticker(ticker)
    expirations = tk.options
    
    if not expirations:
        print(f"No options data found for {ticker}. Defaulting to 30% IV.")
        return 0.30
        
    # Get the option chain for the closest expiration date
    chain = tk.option_chain(expirations[0])
    calls = chain.calls
    
    # Find the strike price closest to our current stock price (ATM) by subtracting curr price from all the strikes
    calls['diff'] = abs(calls['strike'] - current_price)

    # Find the row index with the smallest number (the minimum difference, i.e. closest to current)
    atm_call = calls.loc[calls['diff'].idxmin()] 
    
    # Return the Implied Volatility of that specific call option
    return atm_call['impliedVolatility']

# Fetch live stock price of inputted ticker via finhub api
def get_live_price(ticker):
    # Grab API key from environment var
    api_key = os.getenv("FINNHUB_API_KEY")

    # Setup client
    finnhub_client = finnhub.Client(api_key=api_key)

    q = finnhub_client.quote(ticker)

    return q['c']

if __name__ == "__main__":
    main()