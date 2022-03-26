# Asynchronous Request-Reply Pattern

### Flask based application to demonstrate Asynchronous Request-Reply pattern mentioned in Microsoft Docs.

[Click here](https://docs.microsoft.com/en-us/azure/architecture/patterns/async-request-reply) to read more about this
pattern.

#### Description - <br>

- The client application makes a synchronous call to the API, triggering a long-running operation on the backend.
- The API responds synchronously as quickly as possible. It returns an HTTP 202 (Accepted) status code, acknowledging
  that the request has been received for processing.
- The response holds a location reference pointing to an endpoint that the client can poll to check for the result of
  the long-running operation.
- The API offloads processing to another component, such as a message queue.
- While the work is still pending, the status endpoint returns HTTP 202. Once the work is complete, the status endpoint
  can either return a resource that indicates completion, or redirect to another resource URL. For example, if the
  asynchronous operation creates a new resource, the status endpoint would redirect to the URL for that resource.
  <br><br>
  Here, we have two flask application - <br>
    1. Consumer ([flask_consumer](https://github.com/Evergreenies/asynchronous-request-reply/tree/main/flask_consumer))
    2. Producer ([flask_producer](https://github.com/Evergreenies/asynchronous-request-reply/tree/main/flask_producer))

#### [HTTP Pooling](https://docs.microsoft.com/en-us/azure/architecture/patterns/async-request-reply#solution) <br>

![Asynchronous Request-Reply](async-request.png)

1. The client sends a request and receives an HTTP 202 (Accepted) response.
2. The client sends an HTTP GET request to the status endpoint. The work is still pending, so this call also returns
   HTTP 202.
3. At some point, the work is complete, and the status endpoint returns 302 (Found) redirecting to the resource.
4. The client fetches the resource at the specified URL.

### Run Application - <br>

1. Install requirements in virtual environment -

```shell
$ python3.8 -m virtualenv venv
(venv) $ python3.8 -m pip install -r requirements.txt
```

2. Run both programs on separate terminals by command -

```shell
(venv) $ python3.8 app.py
```

3. Make HTTP request by cURL:

```shell
curl --location --request POST 'http://127.0.0.1:8001/call-me' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "dummy user"
}'
```

#### Note:

1. Custom Python Logger. ([Here](https://github.com/Evergreenies/asynchronous-request-reply/tree/main/flask_producer/producer/custom_logger))
2. Periodic Executor using Python. ([Here](https://github.com/Evergreenies/asynchronous-request-reply/blob/main/flask_consumer/_periodic_caller.py))
3. Queue-Based Load Management using Python. ([Here](https://github.com/Evergreenies/asynchronous-request-reply/tree/main/flask_producer/producer/queuing_mgmt))
