from Auction import Auction
import time
import argparse

number_of_rounds = 1000
starting_capital = 500

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-log', action='store_true', help='Enable logging')
    args = parser.parse_args()
    log = True if args.log else False
    start = time.time()
    myAuction = Auction("Strategies",number_of_rounds,starting_capital,100,0,type='self',log=log)
    myAuction.simulate()
    myAuction.plot_stats("Test Strategy 1","","Plots")
    end = time.time()
    print(f"Execution time: {end-start:0.3f}")