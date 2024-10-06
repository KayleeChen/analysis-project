from utils.getPublicData import getAllCommentsData
import jieba
import jieba.analyse as analyse

targetTxt = 'cutComments.txt'

def stopWordList():
    #  Get the list of stop words from stopWords.txt file
    stopWord = [line.strip() for line in open('./stopWords.txt',encoding='UTF-8').readlines()]
    return stopWord

def seg_depart(sentence):
    # Perform segmentation on the sentence and remove stop words
    # Segment the sentence
    sentence_depart = jieba.cut(" ".join([x[4] for x in sentence]).strip())
    stopwords = stopWordList()
    outstr = ''
    # remove stopWords
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
    return outstr

def writer_comment_fenci():
    # Write the segmented comments into the target file.
    with open(targetTxt, 'a+', encoding='utf-8') as targetFile:
        seg = jieba.cut(seg_depart(getAllCommentsData()), cut_all=False)
        # Separate segmented words by spaces
        output = ' '.join(seg)
        targetFile.write(output)
        targetFile.write('\n')
        print('Successfully written！')


if __name__ == '__main__':
    writer_comment_fenci()