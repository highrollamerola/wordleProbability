import pandas as pd
import matplotlib
import random
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


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
singleFil = singleFil.sum(axis=0)

# combine data
wordle = pd.DataFrame({'Probability':singleFil, 'Location':flatloc[0]})
wordle = wordle.sort_values(by=['Probability'], ascending=False)
# wordle['Probability'] = wordle['Probability'].div(wordle['Probability'].sum())
wordle['Probability'] = wordle['Probability'].div(df.size)

# Return a random five letter word
print(df.words[random.randint(0,len(df))])

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

loc.hist(column='a')
loc.hist(column='t')
loc.hist(column='u')

plt.show()

