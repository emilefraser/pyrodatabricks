# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Well known values for lotteries

# COMMAND ----------

import enum

# COMMAND ----------

# Define Lottery Countries
class Countries(enum.Enum):
   world_wide = 0
   south_africa = 1
   united_states = 2
   unknown = 99

print("Loaded enum: Countries")

# COMMAND ----------

# To define the Provider that host the Lotto Draws
class LotteryProvider:
    def __init__(self, provider_code, provider_name, country, provider_uri, data_retrieval_method):
        self.provider_code = provider_code
        self.provider_name = provider_name
        self.country = country
        self.provider_uri = provider_uri
        self.data_retrieval_method = data_retrieval_method

lottery_provider = {}
lottery_provider["south_africa|ithuba"] = LotteryProvider("south_africa|ithuba", "ithuba", Countries.south_africa.name, "https://www.nationallottery.co.za/index.php?task=results.redirectPageURL&amp;Itemid=265&amp;option=com_weaver&amp;controller=lotto-history", "scrape")

print("Loaded class: LotteryProvider")

# COMMAND ----------

# Define Lottery Types (list of class objects)
class Lottery_Type: 
    def __init__(self, lottery_type_name, count_win_balls, count_bonus_balls, count_power_balls, count_super_balls):
        self.lottery_type_name = lottery_type_name
        self.count_win_balls = count_win_balls
        self.count_bonus_balls = count_bonus_balls
        self.count_power_balls = count_power_balls
        self.count_super_balls = count_super_balls

lottery_types = {}
 
# Adding list as value
lottery_types["6"] = Lottery_Type("5", 5, 0, 0, 0)
lottery_types["5+1"] = Lottery_Type("5+1", 5, 0, 1, 0)
lottery_types["5+1+1"] = Lottery_Type("5+1+1", 5, 0, 1, 1)
lottery_types["6"] = Lottery_Type("6", 6, 0, 0, 0)
lottery_types["6&1"] = Lottery_Type("6&1", 6, 1, 0, 0)

print("Loaded class: Lottery_Type")

# COMMAND ----------

# Lottery Class 
# Draw Frequency should be listed in cron time
# This only defines the different lotto types and where their info can be found
class Lottery:
  def __init__(self, LotteryProvider, lottery_code, lottery_name, lottery_web_alias, lottery_type, count_total_win_balls, count_total_bonus_balls, count_total_power_balls, count_total_super_balls, draw_frequency, lottery_uri, is_active):
    self.LotteryProvider = LotteryProvider
    self.lottery_code = lottery_code
    self.lottery_name = lottery_name
    self.lottery_web_alias = lottery_web_alias
    self.lottery_type = lottery_type
    self.count_balls = count_total_win_balls
    self.count_total_bonus_balls = count_total_bonus_balls
    self.count_power_balls = count_total_power_balls
    self.count_super_balls = count_total_super_balls
    self.draw_frequency = draw_frequency
    self.lottery_uri = lottery_uri
    self.is_active = is_active

# Adds all the lotteries to a list
# Lottery URI can inherit from LotteryProvider
lotteries = {}
lotteries["south_africa|ithuba|LOTTO"] = Lottery(lottery_provider["south_africa|ithuba"], "south_africa|ithuba-LOTTO", "LOTTO", "LOTTO", lottery_types["6&1"], 52, 46, None, None, "xxx", None, True)
lotteries["south_africa|ithuba|LOTTOPLUS1"] = Lottery(lottery_provider["south_africa|ithuba"], "south_africa|ithuba|LOTTOPLUS1", "LOTTO PLUS 1", "LOTTOPLUS", lottery_types["6&1"], 52, 46, None, None, "xxx", None, True)
lotteries["south_africa|ithuba|LOTTOPLUS2"] = Lottery(lottery_provider["south_africa|ithuba"], "south_africa|ithuba|LOTTOPLUS2", "LOTTO PLUS 2", "LOTTOPLUS2", lottery_types["6&1"], 52, 46, None, None, "xxx", None, True)
lotteries["south_africa|ithuba|POWERBALL"] = Lottery(lottery_provider["south_africa|ithuba"], "south_africa|ithuba|POWERBALL", "POWERBALL", "POWERBALL", lottery_types["5+1"], 52, None, 20, None, "xxx", None, True)
lotteries["south_africa|ithuba|POWERBALLPLUS"] = Lottery(lottery_provider["south_africa|ithuba"], "south_africa-ithuba|POWERBALLPLUS", "POWERBALL PLUS", "POWERBALLPLUS", lottery_types["5+1"], 52, None, 20, None, "xxx", None, True)
# print(lotteries["south_africa-LOTTO"].lottery_name)
#[print(i.lottery_name) for i in lotteries]

print("Loaded class: Lottery")

# COMMAND ----------

class Draw:
    def __init__(self, Lottery, draw_id, draw_timestamp, draw_uri):
        self.Lottery = Lottery
        self.draw_id = draw_id
        self.draw_timestamp = draw_timestamp   
        self.draw_uri = draw_uri 

# COMMAND ----------

class DrawEvent:
    def __init__(self, Lottery, Draw, draw_event_id, is_results_published, results_uri):
        self.Lottery = Lottery
        self.Draw = Draw
        self.draw_event_id = draw_event_id
        self.is_results_published = is_results_published
        self.results_uri = results_uri

# COMMAND ----------

class PayoutDivision:
    def __init__(self, Lottery, division, count_win_balls, count_bonus_balls, count_power_balls, count_super_balls, payout_fixed, payout_variable):
        self.Lottery = Lottery
        self.division = division
        self.count_win_balls = count_win_balls
        self.count_bonus_balls = count_bonus_balls
        self.count_power_balls = count_power_balls
        self.count_super_balls = count_super_balls
        self.payout_fixed = payout_fixed
        self.payout_variable = payout_variable

payout_division = {}
#payout_division["south_africa|LOTTO|div1"] = PayoutDivision(lotteries["south_africa|LOTTO|div1"],1, 6, 0, 0, 0, None, None) 
#payout_division["south_africa|LOTTO|div2"] = PayoutDivision(lotteries["south_africa|LOTTO|div2"],2, 5, 1, 0, 0, None, None) ##
#p#ayout_division["south_africa|LOTTO|div3"] = PayoutDivision(lotteries["south_africa|LOTTO|div3"],3, 5, 0, 0, 0, None, None) 
#payout_division["south_africa|LOTTO|div4"] = PayoutDivision(lotteries["south_africa|LOTTO|div4"],4, 4, 1, 0, 0, None, None) 
#payout_division["south_africa|LOTTO|div5"] = PayoutDivision(lotteries["south_africa|LOTTO|div5"],5, 4, 0, 0, 0, None, None) 
#payout_division["south_africa|LOTTO|div6"] = PayoutDivision(lotteries["south_africa|LOTTO|div6"],6, 3, 1, 0, 0, None, None) 
#$#ayout_division["south_africa|LOTTO|div7"] = PayoutDivision(lotteries["south_africaLOTTO|div7"],7, 3, 0, 0, 0, None, None) 
#payout_division["south_africa|LOTTO|div8"] = PayoutDivision(lotteries["south_africa|LOTTO|div8"],8, 2, 1, 0, 0, None, None) 
#payout_division["south_africa|LOTTO|div9"] = PayoutDivision(lotteries["south_africa|LOTTO|div9"],9, 2, 0, 0, 0, None, None) 