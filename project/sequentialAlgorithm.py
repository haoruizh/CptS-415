# sequential algorithms
import pandas as pd
import sqlalchemy as sql
import pandasql as psql
# problem 1
def sqAlg1(file, M, conditions, select):
    df = pd.read_csv(file, index_col=0)
    # run sql on df
    query = "SELECT " + select + " FROM df"+" WHERE " + conditions
    # put the condition part 
    print(query)
    df = psql.sqldf(query)
    return df.head(M)
        
if __name__ == "__main__":
    select1 = "Id"
    conditions1 = "Id < 10 and Id >= 2"
    print(sqAlg1('FINAL-ID-ASIN.csv', conditions1, select1, 2))