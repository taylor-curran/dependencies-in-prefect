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


# --------------------------------------------------------------------------------

## OR if there's a preexisting task's future you're waiting for, you don't need to account for the None case

from prefect import flow, task


@task
def task1(num):
    print(f"Task {num}")


@flow
def flow_of_sequential_tasks():
    fut = task1.submit()
    nums = [1, 2, 3]
    for num in nums:
        fut = task1.submit(num, wait_for=[fut])


if __name__ == "__main__":
    flow_of_sequential_tasks()
