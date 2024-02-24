import tkinter as tk
from tkinter import Text, WORD, N, S, END
import openai
import os
import pickle
import customtkinter

# Initiate App
root = customtkinter.CTk()
root.title("Yaswanth Panguluri ChatGPT Bot")
root.geometry('600x750')
root.iconbitmap('favicon.ico')

# Set Colour scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Submit to ChatGPT
def speak():
    if chat_entry.get():
        filename = "api_key"
        try:
            if os.path.isfile(filename):
                input_file = open(filename, 'rb')
                stuff = pickle.load(input_file)
                # Query ChatGPT
                openai.api_key = stuff
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": chat_entry.get()}
                    ]
                )

                my_text.insert(END, response['choices'][0]['message']['content'])
                my_text.insert(END, "\n\n")

            else:
                input_file = open(filename, 'wb')
                input_file.close()
                # Error Message
                my_text.insert(END, "\n\n You need an API key to talk with chatGPT. Get one here:\n https://platform.openai.com/api-keys")

            # Resize App
            root.geometry('600x750')

        except Exception as e:
            my_text.insert(END, f"\n\n There was an error\n\n{e}")

    else:
        my_text.insert(END, "Hey! You forgot to type anything!")

# Clear the Screen
def clear():
    # Clear the main text box
    my_text.delete(1.0, END)
    # Clear the query entry
    chat_entry.delete(0, END)

# Do API Stuff
def key():
    filename = "api_key"
    try:
        if os.path.isfile(filename):
            input_file = open(filename, 'rb')
            stuff = pickle.load(input_file)
            api_entry.insert(END, stuff)

        else:
            input_file = open(filename, 'wb')
            input_file.close()

        # Resize App
        root.geometry('600x750')

    except Exception as e:
        my_text.insert(END, f"\n\n There was an error\n\n{e}")

def save_key():
    filename = "api_key"
    try:
        output_file = open(filename, 'wb')
        pickle.dump(api_entry.get(), output_file)

        # Delete entry box
        api_entry.delete(0, END)

        # Resize App Smaller
        root.geometry('600x600')

    except Exception as e:
        my_text.insert(END, f"\n\n There was an error\n\n{e}")

# Create Text frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

# Add Text widget To get chat GPT Responses
my_text = Text(text_frame,
               bg="#343638",
               width=65,
               bd=1,
               fg="#d6d6d6",
               relief="flat",
               wrap=WORD,
               selectbackground="#1f538d"
               )
my_text.grid(row=0, column=0)

# Create Scroll bar for for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame, command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky=(N, S))

# Add the scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)

# Entry Widget to type stuff
chat_entry = customtkinter.CTkEntry(root,
                                    placeholder_text="Type Something To ChatGPT...",
                                    width=535,
                                    height=50,
                                    border_width=1)
chat_entry.pack(pady=10)

# Create Button Frame
button_frame = customtkinter.CTkFrame(root)
button_frame.pack(pady=10)

# Create Button
submit_button = customtkinter.CTkButton(button_frame,
                                        text="Speak To ChatGPT",
                                        command=speak)
submit_button.grid(row=0, column=0, padx=25)

# Create Clear Button
clear_button = customtkinter.CTkButton(button_frame,
                                       text="Clear Response",
                                       command=clear)
clear_button.grid(row=0, column=1, padx=35)

# Create API Key Button
api_button = customtkinter.CTkButton(button_frame,
                                     text="Update API Key",
                                     command=key)
api_button.grid(row=0, column=2, padx=25)

# Add API Key frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

# Add API Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
                                   placeholder_text="Enter your API Key",
                                   width=350,
                                   height=50,
                                   border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

# Add Save Key Button
api_save_button = customtkinter.CTkButton(api_frame,
                                          text="Save Key",
                                          command=save_key)
api_save_button.grid(row=0, column=1, padx=10)

root.mainloop()
