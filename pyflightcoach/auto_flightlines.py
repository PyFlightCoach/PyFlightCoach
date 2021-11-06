from pathlib import Path
from datetime import datetime
from flightdata import Flight
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
from typing import List



class Binfile:
    def __init__(self, path: Path):
        self.path = path
        info = self.path.stat()
        self.size = info.st_size
        self.created = datetime.fromtimestamp(info.st_mtime)
        

    @property
    def is_flightline(self):
        return self.size < 5e6

    def get_flight(self, save_path):
        save_file = save_path / (self.path.stem + ".csv")
        if save_file.exists() and not save_path is None:
            flight=Flight.from_csv(save_file)
        else:
            flight = Flight.from_log(str(self.path))

            flight.to_csv(save_file)
        return flight
        
    def to_dict(self):
        return dict(path=str(self.path), size=self.size, created=self.created)


def describe_binfiles(binfiles: List[Binfile], save_path: Path=Path("/home/tom/Documents/AutoJudge/flight_data")):
    data = []
    for fl in tqdm(binfiles):
        flight = fl.get_flight(save_path)
        data.append(flight.describe())
    df1 = pd.concat(data)
    df2 = pd.DataFrame([fl.to_dict() for fl in binfiles])
    return pd.concat([df1.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)


if __name__ == "__main__":
    all_logs = [Binfile(path) for path in Path("/media/tom/LOGS/APM/LOGS").glob("*.BIN")]

    fl_records = [log for log in all_logs if log.is_flightline]
    flights = [log for log in all_logs if not log.is_flightline]

    flightline_info = describe_binfiles(fl_records)
    flight_info = describe_binfiles(flights)

    print("n total flights = {}, n flightline logs = {}".format(len(flights), len(fl_records)))

    df = pd.concat([flightline_info.assign(type="flightline"), flight_info.assign(type="flight")])

    import plotly.express as px
    fig = px.scatter_geo(
        df, 
        lat=df.last_gps__latitude,
        lon=df.last_gps__longitude,
        hover_name="path",
        color="type" 
    )
    fig.show()
    pass

