import random
from Strategy import StrategyBase

class UserStrategy(StrategyBase):
    
    def make_bid(self, current_value, previous_winners, previous_second_highest_bids, capital, num_bidders):
        # Step 1: If it's the first round, bid conservatively to preserve capital
        if not previous_winners:
            return min(current_value * 0.75, capital, 100)  # Bid 75% of your value in the first round
        
        # Step 2: Calculate average of previous highest bids and second-highest bids
        avg_previous_winner_bid = sum(previous_winners) / len(previous_winners)
        avg_previous_second_bid = sum(previous_second_highest_bids) / len(previous_second_highest_bids)
        
        # Step 3: Set a base bid close to the second-highest bid from previous rounds
        base_bid = avg_previous_second_bid + random.uniform(1, 3)  # Add a small buffer to win
        
        # Step 4: Adjust bid dynamically based on your current value and capital
        # Scale the bid up if your value is higher than average, or capital is much larger
        if current_value > avg_previous_winner_bid:
            bid = min(current_value * 0.9, capital, 100)  # Bid 90% of your value if it's high
        else:
            bid = min(base_bid, current_value * 0.85, capital, 100)  # Bid conservatively
        
        # Step 5: Prevent overbidding by limiting bids to capital and the value
        return min(bid, capital, 100)
