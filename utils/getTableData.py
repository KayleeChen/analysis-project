from utils.getPublicData import *
from datetime import datetime
from snownlp import SnowNLP
# def getTableDataPageData():
#     return getAllCiPingTotal()
#
# def getTableData(hotWord):
#     commentList = getAllCommentsData()
#     tableData =[]
#     for comment in commentList:
#         if comment[4].find(hotWord) != -1:
#             tableData.append(comment)
#     return tableData
#
# def getTableDataEchartsData(hotWord):
#     tableList = getTableData(hotWord)
#     xData = [x[1] for x in tableList]
#     xData = list(set(xData))
#     xData = list(sorted(xData,key=lambda x:datetime.strptime(x,'%Y-%m-%d').timestamp(),reverse=True))
#     yData = [0 for x in range(len(xData))]
#     for comment in tableList:
#         for index,x in enumerate(xData):
#             if comment[1] == x:
#                 yData[index] += 1
#     return xData,yData
#
# def getTableDataArticle(flag):
#     if flag:
#         tableListOld = getAllArticleData()
#         tableList = []
#         for item in tableListOld:
#             item = list(item)
#             emotionValue = SnowNLP(item[5]).sentiments
#             if emotionValue > 0.5:
#                 emotionValue = '正面'
#             elif emotionValue == 0.5:
#                 emotionValue = '中性'
#             elif emotionValue < 0.5:
#                 emotionValue = '负面'
#             item.append(emotionValue)
#             tableList.append(item)
#     else:
#         tableList = getAllArticleData()
#     return tableList

def getTableDataPageData():
    # Get all comments data for table display
    return getAllCiPingTotal()

def getTableData(hotWord):
    # Get all comments data
    commentList = getAllCommentsData()
    # Filter comments that contain the hot word
    return [comment for comment in commentList if hotWord in comment[4]]

def getTableDataEchartsData(hotWord):
    # Get filtered comments based on hot word
    tableList = getTableData(hotWord)
    # Extract unique dates and sort them
    xData = sorted({comment[1] for comment in tableList}, key=lambda x: datetime.strptime(x, '%Y-%m-%d').timestamp(), reverse=True)
    # Count comments per date
    yData = [sum(comment[1] == x for comment in tableList) for x in xData]
    return xData, yData

def getTableDataArticle(flag):
    # Get all article data
    tableList = getAllArticleData()
    if flag:
        # If flag is true, perform sentiment analysis and add sentiment labels
        tableList = [
            list(item) + ['positive' if SnowNLP(item[5]).sentiments > 0.5 else 'neutral' if SnowNLP(item[5]).sentiments == 0.5 else 'negative']
            for item in tableList
        ]
    return tableList