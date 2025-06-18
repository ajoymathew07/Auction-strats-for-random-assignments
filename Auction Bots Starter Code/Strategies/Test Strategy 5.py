from Strategy import StrategyBase

#Variant 2 Nash 100*n/(n+1)
class UserStrategy(StrategyBase):

    # Refer to Strategy.py for implementation details
    # Edit the function below without changing its template(name, input parameters, output type)
    def make_bid(self, current_value, previous_winners,previous_second_highest_bids,capital,num_bidders):
        '''
        Make sure you also keep track of how much capital you have left.
        Any strategy that makes a bid greater than available capital will be immediately discarded
        '''
        # Bid a constnant amount
        val = 100*num_bidders/(num_bidders+1)
        
        return min(current_value,val)
        
    # Feel free to make use of class variables and helper functions while editing the above function
        