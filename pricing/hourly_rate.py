import math
from pricing.base_pricing import PricingStrategy

class HourlyRate(PricingStrategy):
    def calculate_fee(self, hours):
        return math.ceil(hours) * 10

    def get_type(self):
        return "Hourly Rate (R10/hour)"