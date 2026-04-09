class ParkingRecord:
    def __init__(self, username, mall, entry_time):
        self.username = username
        self.mall = mall
        self.entry_time = entry_time
        self.exit_time = None
        self.amount = 0