import argparse
from holdings import read_holdings
from rates import ExchangeRate
from returns import compute_returns

from datetime import date

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Compute returns on investments at Erste.")

    # Add a required argument
    parser.add_argument('holdings', type=str, help='Holdings HTML file')

    # Add an optional argument with a default value
    parser.add_argument('--rates', type=str, default='EURHUF.html',
                        help='An optional argument for rates (default: EURHUF.html)')

    # Parse the arguments
    args = parser.parse_args()

    holdings = read_holdings(args.holdings)
    rates = ExchangeRate(args.rates)
    
    returns = compute_returns(holdings, rates)


if __name__ == '__main__':
    main()