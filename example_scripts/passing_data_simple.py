from prefect import flow, task


@task
def task_1():
    return 6


@task
def task_2(x):
    return x + 2


@task
def task_3(x):
    return x + 3


@flow
def my_flow():
    x = task_1.submit()
    y = task_2.submit(x)
    z = task_3.submit(x)
    return y, z


if __name__ == "__main__":
    my_flow()
