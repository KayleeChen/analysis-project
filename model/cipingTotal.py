import jieba
import re

def main():
    reader = open('./cutComments.txt', 'r', encoding='utf8')
    strs = reader.read()
    result = open('./cipingTotal.csv', 'w', encoding='utf8')

    # Perform segmentation and remove duplicates
    word_list = jieba.cut(strs, cut_all=False)

    # Use regular expressions to remove numbers, symbols, and single characters
    new_words = []
    for i in word_list:
        m = re.search("\d+", i) # Check if the word contains digits
        n = re.search("\W+", i)  # Use set to remove duplicates from the list
        if not m and not n and len(i) > 1: # Count occurrences of each word
            new_words.append(i)

    # Count word frequencies
    word_count = {}  # Create a dictionary to store word counts
    for i in set(new_words):   # Use set to remove duplicates from the list
        word_count[i] = new_words.count(i) # Count occurrences of each word

    # Format the result
    list_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True) # Sort by frequency in descending order

    for i in range(300):
        print(list_count[i], file=result) # Write the top 300 words to the result file


if __name__ == '__main__':
        main()