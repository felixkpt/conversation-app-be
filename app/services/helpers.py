from langdetect import detect


def is_english(text):
    try:
        return detect(text) == 'en'
    except Exception as e:
        print(f"Error detecting language: {e}")
        return False


def filter_english_messages(messages, limit=5):
    # Initialize an empty list to store English messages
    english_messages = []

    # Initialize a counter to keep track of the number of English messages found
    english_count = 0

    # Iterate through each message in the input messages
    index = 0
    while english_count < limit and index < len(messages):
        message = messages[index]

        # Check if the content of the message is in English
        if is_english(message['content']):
            # If it's English, append it to the list of English messages
            english_messages.append(message)
            english_count += 1

        # Move to the next message
        index += 1

    # Return the list of English messages
    return english_messages


def format_error(key, detail):
    return [{"loc": ["body", key], "msg": detail}]
