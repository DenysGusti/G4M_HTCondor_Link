from time import perf_counter, sleep
from subprocess import run
from pathlib import Path


def calculateTime(func):
    def wrapper(*args, **kwargs):
        t: float = perf_counter()
        returned_value = func(*args, **kwargs)
        print(f'time spent in {func.__name__}: {perf_counter() - t}s')
        return returned_value

    return wrapper


def checkRunningJobs(user: str, update_s: int) -> None:
    while True:
        sleep(update_s)
        msg: str = run(['condor_q'], capture_output=True, text=True).stdout
        jobs_status: list[str] = [x for x in msg.split('\n') if f'Total for {user}' in x][0].split(', ')
        if int(jobs_status[2].split()[0]) > 0 or int(jobs_status[4].split()[0]) > 0:
            print('please check jobs! problems are possible!')
        if int(jobs_status[3].split()[0]) == 0:
            break


def checkCondorStatus() -> None:
    msg: str = run(['condor_status'], capture_output=True, text=True).stdout
    print(msg)

    if not msg:
        raise Exception('check condor status!')
