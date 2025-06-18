from Strategy import StrategyBase

#Variant 1 Nash V(1-1/n)
class UserStrategy(StrategyBase):

    # Refer to Strategy.py for implementation details
    # Edit the function below without changing its template(name, input parameters, output type)
    def make_bid(self, current_value, previous_winners,previous_second_highest_bids,capital,num_bidders):
        '''
        Make sure you also keep track of how much capital you have left.
        Any strategy that makes a bid greater than available capital will be immediately discarded
        '''
        # Bid a constnant amount
        if previous_second_highest_bids:
            bid = max(previous_second_highest_bids) + 10
        else:
            bid = current_value + 10
        return min(bid, capital, 100)

        
    # Feel free to make use of class variables and helper functions while editing the above function
        