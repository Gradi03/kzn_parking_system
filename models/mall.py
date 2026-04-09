class Mall:
    def __init__(self, name, capacity, pricing_strategy):
        self.name = name
        self.capacity = capacity
        self.pricing_strategy = pricing_strategy
        self.current_vehicles = 0