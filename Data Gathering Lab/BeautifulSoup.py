#Note this code worked in google colab unsure if it will work outside that enviroment.

from urllib.request import urlopen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import re
%matplotlib inline

url = "https://www.hubertiming.com/results/2023WyEasterLong"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
text = soup.get_text()
rows = soup.find_all('tr')
list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)


df = pd.DataFrame(list_rows)
df.head(10)
df1 = df[0].str.split(',', expand=True)
df1.head(10)
df1[0] = df1[0].str.strip('[')
df1.head(10)
col_labels = soup.find_all('th')

all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
df2 = pd.DataFrame(all_header)
df2.head()
df3 = df2[0].str.split(',', expand=True)
df3.head()
frames = [df3, df1]

df4 = pd.concat(frames)
df4.head(10)
df5 = df4.rename(columns=df4.iloc[0])

df6 = df5.dropna(axis=0, how='any')

df7 = df6.drop(df6.index[0])
df7.rename(columns={'[Place': 'Place'},inplace=True)
df7.rename(columns={' Team]': 'Team'},inplace=True)
#df7['Team'] = df7['Team'].str.strip(']')
df7.head()

time_list = df7[' Time'].tolist()

# You can use a for loop to convert 'Chip Time' to minutes

time_mins = []
for i in time_list:
  if(i.count(":") == 2):
    h, m, s = i.split(':')
    math = (int(h) * 3600 + int(m) * 60 + int(s))/60
    time_mins.append(math)
  else:
    m, s = i.split(':')
    math = (int(m) * 60 + int(s))/60
    time_mins.append(math)
df7['Runner_mins'] = time_mins
df7.head()
df7.describe(include=[np.number])

from pylab import rcParams
rcParams['figure.figsize'] = 15, 5


df7.boxplot(column='Runner_mins')
plt.grid(True, axis='y')
plt.ylabel(' Time')
plt.xticks([1], ['Runners'])

x = df7['Runner_mins']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})
plt.show()


f_fuko = df7.loc[df7[' Gender']==' F']['Runner_mins']
m_fuko = df7.loc[df7[' Gender']==' M']['Runner_mins']
sns.distplot(f_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Female')
sns.distplot(m_fuko, hist=False, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Male')
plt.legend()
print("Akira Smedley")


