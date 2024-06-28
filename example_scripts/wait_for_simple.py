from prefect import task, flow


@task
def task_1():
    return 1


@task
def task_2():
    return 2


@flow
def my_flow():
    a = task_1.submit()
    b = task_2.submit(wait_for=[a])


if __name__ == "__main__":
    my_flow()
