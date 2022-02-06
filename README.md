
# Analyzing whatsapp chats with Sentimental analysis

Analyzing the data has become very esential part of our day to day life.
Its helps to take decision visely. In the world of digitalisation,
whatsapp has become one of our main source of texting and communicating.
Unfortunatly we get into so many group conversations and doesnt understand that is going on.


Using a chat analyzer would clearly give you an idea of how active and healthy the group is.
Its a demo statistics of our peorsal groups.

![ezgif com-gif-maker](https://user-images.githubusercontent.com/94764266/152677051-429643d5-662a-4363-8a3b-cae289808a35.gif)


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

###


https://chat-analyser-w.herokuapp.com/















mkdir -p ~/.streamlit

echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
