from pathlib import Path
from datetime import datetime
from flightdata import Flight
import numpy as np
import pandas as pd

class Binfile:
    def __init__(self, path: Path):
        self.path = path
        info = self.path.stat()
        self.size = info.st_size
        self.created = datetime.fromtimestamp(info.st_ctime)

    @property
    def is_flightline(self):
        return self.size < 5e6

    def get_flight(self):
        return Flight.from_log(str(self.path))
        
    def to_dict(self):
        return dict(path=str(self.path), size=self.size, created=self.created)



if __name__ == "__main__":
    default="/media/tom/LOGS/APM/LOGS"

    all_logs = [Binfile(path) for path in Path(default).glob("*.BIN")]

    fl_records = [log for log in all_logs if log.is_flightline]
    flights = [log for log in all_logs if not log.is_flightline]

    print(len(flights), len(fl_records))
    data = []
    for fl in fl_records:
        flight = fl.get_flight()
        data.append(flight.describe())


    df1 = pd.concat(data)
    df2 = pd.DataFrame([fl.to_dict() for fl in fl_records])
    df = pd.concat([df1.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)


    import plotly.express as px
    fig = px.scatter_geo(
        df, 
        lat=df.last_gps__latitude,
        lon=df.last_gps__longitude,
        hover_name="path", 
    )
    fig.show()
    pass

