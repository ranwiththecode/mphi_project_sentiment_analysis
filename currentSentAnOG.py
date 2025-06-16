import nltk
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import defaultdict
from tqdm import tqdm

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('vader_lexicon')

# Function to identify generic mentions of characters


def identify_generic_characters(text, character_terms):
    mentioned_characters = [term for term in character_terms if term in text]
    return mentioned_characters

# Function to perform sentiment analysis using VADER


def get_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(text)['compound']
    return sentiment_score


# Load the reviews from the file
with open('TheAwakeningOutput.txt', 'r', encoding='utf-8') as file:
    reviews = file.readlines()

# Define the list of main characters (update as needed)
characters = ["Tory"]
generic_terms = ['heroine', 'female protagonist',
                 'female main character', 'protagonist', 'main character', 'MC', 'FMC']

# Combine specific character names and generic terms
character_terms = characters + generic_terms

# Initialize data structures
sentiments = {'Positive': defaultdict(
    int), 'Negative': defaultdict(int), 'Neutral': defaultdict(int)}
mention_count = defaultdict(int)

# Process each review
for review in tqdm(reviews, desc="Processing reviews"):
    sentences = sent_tokenize(review)
    mentioned_characters = identify_generic_characters(review, character_terms)

    if mentioned_characters:
        for character in mentioned_characters:
            # Increment mention count for the character
            mention_count[character] += 1
            sentiment_score = get_sentiment(review)
            if sentiment_score > 0.1:
                sentiments['Positive'][character] += 1
            elif sentiment_score < -0.1:
                sentiments['Negative'][character] += 1
            else:
                sentiments['Neutral'][character] += 1
    else:
        sentiment_score = get_sentiment(review)
        if sentiment_score > 0.1:
            sentiments['Positive']['Other'] += 1
        elif sentiment_score < -0.1:
            sentiments['Negative']['Other'] += 1
        else:
            sentiments['Neutral']['Other'] += 1
        mention_count['Other'] += 1  # Increment mention count for 'Other'

# Print the results
print("Character Reviews Summary:")
for character in sorted(set(character_terms)):
    total_mentions = mention_count[character]
    print(f"{character.title()}:")
    print(f"  Total Mentions: {total_mentions}")
    positive = sentiments['Positive'][character]
    negative = sentiments['Negative'][character]
    neutral = sentiments['Neutral'][character]

    if total_mentions > 0:
        print(f"  Positive: {positive} ({(positive/total_mentions)*100:.2f}%)")
        print(f"  Negative: {negative} ({(negative/total_mentions)*100:.2f}%)")
        print(f"  Neutral: {neutral} ({(neutral/total_mentions)*100:.2f}%)")
    else:
        print(f"  Positive: {positive}")
        print(f"  Negative: {negative}")
        print(f"  Neutral: {neutral}")

# Calculate total sentiment counts across all characters
total_positive = sum(sentiments['Positive'].values())
total_negative = sum(sentiments['Negative'].values())
total_neutral = sum(sentiments['Neutral'].values())

# Calculate the total of all sentiments (Positive + Negative + Neutral)
total_sentiments = total_positive + total_negative + total_neutral

# Calculate percentages for each sentiment type
if total_sentiments > 0:
    positive_percentage = (total_positive / total_sentiments) * 100
    negative_percentage = (total_negative / total_sentiments) * 100
    neutral_percentage = (total_neutral / total_sentiments) * 100
else:
    positive_percentage = negative_percentage = neutral_percentage = 0

# Print total sentiment counts with percentages
print("\nTotal Sentiment Counts Across All Characters:")
print(
    f"  Total Positive Sentiments: {total_positive} ({positive_percentage:.2f}%)")
print(
    f"  Total Negative Sentiments: {total_negative} ({negative_percentage:.2f}%)")
print(
    f"  Total Neutral Sentiments: {total_neutral} ({neutral_percentage:.2f}%)")
print(f"  Total Sentiments (All): {total_sentiments}")
