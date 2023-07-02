class Response:
    def __init__(self, *args, **kwargs):
        self.data = kwargs
        
    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__.lower(),
            **self.data
        }

    def __str__(self):
        return f"{self.__class__.__name__}({str(self.data)[0:20]}...)"