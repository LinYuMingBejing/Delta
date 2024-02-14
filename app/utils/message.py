class QueueMessage:
    def __init__(self, instance, body, method, url):
        self.instance = instance
        self.body = body
        self.method = method
        self.url = url

    def to_dict(self):
        return {
            'instance': self.instance,
            'body': self.body,
            'method': self.method,
            'url': self.url
        }
    