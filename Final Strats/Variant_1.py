from Strategy import StrategyBase
import numpy as np

class UserStrategy(StrategyBase):

    def __init__(self):
        self.rounds_played = 0
    
    def make_bid(self, current_value, previous_winners, previous_second_highest_bids, capital, num_bidders):
        '''
        Make sure you also keep track of how much capital you have left.
        '''
        self.rounds_played += 1
        
        # If there are previous bids to refer to, calculate average winning bid and second-highest bid
        if previous_winners:
            avg_winning_bid = np.mean(previous_winners)
            avg_second_highest_bid = np.mean(previous_second_highest_bids)
        else:
            avg_winning_bid = 50  # Starting guess if no previous data
            avg_second_highest_bid = 45  # Starting guess for second-highest
        
        # Calculate a safe bid based on capital and previous round data
        if current_value > avg_winning_bid:
            bid = min(current_value - 5, avg_winning_bid + 1, capital)
        else:
            bid = min(current_value * 0.8, avg_second_highest_bid + 1, capital)
        
        # Ensure bid stays within the allowed range
        bid = max(0, min(bid, 100))
        
        return bid
