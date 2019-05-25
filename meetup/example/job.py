import random
import re
from core4.queue.helper.functool import enqueue, find_job
from core4.queue.job import CoreJob
import time
from core4.queue.main import CoreQueue

JOBS = (
    "meetup.example.job.SwarmJobChild1",
    "meetup.example.job.SwarmJobChild2",
    "meetup.example.job.SwarmJobChild3",
    "meetup.example.job.SwarmJobChild4",
    "meetup.example.job.SwarmJobChild5"
)


class SwarmJob(CoreJob):
    author = "mra"
    defer_time = 15
    defer_max = 360
    error_time = 15
    attempts = 2

    def execute(self, child=None):
        count = find_job(name=re.compile("^meetup.example.job.Swarm"))
        if len(count) > 5:
            if random.random() > 0.95:
                self.defer()
            if random.random() > 0.95:
                raise RuntimeError()
            if len(count) > 200:
                return
        if child is not None:
            child = child.split(".")
        else:
            child = [0]
        child.append(0)
        first = True
        for i in range(5):
            if first or random.random() < 0.3:
                first = False
                tgt = JOBS[random.randint(0, len(JOBS) - 1)]
                child[-1] = i
                enqueue(tgt, child=".".join([str(i) for i in child]))
        time.sleep(3)


class SwarmJobChild1(SwarmJob):
    author = "mra"


class SwarmJobChild2(SwarmJob):
    author = "mra"


class SwarmJobChild3(SwarmJob):
    author = "mra"


class SwarmJobChild4(SwarmJob):
    author = "mra"


class SwarmJobChild5(SwarmJob):
    author = "mra"

    def execute(self, child=None):
        q = CoreQueue()
        for doc in find_job(name=re.compile("^meetup.example.job.SwarmJob")):
            if random.random() < 0.2:
                q.kill_job(doc["_id"])


class SwarmCleaner(SwarmJob):
    author = "mra"

    def execute(self):
        while True:
            q = CoreQueue()
            listing = find_job(
                name=re.compile("^meetup.example.job.SwarmJob"))
            if listing:
                for doc in listing:
                    q.kill_job(doc["_id"])
                    q.remove_job(doc["_id"])
            else:
                break
