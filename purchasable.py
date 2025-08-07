from pyrecord import Record
'''
Purchasable is an object in the game world that can be purchased.
'''
Purchasable = Record.create_type("Purchasable", "purchase_cost", "monthly_income", "sell_price")