"""
Cookie Clicker Simulator
"""

# http://www.codeskulptor.org/#user47_FrObZTplag_28.py

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._cookies_produced = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._game_history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        message = []
        message.append("Current time is " + str(self.get_time()))
        message.append("Current number of cookies " + str(self.get_cookies()))
        message.append("Current cookies per second " + str(self.get_cps()))
        message.append("Total number of cookies produced " + str(self._cookies_produced))
        message.append("")
        return '\n'.join(message)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
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
        return list(self._game_history)

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
            self._cookies_produced += time * self._current_cps
            self._current_cookies += time * self._current_cps
            self._current_time += time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self.get_cookies():
            pass
        
        else:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._game_history.append((self.get_time(), item_name, cost, self._cookies_produced))
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    sim_game = ClickerState()
    sim_build = build_info.clone()

    
    while sim_game.get_time() <= duration:
        time_left = duration - sim_game.get_time()
        item = strategy(sim_game.get_cookies(), sim_game.get_cps(), sim_game.get_history(), time_left, sim_build)
        
        if item == None:
            sim_game.wait(time_left)
            break
            
        wait_time = sim_game.time_until(sim_build.get_cost(item))

            
        if wait_time <= time_left:
            sim_game.wait(wait_time)
            sim_game.buy_item(item, sim_build.get_cost(item), sim_build.get_cps(item))
            sim_build.update_item(item) 
            
        else:
            sim_game.wait(time_left)
            break
            
    print sim_build._info       
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
    cheapest_item = None
    cheapest_cost = float('inf')
    cookies_to_spend = cookies + cps * time_left
    
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost < cheapest_cost and item_cost <= cookies_to_spend:
            cheapest_item = item
            cheapest_cost = item_cost
            
    return cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    priciest_item = None
    priciest_cost = float('-inf')
    cookies_to_spend = cookies + cps * time_left
    
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost > priciest_cost and item_cost <= cookies_to_spend:
            priciest_item = item
            priciest_cost = item_cost

    return priciest_item

def strategy_best_1(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    
    Based off of the idea:
    Item that generates most cookies in the time left / highest ROI they're all the same
    """
    best_item = None
    best_item_benefit = 0
    cookies_to_spend = cookies + cps * time_left
    
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)   
        item_cps = build_info.get_cps(item)  
        time_to_afford = math.ceil(item_cost / cps)
        time_to_enjoy = time_left - time_to_afford
        benefit_from_item = time_to_enjoy * item_cps
        
        if benefit_from_item > best_item_benefit and item_cost <= cookies_to_spend:
            best_item = item   

    return best_item
        
def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    
    Get items with the lowest growth rates, which are also the cheapest at the time
    """
    
    cookies_to_spend = cookies + cps * time_left 
    
    origin_build_info = provided.BuildInfo()
    
    item_growth_dict = {}

    for item in build_info.build_items():
        item_growth_dict[item] = (build_info.get_cost(item) / origin_build_info._info[item][0])
    
#    print "Item growth dict"
#    print item_growth_dict
    
    growth_num_list = []
    
    for item in item_growth_dict:
        growth_num_list.append(item_growth_dict.get(item))
    min_growth = min(growth_num_list)
    
#    print "Growth num list"
#    print growth_num_list
#
#    print "Min growth"
#    print min_growth
    
    items_with_min_growth = []
    for item in build_info.build_items():
        if item_growth_dict[item] == min_growth:
            items_with_min_growth.append(item)
    
    cheapest_item = None
    cheapest_cost = float('inf')
    cookies_to_spend = cookies + cps * time_left
    
    for item in items_with_min_growth:
        item_cost = build_info.get_cost(item)
        if item_cost < cheapest_cost and item_cost <= cookies_to_spend:
            cheapest_item = item
            cheapest_cost = item_cost
            
    return cheapest_item    
      

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it
#
#    history = state.get_history()
#    history = [(item[0], item[3]) for item in history]
#    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)


def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
    
#run()
    

