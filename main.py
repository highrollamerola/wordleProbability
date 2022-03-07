import pandas as pd
import matplotlib
import random
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
pd.options.mode.chained_assignment = None  # default='warn'


# reading csv file
df = pd.read_csv('wordbank.csv', names=['words'])
# print(lst)

# create data frame for sorted values
column_names = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
singleFil = pd.DataFrame(columns=column_names)
loc = pd.DataFrame(columns=column_names)

# process the data
for i in column_names:
    singleFil[i] = df.words.str.contains(i). astype(int)  # total words a letter appears within
    loc[i] = df.words.str.find(i)  # loc: location letter appears within word

loc = loc.mask(loc < 0) + 1
flatloc = loc.mode(axis=0)
flatloc = flatloc.T
flatFil = singleFil.sum(axis=0)

# combine data
wordle = pd.DataFrame({'Probability':flatFil, 'Location':flatloc[0]})
wordle = wordle.sort_values(by=['Probability'], ascending=False)
wordle['Probability'] = wordle['Probability'].div(df.size)

# create list of words that use 5 of the top 10 letters
topten = singleFil[wordle.index[0:10]].copy()
flatTen = topten.sum(axis=1)
topten = topten[flatTen == 5]
flatwords = df.words[topten.index[:]] #list of words using 5 of the top ten letters
# determine word pairs that cover all ten of the top ten letters
dotwords = topten.dot(topten.T)  #dot product with transpose. Orthogonal pairs cover all ten letters
dotwords = dotwords.where(np.triu(np.ones(dotwords.shape)).astype(bool))  # take upper triangle of symmetric matrix
dotwords = dotwords.stack().reset_index()
dotwords.columns = ['Row', 'Column', 'Value']  # reshape as a list of word pairs and their dot product
dotwords = dotwords[dotwords['Value'] == 0]  # Values of 0 contain orthogonal word pairs

# construct a dataframe 'wordPairs' containing the desired word pairs
wordPairs = pd.DataFrame(columns=['word1', 'word2','score'])
wordPairs['word1'] = df.words[dotwords['Row']]
wordPairs.reset_index(drop=True, inplace=True)
word2 =  df.words[dotwords['Column']]
word2.reset_index(drop=True, inplace=True)
wordPairs['word2'] = word2
wordPairs['score'] = np.zeros(len(wordPairs['score']))

# Build dataframe with indexing ['char'][Location] used to score wordPairs
# Score is based on probability of letter being in the specified location
scoreCard = pd.DataFrame(columns=wordle.index[range(0, 10)])
for i in range(0, 10):
    tmp = np.histogram(loc[wordle.index[i]].dropna().values, bins=5, density=True)
    scoreCard[wordle.index[i]] = tmp[0]

# Score the wordPairs
for i in range(0, len(wordPairs['score'])):
    word1 = wordPairs['word1'][i]
    word1 = [*word1]
    word2 = wordPairs['word2'][i]
    word2 = [*word2]
    score1 = 0
    score2 = 0
    for j in range(0, len(word1)):
        score1 += scoreCard[word1[j]][j]
        score2 += scoreCard[word2[j]][j]
    wordPairs['score'][i] = score1 + score2
    if score2 > score1:    # place higher value word first within set
        wordPairs['word1'][i], wordPairs['word2'][i] = wordPairs['word2'][i], wordPairs['word1'][i]

wordPairs = wordPairs.sort_values(by=['score'], ascending=False)
wordPairs.reset_index(drop=True, inplace=True)

#return the best word pair
print('Top ten Wordle openings:')
for i in range(10, 1, -1):
    print(str(i) + ': ' + wordPairs['word1'][i] + ', ' + wordPairs['word2'][i])

print('Number one opening set per highrollamerola: ' + wordPairs['word1'][0] + ', ' + wordPairs['word2'][0])

# plot stuff
fig1, ax1 = plt.subplots()
ax1 = wordle['Probability'].plot.bar(rot=0)
ax1.set_title("Probability of Letter Appearing in a Five Letter Word")
ax1.set_xlabel("Letter")
ax1.set_ylabel("Probability")
plt.grid()

fig2, ax2 = plt.subplots()
ax2 = wordle['Location'].plot.bar(rot=0)
ax2.set_title("Most Likely Location Within Word")
ax2.set_xlabel("Letter")
ax2.set_ylabel("Location")
plt.grid()

plt.show()
