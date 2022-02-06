import streamlit as st
from preprocessor import preprocess_data
import analyzer
import seaborn as sns
import matplotlib.pyplot as plt
from static.load_css import local_css
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

set_background('artifacts/chat_analyzer_bg.jpg')


local_css("static/style.css")


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
        main_title = "<center><div><p class='highlight grey' style='font-size:35px'><span class='bold'>Lets Analyze</span></span></div></center>"
        st.markdown(main_title, unsafe_allow_html=True)
        st.markdown('<br><br>', unsafe_allow_html=True)
        

        col1, col2, col3, col4 = st.beta_columns(4)
        with col1:
            tol_msg_md = f"<center><div><p class='highlight grey' style='font-size:25px'><span class='bold'>Total Messages</span></div></center><br>"
            st.markdown(tol_msg_md, unsafe_allow_html=True)
            tol_num = f"<center><div><span class='highlight grey' style='font-size:25px'><span class='bold'>{num_messages}</span></div></center>"
            st.markdown(tol_num, unsafe_allow_html=True)
        with col2:
            media_shared_md = f"<center><div><p class='highlight grey' style='font-size:25px'><span class='bold'>Media shared</span></div></center><br>"
            st.markdown(media_shared_md, unsafe_allow_html=True)
            media_count = f"<center><div><span class='highlight grey' style='font-size:25px'><span class='bold'>{media}</span></div></center>"
            st.markdown(media_count, unsafe_allow_html=True)
        with col3:
            tol_word_count_md = f"<center><div><p class='highlight grey' style='font-size:25px'><span class='bold'>Word count</span></div></center><br>"
            st.markdown(tol_word_count_md, unsafe_allow_html=True)
            tol_words = f"<center><div><p class='highlight grey' style='font-size:25px'><span class='bold'>{words}</span></div></center>"
            st.markdown(tol_words, unsafe_allow_html=True)
        with col4:
            tol_link_md = f"<center><div><p class='highlight grey' style='font-size:25px'><span class='bold'>Links shared</span></div></center><br>"
            st.markdown(tol_link_md, unsafe_allow_html=True)
            links_count = f"<center><div><span class='highlight grey' style='font-size:25px'><span class='bold'>{links}</span></div></center>"
            st.markdown(links_count, unsafe_allow_html=True)
           
        #busy user
        if selected_user == 'Overall':
            st.markdown('<br><br>', unsafe_allow_html=True)
            busy_user = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Most Busy Users</span></div><center>"
            st.markdown(busy_user, unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            users, values, new_df = analyzer.busy_user(df)

            

            col1, col2 = st.beta_columns(2)
            with col1:
                fig, ax = plt.subplots()
                sns.barplot(x=users, y=values)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
                fig.patch.set_facecolor('#E6E6E6')
                fig.patch.set_alpha(0.5)
                ax.set_facecolor('#eafff5')
                ax.patch.set_alpha(0.5)
                st.pyplot(fig)
            with col2:
                busy_ppl_html = new_df.head(7).to_html()
                st.markdown(f"<center>{busy_ppl_html}</center>", unsafe_allow_html=True)

        #word cloud creation
        st.markdown('<br><br>', unsafe_allow_html=True)
        word_cloud = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Word Cloud</span></div><center>"
        st.markdown(word_cloud, unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)

        df_wc = analyzer.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#E6E6E6')
        fig.patch.set_alpha(0.5)
        ax.imshow(df_wc)
        ax.set_facecolor('#eafff5')
        ax.patch.set_alpha(0.5)
        

        plt.axis('off')
        st.pyplot(fig)

        #most common words
        st.markdown('<br><br>', unsafe_allow_html=True)
        most_common_words = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Most common Words</span></div><center>"
        st.markdown(most_common_words, unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        most_common_df = analyzer.most_common_words(selected_user, df)

        col1, col2 = st.beta_columns(2)
        

        with col1:
            most_common_html = most_common_df.head(5).to_html()
            st.markdown(f"<center>{most_common_html}</center>", unsafe_allow_html=True)
        with col2:
            fig, ax = plt.subplots()
            sns.barplot(x=most_common_df['count'], y=most_common_df['Word'])
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
            fig.patch.set_facecolor('#E6E6E6')
            fig.patch.set_alpha(0.5)
            ax.set_facecolor('#eafff5')
            ax.patch.set_alpha(0.5)
            st.pyplot(fig)

        #Emoji Counter
        st.markdown('<br><br>', unsafe_allow_html=True)
        emoji_count = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>The most used Emojis</span></div><center>"
        st.markdown(emoji_count, unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)


        emoji_df = analyzer.emoji_counter(selected_user, df)
        emoji_html = emoji_df.head(5).to_html()
        st.markdown(f"<center>{emoji_html}</center>", unsafe_allow_html=True)
        #st.table(emoji_df.head(5))



        monthy_timeline_df = analyzer.monthy_timeline_df(selected_user, df)
        daily_timeline_df = analyzer.daily_timeline_df(selected_user, df)

        st.markdown('<br><br>', unsafe_allow_html=True)
        daily_monthy = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Daily and Monthy Timelines</span></div><center><br>"
        st.markdown(daily_monthy, unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)

        col1, col2 = st.beta_columns(2)

        # monthy timeline data
        with col1:
            fig, ax = plt.subplots()
            m= sns.lineplot(data = monthy_timeline_df, x='time', y='message', palette='r')
            m.set_xticklabels(labels=monthy_timeline_df['time'], rotation=90)
            fig.patch.set_facecolor('#E6E6E6')
            fig.patch.set_alpha(0.5)
            ax.set_facecolor('#eafff5')
            ax.patch.set_alpha(0.5)
            st.pyplot(fig)

        #Daily timeline data
        with col2:
            fig, ax = plt.subplots()
            d = sns.lineplot(data=daily_timeline_df, x='full_date', y='message',palette='r')
            d.set_xticklabels(labels=daily_timeline_df['full_date'], rotation=90)
            fig.patch.set_facecolor('#E6E6E6')
            fig.patch.set_alpha(0.5)
            ax.set_facecolor('#eafff5')
            ax.patch.set_alpha(0.5)
            st.pyplot(fig)

        #busy day and month
        busy_day, busy_month = analyzer.busy_month_day(selected_user, df)

        st.markdown('<br><br>', unsafe_allow_html=True)
        busy_month_day = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Busy Days and Months</span></div><center>"
        st.markdown(busy_month_day, unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        col1, col2 = st.beta_columns(2)

        with col1:
            fig, ax = plt.subplots()
            sns.barplot(busy_day.index, busy_day.values)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
            fig.patch.set_facecolor('#E6E6E6')
            fig.patch.set_alpha(0.5)
            ax.set_facecolor('#eafff5')
            ax.patch.set_alpha(0.5)
            st.pyplot(fig)

            

        with col2:
            fig, ax = plt.subplots()
            sns.barplot(busy_month.index, busy_month.values)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
            fig.patch.set_facecolor('#E6E6E6')
            fig.patch.set_alpha(0.5)
            ax.set_facecolor('#eafff5')
            ax.patch.set_alpha(0.5)
            st.pyplot(fig)

            

        #periodic timeline
        periodic_df = analyzer.periodic_timeline_df(selected_user, df)
        st.markdown('<br><br>', unsafe_allow_html=True)
        
        periodic_heat = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Periodic heatmap</span></div><center>"
        st.markdown(periodic_heat, unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(27,10))
        sns.heatmap(periodic_df,cmap="Blues")
        fig.patch.set_facecolor('#E6E6E6')
        fig.patch.set_alpha(0.5)
        ax.set_facecolor('#eafff5')
        ax.patch.set_alpha(0.5)
        st.pyplot(fig)

        #st.pyplot(fig)

        #sentiment analysis
        st.markdown('<br><br>', unsafe_allow_html=True)
        sentiments = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>sentiment Analysis</span></div><center>"
        st.markdown(sentiments, unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)

        score, t_pos, t_neg, t_neu = analyzer.sentimental_analysis(selected_user, df)
        score_md = f"<center><div><span class='highlight grey' style='font-size:18px'><span class='bold'>The overall chat is of {score} sentimental</span></div><center><br><br>"
        st.markdown(score_md, unsafe_allow_html=True)
        st.markdown('<br><br>', unsafe_allow_html=True)



        col1, col2 = st.beta_columns(2)
        with col1:
            data = [t_pos, t_neg, t_neu]
            fig, ax = plt.subplots()
            label = ['Positive', 'Negative', 'Neutral']
            explode = (0.0, 0.0, 0.3)
            colors = sns.color_palette('pastel')[0:3]
            plt.pie(data, labels=label, autopct='%1.1f%%', explode=explode, shadow=True, colors=colors)
            fig.patch.set_facecolor('#E6E6E6')
            fig.patch.set_alpha(0.5)
            ax.set_facecolor('#eafff5')
            ax.patch.set_alpha(0.5)
            st.pyplot(fig)

             
        with col2:
            data = [t_pos, t_neg]
            fig, ax = plt.subplots()
            label = ['Positive', 'Negative']
            color = ['#77DD77', '#FF6961']
            explode = (0.0, 0.15)
            plt.pie(data, labels=label, autopct='%1.1f%%', shadow=True, colors=color, explode=explode)
            fig.patch.set_facecolor('#E6E6E6')
            fig.patch.set_alpha(0.5)
            ax.set_facecolor('#eafff5')
            ax.patch.set_alpha(0.5)
            st.pyplot(fig)
        
            #st.image('artifacts/pos_neg.png')
            st.markdown('<br>', unsafe_allow_html=True)
        
            
