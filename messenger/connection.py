import pika

class Connection:

    #init method
    def __init__(self):
        self.connection_type = ''
        self.host = ''
        self.port = ''
        self.route = ''
        self.login = ''
        self.password = ''
        self.url = ''

    def start_connection(self):

        connection = 'Null'

        if self.connection_type == 'A':
            credentials = pika.PlainCredentials(self.login, self.password)
            connection = pika.BlockingConnection(
                         pika.ConnectionParameters(
                                    self.host,
                                    self.port,
                                    self.route,
                                    credentials))

        elif self.connection_type == 'B':
            params = pika.URLParameters(self.url)
            connection = pika.BlockingConnection(params)

        return connection
