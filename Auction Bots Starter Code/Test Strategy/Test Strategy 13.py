from Strategy import StrategyBase

class UserStrategy(StrategyBase):

    def __init__(self):
        # Initialize class variables
        self.my_previous_bids = []  # Store the bot's previous bids
        self.wins = 0  # Counter for the number of wins
        self.rounds = 0  # Total number of rounds played

    def make_bid(self, current_value, previous_winners, previous_second_highest_bids, capital, num_bidders):
        '''
        Make sure you also keep track of how much capital you have left.
        Any strategy that makes a bid greater than available capital will be immediately discarded.
        '''
        # Calculate Nash equilibrium bid based on the number of bidders
        optimal_bid = current_value * num_bidders/ (num_bidders+1)
        
        # If no previous winners exist (first round), use optimal bid
        if not previous_winners:
            bid = optimal_bid  # Bid based on Nash equilibrium in the first round
            self.my_previous_bids.append(bid)
            self.rounds += 1
            return min(bid, capital, 100)
        
        # Step 1: Compute the average of previous highest bids and second-highest bids
        avg_previous_winner_bid = sum(previous_winners) / len(previous_winners)
        avg_previous_second_bid = sum(previous_second_highest_bids) / len(previous_second_highest_bids)
        
        # Step 2: Adaptive decision-making based on history
        max_winner_bid = max(previous_winners)
        max_second_highest_bid = max(previous_second_highest_bids)

        # Use a mixture of Nash optimal and historical data to decide the bid
        if optimal_bid > max_winner_bid:
            bid = max(max_winner_bid + 1, optimal_bid)  # Bid slightly above the max previous winner
        else:
            bid = optimal_bid  # Otherwise, stick to Nash optimal bid
        
        # Ensure we don't bid more than available capital
        bid = min(bid, capital, 100)
        
        # Track this round's bid for future reference
        self.my_previous_bids.append(bid)
        self.rounds += 1
        
        
        return bid
