from prefect import flow, task


@task(name="Print Hello")
def print_hello(name):
    msg = f"Hello {name}!"
    print(msg)
    return msg


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


if __name__ == "__main__":
    hello_world("Marvin")
