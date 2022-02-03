import streamlit as st
from preprocessor import preprocess_data
import analyzer
import seaborn as sns
import matplotlib.pyplot as plt
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('chat_analyzer_bg.jpg')

st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    up_data = uploaded_file.getvalue()
    data = up_data.decode("utf-8")
    df = preprocess_data(data)


    #fetch unique user
    user_list = df['User'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show analysis wrt ",user_list)

    #fetch stats
    num_messages, words, media, links = analyzer.fetch_stats(selected_user, df)

    if st.sidebar.button('Show Analysis'):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header('Media shared')
            st.title(media)
        with col3:
            st.header('Total Word count')
            st.title(words)
        with col4:
            st.header('Total Links shared')
            st.title(links)

        #busy user
        if selected_user == 'Overall':
            st.header("Most Busy Users")

            users, values, new_df = analyzer.busy_user(df)

            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                sns.barplot(x=users, y=values)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #word cloud creation
        df_wc = analyzer.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.header('Word Cloud')
        plt.axis('off')
        st.pyplot(fig)

        #most common words
        st.header('Most Common Words')
        most_common_df = analyzer.most_common_words(selected_user, df)
        col1, col2 = st.columns(2)
        fig, ax = plt.subplots()

        with col1:
            st.dataframe(most_common_df)
        with col2:
            sns.barplot(x=most_common_df['count'], y=most_common_df['Word'])
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
            st.pyplot(fig)

        #Emoji Counter
        st.header("Most used Emojis")
        emoji_df = analyzer.emoji_counter(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            colors = sns.color_palette('pastel')[0:10]
            plt.pie(emoji_df['Count'][:10], colors = colors)
            st.pyplot(fig)

        with col2:
            st.dataframe(emoji_df.head(10))



        monthy_timeline_df = analyzer.monthy_timeline_df(selected_user, df)
        daily_timeline_df = analyzer.daily_timeline_df(selected_user, df)

        st.header('Daily and Monthy Timelines')

        col1, col2 = st.columns(2)

        # monthy timeline data
        with col1:
            fig, ax = plt.subplots()
            m= sns.lineplot(data = monthy_timeline_df, x='time', y='message')
            m.set_xticklabels(labels=monthy_timeline_df['time'], rotation=90)
            st.pyplot(fig)

        #Daily timeline data
        with col2:
            fig, ax = plt.subplots()
            d = sns.lineplot(data=daily_timeline_df, x='full_date', y='message')
            d.set_xticklabels(labels=daily_timeline_df['full_date'], rotation=90)
            st.pyplot(fig)

        #busy day and month
        busy_day, busy_month = analyzer.busy_month_day(selected_user, df)

        st.header('Busy days and months')
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            sns.barplot(busy_day.index, busy_day.values)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            sns.barplot(busy_month.index, busy_month.values)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
            st.pyplot(fig)

        #periodic timeline
        periodic_df = analyzer.periodic_timeline_df(selected_user, df)
        st.header('Periodic heatmap')

        fig, ax = plt.subplots(figsize=(27,10))
        sns.heatmap(periodic_df,cmap="Blues")
        st.pyplot(fig)

        #sentiment analysis
        st.title('Sentimental Analysis')

        score, t_pos, t_neg, t_neu = analyzer.sentimental_analysis(selected_user, df)
        st.header(f'The overall chat is of {score} sentimental')

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            data = [t_pos, t_neg, t_neu]
            label = ['Positive', 'Negative', 'Neutral']
            explode = (0.0, 0.0, 0.3)
            colors = sns.color_palette('pastel')[0:3]
            plt.pie(data, labels=label, autopct='%1.1f%%', explode=explode, shadow=True, colors=colors)
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            data = [t_pos, t_neg]
            label = ['Positive', 'Negative']
            color = ['#77DD77', '#FF6961']
            explode = (0.0, 0.15)
            plt.pie(data, labels=label, autopct='%1.1f%%', shadow=True, colors=color, explode=explode)
            st.pyplot(fig)
