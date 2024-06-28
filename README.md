# dependencies-in-prefect


## Sending data from one task to the other
![alt text](images/image.png)
Relevant docs found [here](https://docs.prefect.io/latest/guides/specifying-upstream-dependencies/#determination-methods).

[passing_data_simple.py](example_scripts/passing_data_simple.py)
```python
@flow
def my_flow():
    x = task_1.submit()
    y = task_2.submit(x)
    z = task_3.submit(x)
    return y, z
```


## Dependencies without sharing data between tasks

![alt text](images/image-1.png)

You can use [wait_for](https://docs.prefect.io/latest/guides/specifying-upstream-dependencies/?h=wait_for#manual) syntax.

[wait_for_simple.py](example_scripts/wait_for_simple.py)
```python
@flow
def my_flow():
    a = task_1.submit()
    b = task_2.submit(wait_for=[a])
```


## Group tasks using subflows
Relevant docs found [here](https://docs.prefect.io/latest/concepts/flows/?h=subflows#composing-flows).

[subflows.py](example_scripts/subflows.py)

```python
@task
def task_a():
    return 1


@task
def task_b(x):
    return x + 2


@flow(name="Subflow")
def my_subflow(msg):
    print(f"Subflow says: {msg}")
    x = task_a.submit()
    y = task_b.submit(x)


@flow(name="Hello Flow")
def hello_world(name="world"):
    message = print_hello.submit(name)
    my_subflow(message)
```


## Dynamic tasks

[dynamic_tasks.py](example_scripts/dynamic_tasks.py)
```python
from prefect import flow, task


@task
def task1(num):
    print(f"Task {num}")


@flow
def flow_of_sequential_tasks():
    nums = [1, 2, 3]

    fut = None
    for num in nums:
        fut = task1.submit(num, wait_for=[fut] if fut is not None else [])
```

OR if there's a preexisting task's future you're waiting for, you don't need to account for the None case

```python
@flow
def flow_of_sequential_tasks():
    fut = task1.submit()
    nums = [1, 2, 3]
    for num in nums:
        fut = task1.submit(num, wait_for=[fut])
```

## Setting Result Persistence Location

If you are looking to rerun an already run flow instance with the same state as before, skipping the successful tasks and retrying the not run tasks in the flow. 

Hitting the retry button from the flow run page of a deployed flow run achieves this given **result persistence** is configured: 

We recommend setting result persistence to S3 (or Azure/GCP) like so:

```python
@flow(result_storage=S3Bucket.load(“my-bucket-block”)
def my_flow():
    pass

```
^In case you are wondering, a Prefect [block](https://docs.prefect.io/latest/concepts/blocks/#overview) is a way to save configuration for use in many flows. You can create and save blocks in the UI.

Alternatively you can set this for all flows with the following setting:

`PREFECT_DEFAULT_RESULT_STORAGE_BLOCK`

## Daemonize your Prefect Worker with [Systemd](https://systemd.io/)

A guide for starting a worker through systemd is found [here](https://discourse.prefect.io/t/how-to-run-a-prefect-2-worker-as-a-systemd-service-on-linux/1450).

I recommend following this [docker work pool tutorial](https://docs.prefect.io/latest/tutorial/workers/) first and starting the worker on your laptop, then once you've verified that works, start a worker in a linux VM using the Systemd guide linked above.