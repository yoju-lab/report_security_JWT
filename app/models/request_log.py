class RequestLog:
    def __init__(self, request, response, duration, user):
        self.request = request
        self.response = response
        self.duration = duration
        self.user = user

    async def insert(self):
        # Implement the logic to save log to MongoDB
        pass
