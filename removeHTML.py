import re
from bs4 import BeautifulSoup
from langdetect import detect, LangDetectException  # type: ignore

# Example dictionary of emojis to text. Add more emojis as needed.
emoji_dict = {
    "😊": ":smiling_face_with_smiling_eyes:",
    "😂": ":face_with_tears_of_joy:",
    "❤️": ":red_heart:",
    "😍": ":smiling_face_with_heart_eyes:",
    "😒": ":unamused_face:",
    "👍": ":thumbs_up:",
    "🙏": ":folded_hands:",
    "💕": ":two_hearts:",
    "😘": ":face_blowing_a_kiss:",
    "😎": ":smiling_face_with_sunglasses:",
    "🤦‍♀️": ":facepalm:",
    "🥶": ":chills:",
    "⭐": ":star:",
    # Add more emojis as required
}


def preprocess_text(text):
    # Check if the text resembles HTML markup
    if re.search(r'<.*?>', text):
        # Remove HTML tags using BeautifulSoup
        soup = BeautifulSoup(text, 'html.parser')
        clean_text = soup.get_text()
    else:
        clean_text = text

    # Convert emojis to text using the dictionary
    for emoji_char, emoji_desc in emoji_dict.items():
        clean_text = clean_text.replace(emoji_char, emoji_desc)

    return clean_text


def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False


def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    preprocessed_lines = []
    for line in lines:
        preprocessed_line = preprocess_text(line)
        if is_english(preprocessed_line):
            preprocessed_lines.append(preprocessed_line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(preprocessed_lines)


# Example usage
input_file_path = 'TheAwakeningOutput.txt'
process_file(input_file_path)

print(f"File '{input_file_path}' has been preprocessed and overwritten.")
