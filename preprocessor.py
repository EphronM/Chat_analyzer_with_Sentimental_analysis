import re
import pandas as pd


def preprocess_data(data):
    pattern = '\d{2}\/\d{2}\/\d{4},\s\d(?:\d)?:\d{2}\s[ap]m\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages': message, 'date_time': dates})
    df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%m/%Y, %I:%M %p - ')

    user = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            user.append(entry[1])
            messages.append(entry[2].split('\n')[0])
        else:
            user.append('Group Notification')
            messages.append(entry[0].split('\n')[0])

    df['User'] = user
    df['message'] = messages
    df.drop(columns='user_messages', inplace=True)

    df['year'] = df['date_time'].dt.year
    df['month'] = df['date_time'].dt.month_name()
    df['date'] = df['date_time'].dt.day
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute
    df['month_num'] = df['date_time'].dt.month
    df['full_date'] = df['date_time'].dt.date
    df['day_name'] = df['date_time'].dt.day_name()


    return df
