from Strategy import StrategyBase

class UserStrategy(StrategyBase):

    def make_bid(self, current_value, previous_winners, previous_second_highest_bids, capital, num_bidders):
        # Use the maximum of the previous winners' bids and second-highest bids to estimate the competition
        if previous_winners and previous_second_highest_bids:
            estimated_max_value = max(previous_winners)
            estimated_second_highest = max(previous_second_highest_bids)
        else:
            estimated_max_value = current_value  # If no data, assume your value is the max
            estimated_second_highest = current_value - 5  # Conservative estimate for second-highest

        # Try to avoid being the second-highest bidder
        if capital > estimated_max_value:
            bid = estimated_max_value - 1  # Bid just below the max value
        else:
            bid = estimated_second_highest + 1  # Try to outbid the second-highest to avoid penalty

        return min(bid, capital, 100)  # Ensure bid is within capital and bid limit
