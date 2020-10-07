import requests
from mohawk import Sender

sender = Sender(
    {
        'id': 'some-sender',
        'key': 'a long, ddddcomplicated secret',
        'algorithm': 'sha256',
    },
    "http://localhost:8000/data-lake/forecast/",
    "GET",
    content="",
    content_type="text/plain;"
)

response = requests.get(
    "http://localhost:8000/data-lake/forecast/",
    headers={
        'Authorization': sender.request_header,
        'Content-Type': "text/plain;"
    }
)

print(response)
print(response.text)
