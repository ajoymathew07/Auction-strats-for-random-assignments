'''
Code to simulate the auction.
Successively loads all user-submitted files as modules, and calls the make_bid method.
'''

import importlib
import os
from Strategy import StrategyBase,StrategyHelper
from random import randint
from matplotlib import pyplot as plt
import numpy as np
import csv

class Auction:

    def __init__(self, strategy_folder, round_count, starting_capital,max_value,second_highest_fraction,type='self',log=False):
        # type can either be 'self': you get your own value, or 'max': you get max of all values
        self.__strategy_folder = strategy_folder # path where all strategy submissions are located
        self.round_count = round_count # number of rounds
        self.__round_number = 0
        self.starting_capital = starting_capital
        self.max_value = max_value
        self.type=type
        self.__dead_strategies = 0
        self.log=log
        self.second_highest_fraction = second_highest_fraction
        self.__load_strategies(self.starting_capital,self.max_value)
        self.capitals = [starting_capital for strategy in self.__strategies]
        self.simulate()
    

    def __load_strategies(self,starting_capital,max_value):
        self.__strategies = []
        for file in os.listdir(self.__strategy_folder):
            if file.endswith('.py'):
                module_name = file[:-3]  # removes '.py' extension
                module = importlib.import_module(f"{self.__strategy_folder}.{module_name}")
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, StrategyBase) and obj is not StrategyBase:
                        self.__strategies.append(StrategyHelper(module_name,obj(),starting_capital,max_value,second_highest_fraction=self.second_highest_fraction,log=self.log))
    

    def __pick_from_distribution(self):
        # Picks a random number from distribution of our choice
        return randint(0,100)
    
    def __get_values(self):
        self.values = [self.__pick_from_distribution() for i in range(len(self.__strategies)) if self.__strategies[i].capital>0]
        return self.values
    
    def __get_bids(self):
        return [strategy.bid(value,len(self.__strategies)-self.__dead_strategies) for strategy,value in zip([strategy for strategy in self.__strategies if strategy.capital>0],self.values) if strategy.capital>0]
    
    def find_two_highest(self,nums):

        first, second = float('-inf'), float('-inf')

        for num in nums:
            if num > first:
                first, second = num, first
            elif num > second and num != first:
                second = num

        return first, second

    def run_auction(self):
        # Simulates 1 round of the auction
        self.__round_number += 1
        values = self.__get_values()
        bids = self.__get_bids()
        winning_bid,second_highest = self.find_two_highest(bids)
        if self.log: print(f"Top 2 bids are {winning_bid:0.2f},{second_highest:0.2f}")
        max_value = max(values)
        if winning_bid<0:
            print("SOMETHING WENT WRONG. ALl bots either made illegal bids, or are out of capital.")
            print("Bids from active bots: ",bids)
            print("Values obatined by active bots: ",values)
            print("Capitals remaining ", [strategy.capital for strategy in self.__strategies])
            return
        for strategy in self.__strategies:
            winning_value = max_value if self.type=='max' else strategy.value
            if self.compare(strategy.bid_value,winning_bid):
                self.__dead_strategies += strategy.update_capital(winning_value,winning_bid,second_highest,winner=True)
            elif self.compare(strategy.bid_value,second_highest):
                self.__dead_strategies += strategy.update_capital(winning_value,winning_bid,second_highest,winner=False,second=True)
            else:
                self.__dead_strategies += strategy.update_capital(winning_value,winning_bid,second_highest)
        if len(self.__strategies)-self.__dead_strategies <=1: return -1
        else: return 0

    def compare(self,value1, value2, epsilon=0.001):
        return abs(value1-value2)<epsilon

    def simulate(self):
        while self.__round_number < self.round_count:
            status = self.run_auction()
            if status<0: break

    def get_stats(self,name):
        for strategy in self.__strategies:
            if strategy.name == name:
                portfolio,bids,values,_,_ =  strategy.get_stats()
                return portfolio,bids,values

    def get_pnl(self,portfolio):
        return portfolio[-1]-portfolio[0]        

    def gain_analysis(self,portfolio):
        gains = []
        losses = []
        for i in range(len(portfolio)-1):
            change = portfolio[i+1]-portfolio[i]
            if change>0:
                gains.append(change)
            elif change<0:
                losses.append(change)
        return gains,losses
            
    def calculate_max_drawdown(self,portfolio):
        values = np.array(portfolio)
        peak = np.maximum.accumulate(values)
        drawdown = (values - peak) / peak
        max_drawdown = drawdown.min()
        return abs(max_drawdown) * 100
    
    def portfotlio_analysis(self,portfolio):
        portfolio = np.array(portfolio)/self.starting_capital # normalise portfolio
        pnl = self.get_pnl(portfolio)
        drawdown = self.calculate_max_drawdown(portfolio)
        gains,losses = self.gain_analysis(portfolio)
        return pnl,drawdown,gains,losses
            
    def plot_stats(self,name,header,location):
        for strategy in self.__strategies:
            if strategy.name == name:
                portfolio,bids,values,winners,second =  strategy.get_stats()
                pnl,drawdown,gains,losses = self.portfotlio_analysis(portfolio)
                x = range(max([len(portfolio),len(bids),len(values),len(winners),len(second)]))
                bids = [max(bid,0) for bid in bids]
                portfolio = portfolio + [None]*(len(x)-len(portfolio))
                bids = bids + [None]*(len(x)-len(bids))
                values = values + [None]*(len(x)-len(values))
                winners = winners + [None]*(len(x)-len(winners))
                second = second + [None]*(len(x)-len(second))
                data = zip(portfolio,bids,values,winners,second)
                headers = ['Portfolio', 'Bids', 'Values', 'Winners', 'Seconds']
                # Write to CSV file
                with open(f'{location}/{name}.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(data)
                with open(f'{location}/{name}.txt','w') as file:
                    file.write(f"Profit: {pnl:0.2f}\n")
                    file.write(f"Max Drawdown: {drawdown:0.2f}\n")
                    if gains:
                        file.write(f"Highest Gain in a round: {max(gains):0.2f}\n")
                        file.write(f"Average Gain per round: {np.mean(gains):0.2f}\n")
                        file.write(f"Number of rounds with gains: {len(gains)}\n")
                    else:
                        file.write("No gains in any round")
                    if losses:
                        file.write(f"Highest Loss in a round: {min(losses):0.2f}\n")
                        file.write(f"Average Loss per round: {np.mean(losses):0.2f}\n")
                        file.write(f"Number of rounds with losses: {len(losses)}\n")
                    else:
                        file.write("No losses in a ny round")
                    
    
    def dump_stats(self,name,header,location):
        for strategy in self.__strategies:
            if strategy.name == name:
                portfolio,bids,values,winners,second =  strategy.get_stats()
                pnl,drawdown,gains,losses = self.portfotlio_analysis(portfolio)

                csv_path = f"{location}/{name}.csv"
                field_names = ["Name","Round Count","Starting Capital","PnL","Gain Variance","Gain Count","Loss Variance","Loss Count"]
                data = {
                    "Name":name,
                    "Round Count":self.round_count,
                    "Starting Capital":self.starting_capital,
                    "PnL": pnl,
                    "Gain Variance":np.var(gains),
                    "Gain Count":len(gains),
                    "Loss Variance":np.var(losses),
                    "Loss Count":len(losses)
                }
                file_exists = os.path.exists(csv_path)
                with open(csv_path, mode="a", newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=field_names)
                    if not file_exists:
                        writer.writeheader()

                    writer.writerow(data)

    def dump_all_stats(self,location):
        for strategy in self.__strategies:
            self.dump_stats(strategy.name,"",location)

    def plot_all_stats(self,location):
        for strategy in self.__strategies:
            self.plot_stats(strategy.name,"",location)                
