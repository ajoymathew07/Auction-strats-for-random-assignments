from Strategy import StrategyBase
import numpy as np

class UserStrategy(StrategyBase):

    def __init__(self):
        self.rounds_played = 0
        self.previous_bid = 0  # To store the previous round's bid
        self.counter=0
        self.behaviour_list=[]  # To store bids below the expected value
        self.initial_capital=0
        self.backup=False

    def expected_value(self, num_bidders):
        '''Calculate expected max value X for the given number of bidders'''
        return 100 * num_bidders / (num_bidders + 1)
    
    def initial_val(self, num_bidders):
        '''Calculate initial bid estimate based on expected max value'''
        return self.expected_value(num_bidders) * (num_bidders - 1) / num_bidders
    
    def most_frequent_bid(self):
        '''Find the most frequent winning bid from self.winners_list'''
        if len(self.behaviour_list) > 0:
            # Get the unique values and their counts
            unique_bids, counts = np.unique(self.behaviour_list, return_counts=True)
            # Find the most frequent bid
            max_count_index = np.argmax(counts)
            most_frequent_bid = unique_bids[max_count_index]
            return most_frequent_bid, counts[max_count_index]
        return None, 0
    
    def make_bid(self, current_value, previous_winners, previous_second_highest_bids, capital, num_bidders):
        '''
        Function to make a bid based on the current value, previous winners, and available capital.
        '''
        self.rounds_played += 1
        exp = self.expected_value(num_bidders)


        if (self.rounds_played>500 and capital<self.initial_capital) or self.backup==True:
            self.backup=True
            if current_value>exp:
                bid=min(exp*0.98,capital*0.75)
                return bid
            else:
                if self.behaviour_list:
                    avg_behaviour=np.mean(self.behaviour_list)
                    bid=min(avg_behaviour+1,exp*0.95,capital*0.75)
                else:
                    bid=min(exp*0.95,capital*0.75)
                return bid

        # If it's the first round, initialize bid values
        most_frequent_bid, freq_count = self.most_frequent_bid()

            
        if freq_count > 30 and exp-most_frequent_bid<0.5:
                self.counter+=1
                if(self.counter<10):
                    # If the most frequent bid occurs more than 40 times, bid slightly higher
                    bid = min(most_frequent_bid + 0.01, capital)
                    return bid
                else:
                     self.counter=0
                     self.behaviour_list.clear()
        elif freq_count > 30 and exp-most_frequent_bid<1:
                self.counter+=1
                if(self.counter<15):
                    # If the most frequent bid occurs more than 40 times, bid slightly higher
                    bid = min(most_frequent_bid + 0.05, capital)
                    return bid
                else:
                     self.counter=0
                     self.behaviour_list.clear()
        elif freq_count > 35 and exp-most_frequent_bid<2:
                self.counter+=1
                if(self.counter<20):
                    # If the most frequent bid occurs more than 40 times, bid slightly higher
                    bid = min(most_frequent_bid + 0.1, capital)
                    return bid
                else:
                     self.counter=0
                     self.behaviour_list.clear()
        elif freq_count > 40 and exp-most_frequent_bid<4:
                self.counter+=1
                if(self.counter<25):
                    # If the most frequent bid occurs more than 40 times, bid slightly higher
                    bid = min(most_frequent_bid + 0.5, capital)
                    return bid
                else:
                     self.counter=0
                     self.behaviour_list.clear()
        elif freq_count > 40 and exp-most_frequent_bid<7:
                self.counter+=1
                if(self.counter<30):
                    # If the most frequent bid occurs more than 40 times, bid slightly higher
                    bid = min(most_frequent_bid + 1, capital)
                    return bid
                else:
                     self.counter=0
                     self.behaviour_list.clear()
          
                     
        if self.rounds_played == 1:
            bid = self.initial_val(num_bidders)
            self.inital_capital=capital
           
            for i in range(len(previous_winners)):
                if previous_winners[i] > exp and previous_second_highest_bids[i] > exp:
                    continue
                elif previous_winners[i] > exp and previous_second_highest_bids[i] < exp and previous_second_highest_bids[i] > bid:
                    bid = min(bid + 1, exp)
                    self.behaviour_list.append((np.floor(previous_second_highest_bids[i]*10)/10))
                elif previous_winners[i] > exp and previous_second_highest_bids[i] == bid:
                    bid -= 1
                elif previous_winners[i] <= exp and previous_winners[i] > bid:
                    bid = min(bid + 1, exp)
                    self.behaviour_list.append((np.floor(previous_winners[i]*10)/10))
                elif previous_winners[i] == bid:
                    bid -= 1
        else:
           
            bid = self.previous_bid  # Use the previous bid as a starting point for the next one
            
            # Update the bid based on the previous winners and second-highest bids
            i=-1
            if self.rounds_played<=300:
                if previous_winners[i] > exp and previous_second_highest_bids[i] < exp and previous_second_highest_bids[i] > bid:
                        bid = min(bid + 1, exp-0.5)
                        self.behaviour_list.append((np.floor(previous_second_highest_bids[i]*10)/10))
                elif previous_winners[i] > exp and previous_second_highest_bids[i] == bid:
                        bid -= 1
                elif previous_winners[i] <= exp and previous_winners[i] > bid:
                        bid = min(bid + 1, exp-0.5)
                        self.behaviour_list.append((np.floor(previous_second_highest_bids[i]*10)/10))
                elif previous_winners[i] == bid:
                        bid -= 1
            else:
                if previous_winners[i] > exp and previous_second_highest_bids[i] < exp and previous_second_highest_bids[i] > bid:
                        bid = min(bid + 0.5, exp-0.75)
                        self.behaviour_list.append((np.floor(previous_second_highest_bids[i]*10)/10))
                elif previous_winners[i] > exp and previous_second_highest_bids[i] == bid:
                        bid -= 1
                elif previous_winners[i] <= exp and previous_winners[i] > bid:
                        bid = min(bid + 0.5, exp-0.75)
                        self.behaviour_list.append((np.floor(previous_second_highest_bids[i]*10)/10))
                elif previous_winners[i] == bid:
                        bid -= 1
                 

        # If there are previous bids, use their data to adjust strategy
        
        # Adjust bid based on current value and previous round averages
        
        # Ensure bid is within allowed range
        bid = max(1, min(bid,exp,capital*0.5))

        # Update instance variables for future rounds
        self.previous_bid = bid
       

        return bid
