import zmq
from Quote import Quote


class QuoteArchiveAPI:
    """
    Acts as an endpoint for the QuoteArchive microservice
    """

    def __init__(self, host="localhost", port="5558") -> None:
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{host}:{port}")
        print("QuoteArchive API initialized at port {}".format(port))

    def get_random(self) -> Quote:
        request_json = {
            "type": "random",
            "payload": ""
        }
        self.socket.send_json(request_json)
        reply = self.socket.recv_json()
        if reply['status'] == 'error':
            raise Exception(reply['payload'])
        quote = Quote()
        quote.body = reply['payload']['body']
        quote.author = reply['payload']['author']
        return quote

    def archive_quote(self, quote:Quote) -> bool:
        request_json = {
            "type": "archive",
            "payload": {
                "body": quote.body,
                "author": quote.author
            }
        }
        self.socket.send_json(request_json)
        reply = self.socket.recv_json()
        if reply['status'] == 'error':
            return False
        return True


if __name__ == "__main__":
    my_quote = Quote("This is a test quote", "Archive McArchiverson")
    q = QuoteArchiveAPI()
    print("Archived quote successfully" if q.archive_quote(my_quote) else "Failed archive")
    print(q.get_random())