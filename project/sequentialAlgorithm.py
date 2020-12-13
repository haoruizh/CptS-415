# sequential algorithms
import pandas as pd
#import sqlalchemy as sql
import pandasql as psql
import csv
# problem 1
def sqAlg1(file, M, conditions, select):
    with open(file, mode = 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        df = pd.DataFrame(csv_reader)
        del df['']
        print(df.columns)
        # run sql on df
        query = "SELECT " + select + " FROM df"+" WHERE " + conditions
        # put the condition part 
        print(query)
        df = psql.sqldf(query)
        return df.head(M)
        
if __name__ == "__main__":
    sqAlg1('ID_CUSTOMERID_RATING.csv', 100, "ratings>=4", "Id")