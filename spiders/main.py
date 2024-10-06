# from spyderContent import start as contentStart
# from spyderComments import start as commentsStart
# import os
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://root:12345678@127.0.0.1/weiboarticles?charset=utf8mb4')

# def save_to_sql():
#     try:
#         articleOldPd = pd.read_sql('select * from article', engine)
#         articleNewPd = pd.read_csv('./articleData.csv')
#         concatPd = pd.concat([articleNewPd,articleOldPd],join='inner')
#         concatPd = concatPd.drop_duplicates(subset='id', keep='last')
#         concatPd.to_sql('article',con=engine, if_exists='replace',index=False)
#
#         commentOldPd = pd.read_sql('select * from comments', engine)
#         commentNewPd = pd.read_csv('./commentsData.csv')
#         concatCommentPd = pd.concat([commentNewPd, commentOldPd], join='inner')
#         concatCommentPd = concatCommentPd.drop_duplicates(subset='content', keep='last')
#         concatCommentPd.to_sql('comments',con=engine, if_exists='replace',index=False)
#     except  Exception as e:
#         print(f"An error occurred: {e}")
#         articleNewPd = pd.read_csv('./articleData.csv')
#         commentNewPd = pd.read_csv('./commentsData.csv')
#         articleNewPd.to_sql('article', con=engine, if_exists='replace',index=False)
#         commentNewPd.to_sql('comments', con=engine, if_exists='replace',index=False)
#
#     # os.remove('./articleData.csv')
#     # os.remove('./commentsData.csv')

def save_to_sql():
    try:
        articleOldPd = pd.read_sql('select * from article', engine)
    except Exception as e:
        print(f"Article table not found. Creating new table: {e}")
        articleNewPd = pd.read_csv('./articleData.csv')
        articleNewPd.to_sql('article', con=engine, if_exists='replace', index=False)
    else:
        articleNewPd = pd.read_csv('./articleData.csv')
        concatPd = pd.concat([articleNewPd, articleOldPd], join='inner')
        concatPd = concatPd.drop_duplicates(subset='id', keep='last')
        concatPd.to_sql('article', con=engine, if_exists='replace', index=False)

    try:
        commentOldPd = pd.read_sql('select * from comments', engine)
    except Exception as e:
        print(f"Comments table not found. Creating new table: {e}")
        commentNewPd = pd.read_csv('./commentsData.csv')
        commentNewPd.to_sql('comments', con=engine, if_exists='replace', index=False)
    else:
        commentNewPd = pd.read_csv('./commentsData.csv')
        concatCommentPd = pd.concat([commentNewPd, commentOldPd], join='inner')
        concatCommentPd = concatCommentPd.drop_duplicates(subset='content', keep='last')
        concatCommentPd.to_sql('comments', con=engine, if_exists='replace', index=False)

def main():
    # !!! Don't run these - will scrape data again !!!
    # print('Scraping article...')
    # contentStart(60,10) 60 types 10 pages
    # print('Scraping comments...')
    # commentsStart()
    # print('Finish scraping start saving...')
    save_to_sql()

if __name__ == '__main__':
    main()