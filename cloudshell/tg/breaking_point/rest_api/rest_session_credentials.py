class RestSessionCredentials(object):
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def __eq__(self, other):
        """
        :param other:
        :type other: RestSessionCredentials
        """
        return self.hostname == other.hostname and self.username == other.username and self.password == other.password
