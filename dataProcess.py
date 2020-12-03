import pandas as pd
from collections import defaultdict

def ID_ASIN_HANDLE(line):
    tokens = line.split(":")
    tokens[1] = tokens[1].strip()
    tokens[1] = tokens[1].strip('\n')
    ID_ASIN[tokens[0]].append(tokens[1])
    if (tokens[0] == 'ASIN'):
        ASIN = tokens[1]
        return ASIN

def ASIN_TITLE_GROUP_SALESRANK_HANDLE(line):
    if (curASIN not in ASIN_TITLE_GROUP_SALESRANK["ASIN"]):
        ASIN_TITLE_GROUP_SALESRANK["ASIN"].append(curASIN)
    tokens2 = line.split(':', 1)
    tokens2[0] = tokens2[0].strip()
    tokens2[1] = tokens2[1].strip()
    tokens2[1] = tokens2[1].strip('\n')
    ASIN_TITLE_GROUP_SALESRANK[tokens2[0]].append(tokens2[1])

def ASIN_SIMILAR_HANDLE(line):
    if (curASIN not in ASIN_SIMILAR["ASIN"]):
        ASIN_SIMILAR["ASIN"].append(curASIN)
    tokens3 = line.split()
    ASIN_SIMILAR["COUNT"].append(tokens3[1])
    similarCount = int(tokens3[1])
    if (similarCount == 0):
        ASIN_SIMILAR["ID"].append([])
    else:
        temp = ",".join(tokens3[2:similarCount+2])
        ASIN_SIMILAR["ID"].append(temp)

def ASIN_CATEGORIES_HANDLE(line):
    if (curASIN not in ASIN_CATEGORIES["ASIN"]):
       ASIN_CATEGORIES["ASIN"].append(curASIN)
    tokens4 = line.split()
    categoriesCount = int(tokens4[1])
    ASIN_CATEGORIES["CATEGORIESCOUNT"].append(tokens4[1])
    return categoriesCount

def ASIN_REVIEWS_HANDLE(line):
    if (curASIN not in ASIN_REVIEWS["ASIN"]):
        ASIN_REVIEWS["ASIN"].append(curASIN)
    line = (line.strip('\n')).strip(' ')
    tokens5 = line.split()
    ASIN_REVIEWS["total"].append(tokens5[2])
    ASIN_REVIEWS["downloaded"].append(tokens5[4])
    ASIN_REVIEWS["avg rating"].append(tokens5[-1])
    reviewsCount = int(tokens5[2])
    return reviewsCount

def ASIN_REVIEWS_DETAIL_HANDLE(line):
    ASIN_REVIEWS_DETAIL["ASIN"].append(curASIN)
    if (reviewsCount == 0):
        ASIN_REVIEWS_DETAIL["date"].append("")
        ASIN_REVIEWS_DETAIL["customer"].append("")
        ASIN_REVIEWS_DETAIL["ratings"].append("")
        ASIN_REVIEWS_DETAIL["votes"].append("")
        ASIN_REVIEWS_DETAIL["helpful"].append("")
    else:
        line = (line.strip('\n')).strip(' ')
        tokens6 = line.split()
        ASIN_REVIEWS_DETAIL["date"].append(tokens6[0])
        ASIN_REVIEWS_DETAIL["customer"].append(tokens6[2])
        ASIN_REVIEWS_DETAIL["ratings"].append(tokens6[4])
        ASIN_REVIEWS_DETAIL["votes"].append(tokens6[6])
        ASIN_REVIEWS_DETAIL["helpful"].append(tokens6[-1])

def ASIN_CATEGORIES_DETAILS_HANDLE(line):
    ASIN_CATEGORIES_DETAILS["ASIN"].append(curASIN)
    if(categoriesCount == 0):
        ASIN_CATEGORIES_DETAILS["CATEGORIES"].append([])
    else:
        line = (line.strip('\n')).strip(' ')
        tokens7 = line.split('|')
        tokensLen = len(tokens7)-1
        temp = ", ".join(tokens7[1:tokensLen+1])
        ASIN_CATEGORIES_DETAILS["CATEGORIES"].append(temp)

def tableHash(tableID):
    global ID_ASIN, ASIN_TITLE_GROUP_SALESRANK, ASIN_REVIEWS, ASIN_REVIEWS_DETAIL, ASIN_CATEGORIES, ASIN_CATEGORIES_DETAILS, ASIN_SIMILAR
    global TOTAL_ID_ASIN, TOTAL_ASIN_TITLE_GROUP_SALESRANK, TOTAL_ASIN_REVIEWS, TOTAL_ASIN_REVIEWS_DETAIL, TOTAL_ASIN_CATEGORIES, TOTAL_ASIN_CATEGORIES_DETAILS, TOTAL_ASIN_SIMILAR
    if tableID % 1000 == 0 and tableID!=0:
        # hash all min tables into total table
        indexID = tableID/1000
        TOTAL_ID_ASIN[indexID]=ID_ASIN
        TOTAL_ASIN_TITLE_GROUP_SALESRANK[indexID]=ASIN_TITLE_GROUP_SALESRANK
        TOTAL_ASIN_REVIEWS[indexID]=ASIN_REVIEWS
        TOTAL_ASIN_REVIEWS_DETAIL[indexID]=ASIN_REVIEWS_DETAIL
        TOTAL_ASIN_CATEGORIES[indexID]=ASIN_CATEGORIES
        TOTAL_ASIN_CATEGORIES_DETAILS[indexID]=ASIN_CATEGORIES_DETAILS
        TOTAL_ASIN_SIMILAR[indexID]=ASIN_SIMILAR
        # empty tables
        ID_ASIN = {"Id": [], "ASIN": []}
        ASIN_TITLE_GROUP_SALESRANK = {"ASIN": [], "title": [], "group": [], "salesrank": []}
        ASIN_REVIEWS = {"ASIN": [], "total": [], "downloaded": [], "avg rating": []}
        ASIN_REVIEWS_DETAIL = {"ASIN": [], "date": [], "customer": [], "ratings": [], "votes": [], "helpful": []}
        ASIN_CATEGORIES = {"ASIN": [], "CATEGORIESCOUNT": []}
        ASIN_CATEGORIES_DETAILS = {"ASIN": [], "CATEGORIES": []}
        ASIN_SIMILAR = {"ASIN": [], "COUNT": [], "ID": []}

if __name__ == '__main__':
    ID_ASIN = {"Id": [], "ASIN": []}
    ASIN_TITLE_GROUP_SALESRANK = {"ASIN": [], "title": [], "group": [], "salesrank": []}
    ASIN_REVIEWS = {"ASIN": [], "total": [], "downloaded": [], "avg rating": []}
    ASIN_REVIEWS_DETAIL = {"ASIN": [], "date": [], "customer": [], "ratings": [], "votes": [], "helpful": []}
    ASIN_CATEGORIES = {"ASIN": [], "CATEGORIESCOUNT": []}
    ASIN_CATEGORIES_DETAILS = {"ASIN": [], "CATEGORIES": []}
    ASIN_SIMILAR = {"ASIN": [], "COUNT": [], "ID": []}
    ASIN_CUSTOMERID_TITLE = {"ASIN":[], "CUSTOMERID":[], "TITLE":[]}
    
    TOTAL_ID_ASIN = {}
    TOTAL_ASIN_TITLE_GROUP_SALESRANK = {}
    TOTAL_ASIN_REVIEWS = {}
    TOTAL_ASIN_REVIEWS_DETAIL = {}
    TOTAL_ASIN_CATEGORIES = {}
    TOTAL_ASIN_CATEGORIES_DETAILS = {}
    TOTAL_ASIN_SIMILAR = {}

    FINAL_ID_ASIN = {"Id": [], "ASIN": []}
    FINAL_ASIN_TITLE_GROUP_SALESRANK = {"ASIN": [], "title": [], "group": [], "salesrank": []}
    FINAL_ASIN_REVIEWS = {"ASIN": [], "total": [], "downloaded": [], "avg rating": []}
    FINAL_ASIN_REVIEWS_DETAIL = {"ASIN": [], "date": [], "customer": [], "ratings": [], "votes": [], "helpful": []}
    FINAL_ASIN_CATEGORIES = {"ASIN": [], "CATEGORIESCOUNT": []}
    FINAL_ASIN_CATEGORIES_DETAILS = {"ASIN": [], "CATEGORIES": []}
    FINAL_ASIN_SIMILAR = {"ASIN": [], "COUNT": [], "ID": []}



    curASIN = 0
    tableID = 0
    ID=1
    reviewsCount = 0
    categoriesCount = 0
    similarCount = 0
    lineBreak = []
    unformatData = open("amazon-meta.txt", 'r', encoding="utf8")
    if (unformatData):
        print("READ FILE SUCCEED!")
        # skip first 3 lines
        next(unformatData)
        next(unformatData)
        next(unformatData)
        # #read the data
        for line in unformatData:
            if line != "  discontinued product\n" and line != 'Id:   0\n' and line != "ASIN: 0771044445\n":
                lineBreak = line.split()
                if(line =='\n'):
                    tableHash(tableID)
                    tableID += 1
                elif (lineBreak[0] == 'Id:' or lineBreak[0] == "ASIN:"):
                  # read the ID and ASIN into one dict
                    print(ID)
                    ID+=1
                    curASIN = ID_ASIN_HANDLE(line)
                elif (lineBreak[0] == "title:" or lineBreak[0] == "group:" or lineBreak[0] == "salesrank:"):
                    # handle title, group, and salesrank part
                    ASIN_TITLE_GROUP_SALESRANK_HANDLE(line)
                elif (lineBreak[0] == "similar:"):
                    # handle similar part
                    ASIN_SIMILAR_HANDLE(line)
                elif (lineBreak[0] == "categories:"):
                    # handle categories part
                    categoriesCount = ASIN_CATEGORIES_HANDLE(line)
                elif (lineBreak[0] == "reviews:"):
                    # handle reviews part
                    reviewsCount = ASIN_REVIEWS_HANDLE(line)
                else:
                    if(line.find('|') != -1):
                        #handle categories detail
                        ASIN_CATEGORIES_DETAILS_HANDLE(line)
                    else:
                        #handle review detail
                        ASIN_REVIEWS_DETAIL_HANDLE(line)
        # hash total tables into one gnereal tables
        for curTableID,value in TOTAL_ID_ASIN.items():
            for curKey, curVal in value.items():
                for d in curVal:
                    FINAL_ID_ASIN[curKey].append(d)
            # hash reviews table
            for curKey, curVal in TOTAL_ASIN_REVIEWS[curTableID].items():
                for d in curVal:
                    FINAL_ASIN_REVIEWS[curKey].append(d)
            # hash reviews detail table
            for curKey, curVal in TOTAL_ASIN_REVIEWS_DETAIL[curTableID].items():
                for d in curVal:
                    FINAL_ASIN_REVIEWS_DETAIL[curKey].append(d)
            # hash categories details table
            for curKey, curVal in TOTAL_ASIN_CATEGORIES_DETAILS[curTableID].items():
                for d in curVal:
                    FINAL_ASIN_CATEGORIES_DETAILS[curKey].append(d)
            for curKey, curVal in TOTAL_ASIN_CATEGORIES[curTableID].items():
                for d in curVal:
                    FINAL_ASIN_CATEGORIES[curKey].append(d)
            for curKey, curVal in TOTAL_ASIN_SIMILAR[curTableID].items():
                for d in curVal:
                    FINAL_ASIN_SIMILAR[curKey].append(d)
            for curKey, curVal in TOTAL_ASIN_TITLE_GROUP_SALESRANK[curTableID].items():
                for d in curVal:
                    FINAL_ASIN_TITLE_GROUP_SALESRANK[curKey].append(d)
        
        # hash the last part of data to final tables
        for curTableID,value in ID_ASIN.items():
            for d in value:
                FINAL_ID_ASIN[curTableID].append(d)
        # hash reviews table
        for curKey, curVal in ASIN_REVIEWS.items():
            for d in curVal:
                FINAL_ASIN_REVIEWS[curKey].append(d)
        # hash reviews detail table
        for curKey, curVal in ASIN_REVIEWS_DETAIL.items():
            for d in curVal:
                FINAL_ASIN_REVIEWS_DETAIL[curKey].append(d)
        # hash categories details table
        for curKey, curVal in ASIN_CATEGORIES_DETAILS.items():
            for d in curVal:
                FINAL_ASIN_CATEGORIES_DETAILS[curKey].append(d)
        for curKey, curVal in ASIN_CATEGORIES.items():
            for d in curVal:
                FINAL_ASIN_CATEGORIES[curKey].append(d)
        for curKey, curVal in ASIN_SIMILAR.items():
            for d in curVal:
                FINAL_ASIN_SIMILAR[curKey].append(d)
        for curKey, curVal in ASIN_TITLE_GROUP_SALESRANK.items():
            for d in curVal:
                FINAL_ASIN_TITLE_GROUP_SALESRANK[curKey].append(d)

        #convert dictionary to dataframe
        ID_ASIN = pd.DataFrame(FINAL_ID_ASIN)
        ASIN_TITLE_GROUP_SALESRANK = pd.DataFrame(FINAL_ASIN_TITLE_GROUP_SALESRANK)
        ASIN_SIMILAR = pd.DataFrame(FINAL_ASIN_SIMILAR)
        ASIN_REVIEWS = pd.DataFrame(FINAL_ASIN_REVIEWS)
        ASIN_CATEGORIES = pd.DataFrame(FINAL_ASIN_CATEGORIES)
        ASIN_REVIEWS_DETAIL = pd.DataFrame(FINAL_ASIN_REVIEWS_DETAIL)
        #drop dup customers for one item
        ASIN_REVIEWS_DETAIL = ASIN_REVIEWS_DETAIL.drop_duplicates(subset=["ASIN", "customer"])

        ASIN_CATEGORIES_DETAILS = pd.DataFrame(FINAL_ASIN_CATEGORIES_DETAILS)
        #added id-title, id-customerID-rating
        ID_TITLE = pd.merge(ASIN_TITLE_GROUP_SALESRANK, ID_ASIN, on = 'ASIN')
        ID_TITLE = ID_TITLE[["Id", "title"]]
        ID_CUSTOMERID_RATING = pd.merge(ASIN_REVIEWS_DETAIL, ID_ASIN, on = 'ASIN')
        ID_CUSTOMERID_RATING = ID_CUSTOMERID_RATING[["customer", "Id", "ratings", "ASIN"]]
        USERID_CUSTOMER = pd.DataFrame(ASIN_REVIEWS_DETAIL)
        #do for user ID which start at 1 2 3 ...
        USERID_CUSTOMER = USERID_CUSTOMER[["customer"]]
        UD_CUSTOMER = USERID_CUSTOMER.drop_duplicates()
        FINAL_UD = pd.DataFrame(UD_CUSTOMER)
        # print("row count: ", FINAL_UD.shape[0])
        # print("row count1: ", len(FINAL_UD.index))
        ll = []
        for x in range(1555170):
            ll.append(x)
        FINAL_UD["userID"] = ll[0:1555170]
        ID_USERID_RATING = pd.merge(FINAL_UD, ID_CUSTOMERID_RATING, on = 'customer')
        ID_USERID_RATING = ID_USERID_RATING[["userID", "Id", "ratings"]]



        ID_ASIN.to_csv("FINAL-ID-ASIN.csv")
        ASIN_TITLE_GROUP_SALESRANK.to_csv("FINAL-ASIN-TITLE-GROUP-SALESRANK.csv")
        ASIN_SIMILAR.to_csv("FINAL-ASIN-SIMILAR.csv")
        ASIN_REVIEWS.to_csv("FINAL-ASIN-REVIEWS.csv")
        ASIN_CATEGORIES.to_csv("ASIN-CATEGORIES.csv")
        ASIN_CATEGORIES_DETAILS.to_csv("FINAL-ASIN-CATEGORIES-DETAILS.csv")
        ASIN_REVIEWS_DETAIL.to_csv("FINAL-ASIN-REVIEWS-DETAIL.csv")
        ID_TITLE.to_csv("ID_TITLE.csv")
        ID_CUSTOMERID_RATING.to_csv("ID_CUSTOMERID_RATING.csv")
        FINAL_UD.to_csv("USERID_CUSTOMER.csv")
        ID_USERID_RATING.to_csv("ID_USERID_RATING.csv")