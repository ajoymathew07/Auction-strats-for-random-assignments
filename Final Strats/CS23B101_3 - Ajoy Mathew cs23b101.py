from Strategy import StrategyBase
import numpy as np

class UserStrategy(StrategyBase):

    def __init__(self):
        self.rounds_played = 0
        self.previous_bid = 0  # To store the previous round's bid
        
        self.behavior_list = []  # To store bids below the expected value
        self.initial_capital=0
        self.counter=0
        self.conservative_earnings=0
        self.loss_counter=0
        self.aggression=1

        self.conservative=False

    
    def expected_value(self, num_bidders):
        '''Calculate expected max value X for the given number of bidders'''
        return 100 * num_bidders / (num_bidders + 1)
    
    def ideal_val(self, num_bidders,current_value):
        '''Calculate initial bid estimate based on expected max value'''
        return current_value * (num_bidders - 1) / num_bidders
    
    def make_bid(self, current_value, previous_winners, previous_second_highest_bids, capital, num_bidders):
        '''
        Function to make a bid based on the current value, previous winners, and available capital.
        '''
        self.rounds_played += 1
        exp=self.expected_value(num_bidders)

        if self.rounds_played==1:
            self.initial_capital=capital

        # If it's the first round, initialize bid values
        
        bid=self.ideal_val(num_bidders,current_value)

        if self.rounds_played<10:
             return bid
        if current_value>exp:
             bid=min(capital*0.5,exp-2)
             return bid
        if self.rounds_played%20==0:
             self.aggression*=0.9
        if self.rounds_played>=10 and self.conservative==False and capital>self.initial_capital*0.8:
            if self.previous_bid==previous_second_highest_bids[-1]:
                 self.loss_counter+=1
            if self.loss_counter==15:
                 self.conservative=True
  
            if previous_winners:
                  
                  if previous_winners:
                    avg_winning_bid=np.mean(previous_winners)
                    my_bid=avg_winning_bid+1.5*self.aggression
                    if my_bid>exp-2:
                        self.aggression*=0.9
                    self.previous_bid=my_bid
                    return min(my_bid,capital*0.5)
            else:
                  return bid  
        else:
             self.loss_counter=0
             self.conservative=True  
           
             
        if previous_winners and self.conservative==True:
                if self.counter<400:
                    avg_winning_bid=np.mean(previous_winners)
                    if avg_winning_bid<current_value:
                        bid=avg_winning_bid+1
                else:
                    self.counter=0
                   
                    self.conservative=False
                            
                            
                            
                           
       

        
                  

                
        # Adjust bid based on current value and previous round averages
        
        # Ensure bid is within allowed range
        bid = max(0, min(bid,capital*0.5))

        # Update instance variables for future rounds
    
       

        return bid