from snownlp import SnowNLP
import csv
import os
from utils.getPublicData import getAllCommentsData

def targetFile():
    targetFile = 'target.csv'
    commentsList = getAllCommentsData()

    rateData = []
    positive = 0
    negative = 0
    neutral = 0

    # Iterate through the comments list
    for index, i in enumerate(commentsList):
        score = SnowNLP(i[4]).sentiments
        if score > 0.5:
            positive += 1
            rateData.append([i[4], 'positive'])
        elif score == 0.5:
            neutral += 1
            rateData.append([i[4], 'neutral'])
        elif score < 0.5:
            negative += 1
            rateData.append([i[4], 'negative'])

    # Write the sentiment analysis results to a CSV file
    for i in rateData:
        with open (targetFile, 'a+', encoding='utf8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(i)

def main():
    targetFile()

if __name__ == '__main__':
    main()