import math
from pricing.base_pricing import PricingStrategy

class CappedRate(PricingStrategy):
    def calculate_fee(self, hours):
        fee = math.ceil(hours) * 12
        return min(fee, 60)

    def get_type(self):
        return "Hourly Rate with Cap (R12/hour, max R60)"