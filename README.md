# FastAPI with Kafka Consumer

This project shows how to use a **Kafka Consumer** inside a Python Web API built using 
**FastAPI**. This can be very useful for use cases where one is building a Web API that 
needs to have some state, and that the state is updated by receiving a message from a 
message broker (in this case Kafka).

One example of this could be a ML Web API, that is serving requests for performing 
inferences according to the *current* model. Often, this model will be updated over time
as the model gets retrained according to a given schedule or after model/data drift job 
has been executed. Therefore, one solution could be to notify the Web API by sending a 
message with either the new model or some metadata that will enable the API to fetch the
new model.

## Technologies

The implementation was done in `python>=3.7` using the web framework `fastapi` and for 
interacting with **Kafka** the `aiokafka` library was chosen. The latter fits very well
within an `async` framework like `fastapi` is.

## How to Run

First, step will be to have **Kafka** broker and zookeeper running, by default it expects
the bootstrap server to be running on `localhost:9092`. This can be changed using the 
environment variable `KAFKA_BOOTSTRAP_SERVERS`. 

Next, the following environment variable `KAFKA_TOPIC` should be defined with desired 
name for this topic.

```bash
$ export KAFKA_TOPIC=<my_topic>
```

The topic can be created using the command line, or it can be automatically created by 
the consumer inside the Web API.

Start the Web API by running:

```bash
$ python main.py
``` 

Finally, send a message by running the `producer.py`:

```bash
$ python producer.py
```

<details>
    <summary>Result</summary>

    ```bash
    Sending message with value: {'message_id': '4142', 'text': 'some text', 'state': 96}
    ```

</details>


The producer sends a message with a field `state` that is used in this demonstration for
showing how the state of the Web API can be updated. One can confirm that the state of the
Web API is being updated by performing a `GET` request on the `/state` endpoint.

```bash
curl http://localhost:8000/state
```

<details>
    <summary>Result before sending message</summary>

    ```bash
    {"state":0}
    ```

</details>

<details>
    <summary>Result after sending message</summary>

    ```bash
    {"state":23}
    ```    
    The actual value will vary given it's a random number.
</details>


## Consumer Initialization

During the initialization process of the Consumer the log end offset is checked to determine whether we already have messages in the topic. If so, consumer will *seek* to this offset so that it can read the last message committed in this kafka topic.

 This is useful to guarantee that the consumer does not miss on previously published messages, either because they were published before the consumer was up, or because the Web API has been down for some time. For this use case, we consider that only the most recent `state` matters, and thereby, we only care about the last committed message.

Each instance of the Web API will have it's own consumer group (they share the same group name prefix + a random id), so that each instance of the API receives the same state updates.
  