import re

#################################################
#   Parses the data file and returns a list     # 
#   of dictionaries for each message            #
#################################################

def ParseData(file):
    anino = list(file)
    anino_edited = [i.replace("\u200e","") for i in anino]
    Cleaned = []
    datetimeSplice = []
    Cleaned.append(anino_edited[0])

    
    # Define RegEx patterns for iOS and android whatsapp backups
    StartPattern1 = "^\[([0][1-9]|[0-2][0-9]|[3][0-1])/([0][1-9]|[1][0-2])/[\d]{4}"
    StartPattern2 = '^([\d]{1}|[\d]{2})/([\d]{1}|[\d]{2})/[\d]{2}'

    
    # Test first for Android whatsapp backups
    # Iterate through split lines and append one line to the previous line if it doesn't start with the regex pattern.
    if re.search(StartPattern1, Cleaned[0]):
        for i in anino_edited[1:]:
            if re.search(StartPattern1, i):
                Cleaned.append(i)
            else:
                Cleaned[-1] = "\n".join([Cleaned[-1], i])
        for i in Cleaned:
            datetimeSplice.append(i[1:].split("]", 1))
    
    
    # iOS
    else:
        for i in anino_edited[1:]:
            if re.search(StartPattern2, i):
                Cleaned.append(i)
            else:
                Cleaned[-1] = "\n".join([Cleaned[-1], i])
        for i in Cleaned:
            datetimeSplice.append(i.split(" - ", 1))

    return datetimeSplice


# Extract the date, time, sender and Message from each full message set
def DatatoDic(parsedData):
        Date, Time = parsedData[0].split(", ")
        try:
            Sender, Message = parsedData[1].split(": ", 1)
        except ValueError:
            Sender = ""
            Message = parsedData[1]
        return {"Date": Date, "Time": Time, "Sender": Sender.strip(), "Message": Message}

 # Create a list of dicitonaries to be fed into pandas methods
def Dataset(Dic):
    Data = [DatatoDic(i) for i in Dic]
    return Data

