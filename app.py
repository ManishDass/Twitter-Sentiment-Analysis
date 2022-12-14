#==========================================
# Title:  Twitter Sentiment Analysis
# Author: Manish Das & Shahid Sadiq
# Date:   12 Nov 2022
#Status: TextCloud Module is in progress
#==========================================

from attr import has
import streamlit as st
from helper import preprocessing_data, graph_sentiment, analyse_mention, analyse_hastag, download_data


st.set_page_config(
     page_title="TSA By Manish Das",
     page_icon="📊",
     layout="wide",
     initial_sidebar_state="expanded",
)

title = "";

st.title("Twitter Sentimental Analysis ")

function_option = st.sidebar.selectbox("Select The Funtionality: ", ["Search By #Tag and Words", "Search By Username"])

if function_option == "Search By #Tag and Words":
    word_query = st.text_input("Enter the Hastag or any word")
    title = word_query

if function_option == "Search By Username":
    word_query = st.text_input("Enter the Username ( Don't include @ )")
    title = word_query

number_of_tweets = st.slider("How many tweets You want to collect from {}".format(word_query), min_value=100, max_value=10000)
st.info("1 Tweets takes approx 0.05 sec so you may have to wait {} minute for {} Tweets, So Please Have Patient.".format(round((number_of_tweets*0.05/60),2), number_of_tweets))

if st.button("Analysis Sentiment"):
    data = preprocessing_data(word_query, number_of_tweets, function_option)
    analyse = graph_sentiment(data)  
    mention = analyse_mention(data)
    hastag = analyse_hastag(data)

    st.write(" ")
    st.write(" ")
    st.header("Extracted and Preprocessed Dataset")
    st.write(data)
    download_data(data, label=title)
    st.write(" ")
    

    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("### EDA On the Data")


    col1, col2 = st.columns(2)

    with col1:
        st.text("Top 10 @Mentions in {} tweets".format(number_of_tweets))
        st.bar_chart(mention)
    with col2:
        st.text("Top 10 Hastags used in {} tweets".format(number_of_tweets))
        st.bar_chart(hastag)
    
    col3, col4 = st.columns(2)
    with col3:
        st.text("Top 10 Used Links for {} tweets".format(number_of_tweets))
        st.bar_chart(data["links"].value_counts().head(10).reset_index())
    
    with col4:
        st.text("All the Tweets that containes top 10 links used")
        filtered_data = data[data["links"].isin(data["links"].value_counts().head(10).reset_index()["index"].values)]
        st.write(filtered_data)


    #Printing Bar Chart
    st.subheader("Twitter Sentment Analysis Bar Chart")
    st.bar_chart(analyse)


    #Display Wordcloud //Work in Progress
    #st.text(hastag)
    # stopwords = set(STOPWORDS)
    # stopwords.update(["the", "a", "an", "in"])
    # wordcloud = WordCloud(width=1600, stopwords=stopwords,height=800,max_font_size=200,max_words=50,collocations=False, background_color='black').generate(hastag)
    # plt.figure(figsize=(40,30))
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()


#Just to hide the "Made with Streamlit"
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    





    