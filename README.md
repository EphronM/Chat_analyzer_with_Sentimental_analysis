
# Analyzing whatsapp chats with Sentimental analysis

**[Demo Site Link](https://chat-analyser-w.herokuapp.com)**

Analyzing the data has become very esential part of our day to day life.
Its helps to take decision visely. In the world of digitalisation,
whatsapp has become one of our main source of texting and communicating.
Unfortunatly we get into so many group conversations and doesnt understand that is going on.


Using a chat analyzer would clearly give you an idea of how active and healthy the group is.
Its a demo statistics of our peorsal groups.

![ezgif com-gif-maker](https://user-images.githubusercontent.com/94764266/152677051-429643d5-662a-4363-8a3b-cae289808a35.gif)

## Run this webApp localy

Clone the repository

```bash
https://github.com/EphronM/chat_analyzer_with_sentimental_analysis.git
```
* Note: WordCloud has a issue of not getting installed on newer python versions. Its preferred to set runtime as Python 3.7 

#### Create a conda environment after opening the repository

```bash
conda create -n chatenv python=3.7 -y
```

```bash
conda activate chatenv
```


#### Installing the required dependencies
```bash
pip install -r requirements.txt
```


#### All set to run the webApp
```bash
streamlit run app.py
```



## where do you get these datas from?

Whatsapp has an intresting feature to export out chats in a **.txt** format.

```bash
Open chat >> More >> Export chat >> Without Media
```
We need the text formated data, hence media files doesnt play any role.
You could try this webApp for both group and direct chats.


## Analysing raw data

After uploading the text file to the webapp, it converts the text into clean pandas dataframe, makes it more
 converient for analysing.


If the uploaded data is from a group chat, it fetches the user names and displays it on a dropdown menu.
We could either analyze individual performance as will as overall analytics.

![06 02 2022_16 48 26_REC](https://user-images.githubusercontent.com/94764266/152678291-a244f64f-ff86-4447-b808-8ed7d8e90037.png)

Initially displays the total message count by taking the length of the dataset. 
As we have taken the data without media, those positions are with *<Media omitted>*
as message, media count is the count of the occurance.
Using the **URLExtract**, we extract the links present in the chat. And finaly count the words
in the chat by spliting the string gives us the total word count.

### Finding the most active users
This is only performed in group chat or the "overall" option is selected.

![06 02 2022_17 00 47_REC](https://user-images.githubusercontent.com/94764266/152678775-d7d2d4b2-8bdb-4ea3-bf7c-e4f7f095e6d4.png)


BY taking the value count for "USERS" features from the dataset.
The bar plot and the top active users table is displayed.

#### The wordCloud
![wordcloud](https://user-images.githubusercontent.com/94764266/152689566-75a3517c-39c7-4262-afc8-3f62c88062d9.png)


Creating a wordcloud that shows the combination of the most 
frequently used words. The words 
in the cloud tells us if the chat language is formal 
or informal. The stopwords and puntuations are removed inorder to acheived relavent words.

#### Most common words
Succeeding the word cloud, there is word count table 
that exhibits a list of the most commonly used words 
along with the number of times the word has been used.
For easier interpretation, the same data has been
 conveyed through a horizontel bar graph.

#### The routine of emojis
A similar table displaying the values of the often 
used emojis. The most commonly icon used by people 
to express their emotions digitally tops the list. Using
**emoji.UNICODE_EMOJI['en']** package which contains most of the emoji avaiable and counting the value if present gives us the emoji count.


#### Timelines
![monthy](https://user-images.githubusercontent.com/94764266/152689960-6a46b45c-6e8e-44bc-b7b5-b14dc4c17b44.png) ![daily](https://user-images.githubusercontent.com/94764266/152689961-e171fda6-8d6d-49e7-a805-7c906a9f2570.png)


Two consecutive line graphs are present to display 
the message traffic wrt monthy and daily basis. This gives us a very indepth insights on the group.

#### Bar plot for busy months and days

![busy_month](https://user-images.githubusercontent.com/94764266/152690245-cfaeb200-f941-4ad0-b5ae-a48692b641bb.png) ![busy_day](https://user-images.githubusercontent.com/94764266/152690244-ae9171cc-dae9-48f0-b5a2-2f2a264613b5.png)

Barplot are famous for there simpliest way of represting and understanding nature. From this, we clearly understand which month of the year or which day of the week
the group is active the most. This can tell us a the story for why a particular month was the busiest and why other the least.


#### Periodic Heatmap
![heatmap](https://user-images.githubusercontent.com/94764266/152690406-ae71ad25-971d-4ef0-85e9-9330a9f6fd87.png)

The whole dataset was divided into the hourly basis by creating a new feature named period by adding the preceding hour to the current hour feature.
Thus, by creating a **Pivot table** by assigning index as day names, value as messages and columns value as newly prepared period feature.

Using the seaborn Heatmap, the matrix is formed using the prepared Pivot table.
This tells us, at which period of the day the traffic was at the peak and the least.

### Sentimental Analysis

Using the NLTK - vadar_lexicon package **Sentiment Intensity Analyzer**  is imported and applied on the dataset of message.

The Analyzer gives us the polarity score for

* Positive
* Negative
* Neutral

![sentimal_all](https://user-images.githubusercontent.com/94764266/152691269-1e0eec69-81cb-4480-ade0-ad1114bfea50.png)

 And the values are assigned as each separate feature. By calulating the total sum of all the 3 new features, and 
 comparing the values to find the max to give the corresponding Sentiment as overall sentiments.

By ploting all three total sums gives the overall sentiments of the chat.
To compare the diffrence between positive and negative sentiments, separate pie chat is plotted for total positive & negative.

![senti](https://user-images.githubusercontent.com/94764266/152691248-17611f8b-97f3-4e81-bb16-9106cc482660.png)



```bash
Author: EphronM
Email: ephronmartin2016@gmail.com

```
