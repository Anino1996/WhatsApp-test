import re


def ParseData(file):
    anino = list(file)
    anino_edited = [i.replace("\u200e","") for i in anino]
    Cleaned = []
    datetimeSplice = []
    Cleaned.append(anino_edited[0])

    StartPattern1 = "^\[([0][1-9]|[0-2][0-9]|[3][0-1])/([0][1-9]|[1][0-2])/[\d]{4}"
    StartPattern2 = '^([\d]{1}|[\d]{2})/([\d]{1}|[\d]{2})/[\d]{2}'

    if re.search(StartPattern1, Cleaned[0]):
        for i in anino_edited[1:]:
            if re.search(StartPattern1, i):
                Cleaned.append(i)
            else:
                Cleaned[-1] = "\n".join([Cleaned[-1], i])
        for i in Cleaned:
            datetimeSplice.append(i[1:].split("]", 1))

    else:
        for i in anino_edited[1:]:
            if re.search(StartPattern2, i):
                Cleaned.append(i)
            else:
                Cleaned[-1] = "\n".join([Cleaned[-1], i])
        for i in Cleaned:
            datetimeSplice.append(i.split(" - ", 1))

    return datetimeSplice

def DatatoDic(parsedData):
        Date, Time = parsedData[0].split(", ")
        try:
            Sender, Message = parsedData[1].split(": ", 1)
        except ValueError:
            Sender = ""
            Message = parsedData[1]
        return {"Date": Date, "Time": Time, "Sender": Sender.strip(), "Message": Message}

def Dataset(Dic):
    Data = [DatatoDic(i) for i in Dic]
    return Data

