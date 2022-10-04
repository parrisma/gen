class MessageOriginException(Exception):
    """
    There was a request to handle a message, where the message was not sent by teh caller process
    """
    pass
