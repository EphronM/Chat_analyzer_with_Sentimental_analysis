from urlextract import URLExtract
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
import emoji
from collections import Counter
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    media_files = df[df['message'] == '<Media omitted>']

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), len(media_files), len(links)

def busy_user(df):
    users = df['User'].value_counts().index[:10]
    values = df['User'].value_counts().values[:10]
    new_df = np.round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'Name', 'User': 'Percentage'})
    return users, values, new_df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'Group Notification']
    temp = temp[temp['message'] != '<Media omitted>']

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'Group Notification']
    temp = temp[temp['message'] != '<Media omitted>']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.extend(message.split())


    most_common_df = pd.DataFrame(Counter(words).most_common(15), columns=['Word','count' ])

    return most_common_df

def emoji_counter(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([e for e in message if e in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emoji', 'Count'])

    return emoji_df

def monthy_timeline_df(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    time_line = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(time_line.shape[0]):
        time.append(time_line['month'][i] + '-' + str(time_line['year'][i]))

    time_line['time'] = pd.DataFrame(time)
    return time_line

def daily_timeline_df(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('full_date').count()['message'].reset_index()
    return daily_timeline

def busy_month_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    busy_day = df['day_name'].value_counts()
    busy_month = df['month'].value_counts()
    return busy_day, busy_month

def periodic_timeline_df(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    periodic_df = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return periodic_df

def sentimental_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    senti_analyzer = SentimentIntensityAnalyzer()
    senti_df = df[['User', 'message', 'date_time']]

    senti_df['postive'] = [senti_analyzer.polarity_scores(i)['pos'] for i in df['message']]
    senti_df['negative'] = [senti_analyzer.polarity_scores(i)['neg'] for i in df['message']]
    senti_df['neutral'] = [senti_analyzer.polarity_scores(i)['neu'] for i in df['message']]

    t_pos = senti_df['postive'].sum()
    t_neg = senti_df['negative'].sum()
    t_neu = senti_df['neutral'].sum()

    def sentiment_score(pos, neg, neu):
        if (pos > neg) and (pos > neu):
            return 'Positive'
        elif (neg > pos) and (neg > neu):
            return 'Negative'
        else:
            return 'Neutral'

    score = sentiment_score(t_pos, t_neg, t_neu)

    return score, t_pos, t_neg, t_neu