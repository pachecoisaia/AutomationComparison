import csv
import pandas as pd


def createDisconnectedOutputFile(file_name2):
    df = pd.read_csv(file_name2)

    df.drop(columns=['CallCompletedTimeStamp','ExactBillingDurationInSeconds',
                     'RoundedBillingDurationInMinutes']
            , axis=1, inplace=True)

    for index,row in df.iterrows():
        if row[1] == "No_Answer":
            df = df.drop([index], axis=0)
        elif row[1] == "Answering_Machine":
            df = df.drop([index], axis=0)
        elif row[1] == "Disconnected5408":
            df = df.drop([index], axis=0)
        else:
            None
    df.drop(columns=['Response'], axis=1, inplace=True)
    df.drop_duplicates(keep= 'first', ignore_index=True, inplace = True)

    df.to_csv("DISCONNECTED_PHONE_NUMBERS.csv", index = False)

def csv_toDictionary(file_name):
    #create empty dictionary for storing
    dictA = {}

    with open(file_name) as inputfile:
        reader = csv.reader(inputfile)
        #skip Header
        next(reader)
        for row in reader:
            #Assign the phoneNumber to the key and HouseHoldID as value pair (phoneNumber:HouseHoldID)
            dictA[row[1]] = row[0]

    return dictA

def createSuccessfulVoicemailFile(file_name2, dictA, filename):
    if filename.endswith(".csv"):
        None
    else:
        filename = filename + ".csv"

    #delete unnecessary columns
    df = pd.read_csv(file_name2)
    df.drop(
        columns = ['ExactBillingDurationInSeconds','RoundedBillingDurationInMinutes'], axis=1, inplace=True)

    #delete rows with NaN
    df = df.dropna()

    #delete No_Answer records and Diconnected Records
    for index,row in df.iterrows():
        if row[2] == "No_Answer":
            df = df.drop([index], axis=0)
        elif row[2] == "Disconnected5404":
            df = df.drop([index], axis=0)
        elif row[2] == "Disconnected5408":
            df = df.drop([index], axis=0)
        else:
            None

    df.drop(
        columns = ['Response'], axis=1, inplace=True)

    #Reformat timeStamp column
    df['CallCompletedTimeStamp'] = pd.to_datetime(df['CallCompletedTimeStamp'])

    #Sort by Most Recent Timestamp
    df = df.sort_values(by='CallCompletedTimeStamp' , axis = 0, ascending= False, ignore_index= True)

    #keep most recent timeStamp ,delete the non recent timestamps
    df = df.drop_duplicates(subset = ['PhoneNumberDialed'], keep='first')

    #find timestamp for phonenumbers with prefix
    for index, row in df.iterrows():
        #check if the number is in the list
        phonenumber = str(row[1])[1:]
        dialedList = df['PhoneNumberDialed'].tolist()
        dialedMap = map(str, dialedList)
        if phonenumber in dialedMap:
            #find index of matching phonenumber
            for i, r in df.iterrows():
                if str(r[1]) == phonenumber:
                    #update master record with max timestamp
                    df.iloc[i,0] = max(df.iloc[i,0],df.iloc[index,0])
                    #drop nonmaster record
                    df = df.drop(index, axis=0)

    #delete records that have the same number with 1 in front
    #for index, row in df.iterrows():
    #    #check if the number is in the list
    #    phonenumber = str(row[1])[1:]
    #    dialedList = df['PhoneNumberDialed'].tolist()
    #    dialedMap = map(str, dialedList)
    #    if phonenumber in dialedMap:
    #        df = df.drop(index, axis=0)

    #get the corresponding householdID from dictionary
    householdID = []
    for index, row in df.iterrows():
        keyexist = dictA.get(str(row[1]), False)
        if keyexist:
            #add to householdID list
            householdID.append(dictA.get(str(row[1])))
        else:
            #else not a key
            None

    #append householdID list to csv
    df.insert(0, 'HouseholdID', householdID)

    #delete PhoneNumberDialed and Response columns
    df = df.drop(['PhoneNumberDialed'], axis = 1)

    #convert into a csv
    df.to_csv(filename, index=False)