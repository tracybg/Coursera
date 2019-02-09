http://www.codeskulptor.org/#user45_Kr19O7dKfF_25.py

"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(10)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
        
    def __str__(self):
        """
        Return human readable state
        """                       
        message = []
        message.append("Current time is " + str(self.get_time()))
        message.append("Current number of cookies " + str(self.get_cookies()))
        message.append("Current cookies per second " + str(self.get_cps()))
        message.append("Total number of cookies produced " + str(self._total_cookies))
        message.append("")
        return '\n'.join(message)

    
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies

    
    def get_total_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._total_cookies        
    
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps

    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    
    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """        
        if cookies <= self.get_cookies():
            return 0.0
        
        else:
            time_in_sec = (cookies - self.get_cookies()) / float(self.get_cps())        
            return float(math.ceil(time_in_sec))

        
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            pass
        
        else:
            self._total_cookies += self.get_cps() * time
            self._current_cookies += self.get_cps() * time
            self._current_time += time      

            
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self.get_cookies():
            pass
        
        else:
            self._current_cookies -= float(cost)
            self._current_cps += additional_cps
            self._history.append((self.get_time(), item_name, cost, self.get_total_cookies()))

            
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    
    sim_build_info = build_info.clone()
    sim_game = ClickerState()
    current_time = 0
    wait_time = 0
    
    while current_time <= duration:
                                       
        # Initialize local variables
        current_cookies = sim_game.get_cookies()
        current_cps = sim_game.get_cps()
        current_time = sim_game.get_time()
        time_left = duration - current_time
                
        item = strategy(current_cookies, current_cps, sim_game.get_history(), time_left, sim_build_info)

        if item == None:
            sim_game.wait(time_left)
            break            
        
        else:
            item_cost = sim_build_info.get_cost(item)
            item_cps = sim_build_info.get_cps(item)                    

            
        # Check wait time until having enough cookies to buy item
        if current_cookies >= item_cost:
            wait_time = 0
            
        else:
            wait_time = sim_game.time_until(item_cost)
            if wait_time + current_time > duration:
                sim_game.wait(duration - current_time)
                break

            
        # Update state of simulation
 
        sim_game.wait(wait_time)
        sim_game.buy_item(item, item_cost, item_cps)
        sim_build_info.update_item(item)  
        
    return sim_game

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    
    max_balance = time_left * cps + cookies
    
    item_list = build_info.build_items()
    cheapest_item = None
    cheapest_item_cost = float('inf')
    
    for item in item_list:
        item_cost = build_info.get_cost(item)
        if item_cost < cheapest_item_cost and item_cost <= max_balance:
            cheapest_item = item
            cheapest_item_cost = build_info.get_cost(item)
        
    return cheapest_item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
                
    max_balance = time_left * cps + cookies

    item_list = build_info.build_items()
    bougiest_item = None
    bougiest_item_cost = float('-inf')
    
    for item in item_list:
        item_cost = float(build_info.get_cost(item))
        if item_cost > bougiest_item_cost and item_cost <= max_balance:
            bougiest_item = item
            bougiest_item_cost = float(build_info.get_cost(item))
                
    return bougiest_item


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    item_list = build_info.build_items()
    best_item = None
    best_item_effective_cps = float('-inf')
    
    for item in item_list:
        item_cost = build_info.get_cost(item)
        item_cps = build_info.get_cps(item)
        
        # Calculate more info on items
        time_to_afford = math.ceil(item_cost - cookies) / float(cps)
        
        if time_to_afford >= time_left:
            item_effective_time = 0
            
        else:
            item_effective_time = time_left - time_to_afford
            
        if time_left == 0:
            item_effective_cps = 0
            
        else:    
            item_effective_cps = (item_effective_time * item_cps) / item_cost

        # Create beter list
        if item_effective_cps > best_item_effective_cps:
            best_item = item
            best_item_effective_cps = item_effective_cps
                
    return best_item   


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

#    history = state.get_history()
#    history = [(item[0], item[3]) for item in history]
#    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
#    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
#    run_strategy("Cheap", SIM_TIME, strategy_cheap)
#    run_strategy("Expensive", SIM_TIME, strategy_expensive)
#    run_strategy("Best", SIM_TIME, strategy_best)
#    
#run()
    

