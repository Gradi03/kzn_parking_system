from pricing.base_pricing import PricingStrategy

class FlatRate(PricingStrategy):
    def calculate_fee(self, hours):
        return 15

    def get_type(self):
        return "Flat Rate (R15)"