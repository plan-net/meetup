from core4.api.v1.request.main import CoreRequestHandler
from core4.api.v1.application import CoreApiContainer

from meetup.job import MyJob
import pandas as pd
import numpy as np
import datetime


class MyHandler(CoreRequestHandler):

    """Demo request handler serving MVG data, soon."""

    author = "mra"
    title = "MVG demo handler"

    def get(self):
        data = MyJob().cookie.get("departures")
        df = pd.DataFrame(
            data, columns=[
                "station",
                "product",
                "label",
                "color",
                "destination",
                "departure",
                "distance",
                "name"
            ]
        )
        df["walk"] = df.apply(
            lambda r: (
                    r["departure"]
                    - datetime.timedelta(
                minutes=np.ceil(r["distance"] / 1000. / 3.5 * 60.))
            ),
            axis=1
        )
        df.sort_values("walk", inplace=True)
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        df = df[df.walk >= now]
        g = df.groupby([
            "station", "product", "label", "destination"]).first()
        df = pd.DataFrame(g)
        df.reset_index(inplace=True)
        df.sort_values("walk", inplace=True)
        if self.wants_html():
            self.render("template/mvg.html", data=df.to_dict("rec"))
        else:
            self.reply(df)


class MyContainer(CoreApiContainer):

    rules = [
        ("/mvg", MyHandler)
    ]


if __name__ == '__main__':
    from core4.api.v1.tool.functool import serve
    serve(MyContainer)

