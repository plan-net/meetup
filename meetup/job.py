import datetime
import requests

from core4.queue.job import CoreJob

DEP_URL = "https://www.mvg.de/fahrinfo/api/departure/{id}?footway=0"


class MyJob(CoreJob):
    author = "mra"
    schedule = "*/15 * * * *"
    attempts = 5
    error_time = 60
    
    def execute(self):
        data = {tuple(i) for i in self.cookie.get("departures", set())}
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        data = {d for d in data if d[5] >= now}

        for station in self.config.meetup.mvg.station:
            (station_id, distance, *name) = station.split()
            name = " ".join(name)
            self.logger.info("get data of [%s: %s]", station_id, name)
            update = self.get_data(station_id, distance, name)
            data = data.union(update)

        self.cookie.set("departures", list(data))

    def get_data(self, station_id, distance, name):
        url = DEP_URL.format(id=station_id)
        resp = requests.get(url, headers={
            'X-MVG-Authorization-Key': self.config.meetup.mvg.key})

        self.logger.debug("response:\n%s", resp.content)
        if resp.status_code != 200:
            raise RuntimeError("MVG API returned [%s]", resp.status_code)

        data = set()
        for r in resp.json()["departures"]:
            data.add((
                station_id,
                r["product"],
                r["label"],
                r["lineBackgroundColor"],
                r["destination"],
                datetime.datetime.fromtimestamp(
                    r["departureTime"] / 1000).replace(second=0),
                int(distance),
                name
            ))

        return data


if __name__ == '__main__':
    from core4.queue.helper.functool import execute

    execute(MyJob)

