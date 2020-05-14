from mysimbdp import subscribe_stream
import json

 # A function to receive analytics results
def subscribe(topic_name):
    subscribe_stream(topic_name)
    pass

if __name__ == '__main__':
    topic_name = "results-A"
    stream = subscribe_stream(topic_name)
    print(stream)
    for msg in stream:
        print("Message")
        print(msg.value)
