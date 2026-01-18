from datetime import timedelta, datetime


def parse_duration(duration_str):

    duration_str = duration_str.replace("P", "").replace("T", "")

    #now what remains is this value " 1D2H0M45S"

    components = ["D", "H", "M", "S"]
    values = {"D": 0, "H": 0, "M": 0, "S": 0}

    for component in components:
        if component in duration_str:
            value, duration_str = duration_str.split(component)
            values[component] = int(value)

    total_duration = timedelta(
        days=values["D"], hours=values["H"], minutes=values["M"], seconds=values["S"]
    )

    return total_duration


def transform_data(row):  #row represent on row in the staging columun

    duration_td = parse_duration(row["Duration"]) #we use the def created before

    row["Duration"] = (datetime.min + duration_td).time()  #datetime.min is the eraliest possible daytime, 
                                                           # which if I iterate it down will be this value : 00:00:00

    row["Video_Type"] = "Shorts" if duration_td.total_seconds() <= 60 else "Normal"

    return row