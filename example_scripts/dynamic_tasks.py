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


if __name__ == "__main__":
    flow_of_sequential_tasks()
