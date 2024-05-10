import streamlit as st
import requests
import json
import sqlite3

chat_history = []

conn = sqlite3.connect('message.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS messages (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL
)''') 




def call_web_service(message):
    response = requests.post('http://localhost:8000/chat/', json={'text': message})
    return response.json()

st.title('Chat Interface')

user_input = st.text_input("Type your message here:", key="user_input")
if st.button("Send"):
    if user_input:
        response = call_web_service(user_input)
        chat_history.append("You :" + " " + user_input)
        chat_history.append("DocChat :" + " " + response["message"])
        for message in chat_history:
            format_sql_insert = "INSERT INTO messages (message) VALUES ('{value}')".format(value=message)
            print("DEBUG:  " + format_sql_insert)
            c.execute(format_sql_insert)
        conn.commit()

        c.execute("Select message from messages order by id desc")
        msg_from_db = c.fetchall()

        for op_message in msg_from_db:
            st.write(op_message[0])

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

if st.sidebar.button('Load Chat'):
    st.session_state.button_clicked = True

if st.session_state.button_clicked:
    response = requests.post('http://localhost:8000/loadvector/', json={"text": "_chat"})
    #st.write(response.text)
