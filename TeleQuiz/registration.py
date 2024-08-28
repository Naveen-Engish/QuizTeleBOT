import csv
from telebot import types
import json

# Temporary storage for team members' information
temp_data = {}
registration_step = {}

def register_leader(message, bot):
    """Start the registration process by asking for the leader's registration number."""
    msg = bot.reply_to(message, "Enter Team Leader's Registration Number:")
    bot.register_next_step_handler(msg, lambda msg: process_registration_number(msg, bot))

def process_registration_number(message, bot):
    """Process the registration number and confirm the associated name."""
    chat_id = message.chat.id
    registration_number = message.text
    
    try:
        # Open the CSV file and search for the registration number
        with open("C:/Users/USER/Desktop/TeleQuiz/Data/Students.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == registration_number:
                    leader_name = row[1]
                    
                    # Store the registration number and name temporarily
                    temp_data[chat_id] = {'registration_number': registration_number, 'name': leader_name}
                    
                    # Ask the user to confirm or edit the name
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("Edit", callback_data="edit_leader"))
                    markup.add(types.InlineKeyboardButton("Confirm", callback_data="confirm_leader"))
                    
                    bot.send_message(chat_id, f"Is this correct?\nName: {leader_name}", reply_markup=markup)
                    return
                
        # If registration number not found
        bot.reply_to(message, "Registration number not found. Please try again.")
        register_leader(message, bot)  # Restart the registration process
    except FileNotFoundError:
        bot.reply_to(message, "students.csv file not found.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

def handle_callback(call, bot):
    """Handle the callback from the inline buttons."""
    chat_id = call.message.chat.id

    if call.data.startswith("edit_"):
        # Determine which member is being edited
        member_type = call.data.split("_")[1]
        bot.answer_callback_query(call.id, "Please enter the registration number again.")
        
        if member_type == "leader":
            register_leader(call.message, bot)
        elif member_type in ["member1", "member2"]:
            # Update registration step to restart the process
            registration_step[chat_id] = member_type
            register_member(call.message, bot, member_type)
        
        # Edit the message to remove the inline keyboard
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="Please enter the registration number again.",
            reply_markup=None  # This removes the inline keyboard
        )

    elif call.data.startswith("confirm_"):
        # Determine which member is being confirmed
        member_type = call.data.split("_")[1]
        leader_info = temp_data.get(chat_id)
        if leader_info:
            if member_type == "leader":
                bot.answer_callback_query(call.id, f"Team Leader Registered!\nName: {leader_info['name']}")
                # Proceed to register member 1
                registration_step[chat_id] = 'member1'
                bot.send_message(chat_id, "Now enter the Registration Number for Member 1:")
                bot.register_next_step_handler_by_chat_id(chat_id, lambda msg: process_member_registration(msg, bot, "member1"))
                
                # Remove the inline keyboard from the previous message
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    text=f"Team Leader Registered!\nName: {leader_info['name']}",
                    reply_markup=None
                )
            elif member_type in ["member1", "member2"]:
                bot.answer_callback_query(call.id, f"Team {member_type.capitalize()} Registered!\nName: {leader_info[f'name_{member_type}']}")
                if member_type == "member1":
                    # Proceed to register member 2
                    registration_step[chat_id] = 'member2'
                    bot.send_message(chat_id, "Now enter the Registration Number for Member 2:")
                    bot.register_next_step_handler_by_chat_id(chat_id, lambda msg: process_member_registration(msg, bot, "member2"))
                elif member_type == "member2":
                    # Finish registration
                    bot.send_message(chat_id, f"All team members have been registered successfully! {temp_data}")
                    # Open the JSON file in write mode
                    with open('C:/Users/USER/Desktop/TeleQuiz/Data/team_data.json', 'a') as f:
                        # Dump the temporary data into the JSON file
                        json.dump(temp_data, f, indent=4)  # Indent for better readability

                    print("Data added to data.json successfully.")
                    registration_step.pop(chat_id, None)  # Remove step for completed registration

                # Remove the inline keyboard from the previous message
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    text=f"Team {member_type.capitalize()} Registered!\nName: {leader_info[f'name_{member_type}']}",
                    reply_markup=None
                )
            else:
                bot.answer_callback_query(call.id, "Unexpected member type.")
        else:
            bot.answer_callback_query(call.id, "No data found to confirm.")
            
            # Edit the message to remove the inline keyboard
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text="No data found to confirm.",
                reply_markup=None
            )


def register_member(message, bot, member_type):
    """Start the registration process for a team member."""
    # Clear the current registration step
    registration_step.pop(message.chat.id, None)
    
    msg = bot.reply_to(message, f"Enter Team {member_type.capitalize()}'s Registration Number:")
    bot.register_next_step_handler(msg, lambda msg: process_member_registration(msg, bot, member_type))


def process_member_registration(message, bot, member_type):
    """Process the registration number for a team member and confirm the associated name."""
    chat_id = message.chat.id
    registration_number = message.text
    
    try:
        # Open the CSV file and search for the registration number
        with open("C:/Users/USER/Desktop/TeleQuiz/Data/Students.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == registration_number:
                    member_name = row[1]
                    
                    # Store the registration number and name temporarily
                    temp_data[chat_id][f'registration_number_{member_type}'] = registration_number
                    temp_data[chat_id][f'name_{member_type}'] = member_name
                    
                    # Ask the user to confirm or edit the name
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("Edit", callback_data=f"edit_{member_type}"))
                    markup.add(types.InlineKeyboardButton("Confirm", callback_data=f"confirm_{member_type}"))
                    
                    bot.send_message(chat_id, f"Is this correct?\nName: {member_name}", reply_markup=markup)
                    return
                
        # If registration number not found
        bot.reply_to(message, "Registration number not found. Please try again.")
        register_member(message, bot, member_type)  # Restart the registration process
    except FileNotFoundError:
        bot.reply_to(message, "students.csv file not found.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")
