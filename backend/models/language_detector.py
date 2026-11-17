
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


# 1. Training dataset

sentences = [
    # English
    "Hello how are you",
    "I am learning artificial intelligence",
    "Natural language processing is interesting",
    "Machine learning is powerful",
    "How can I improve my English",
    "I love programming and technology",
    "This is a language detection project",
    "Artificial intelligence is the future",

    # Hindi
    "मुझे हिंदी सीखनी है",
    "आप कैसे हैं",
    "मेरा नाम महेश है",
    "मुझे कृत्रिम बुद्धिमत्ता पसंद है",
    "आज मौसम बहुत अच्छा है",
    "मैं मशीन लर्निंग सीख रहा हूं",
    "यह एक भाषा पहचान प्रणाली है",
    "मुझे कंप्यूटर विज्ञान पसंद है",

    # Telugu
    "నాకు తెలుగు నేర్చుకోవాలి",
    "మీరు ఎలా ఉన్నారు",
    "నా పేరు మహేష్",
    "నాకు కృత్రిమ మేధస్సు ఇష్టం",
    "ఈ రోజు వాతావరణం బాగుంది",
    "నేను మెషిన్ లెర్నింగ్ నేర్చుకుంటున్నాను",
    "ఇది భాష గుర్తింపు వ్యవస్థ",
    "నాకు కంప్యూటర్ సైన్స్ ఇష్టం",

    # Gujarati
    "મારે ગુજરાતી શીખવું છે",
    "તમે કેમ છો",
    "મારું નામ મહેશ છે",
    "મને કૃત્રિમ બુદ્ધિ ગમે છે",
    "આજે હવામાન સારું છે",
    "હું મશીન લર્નિંગ શીખું છું",
    "આ એક ભાષા ઓળખવાની સિસ્ટમ છે",
    "મને કમ્પ્યુટર વિજ્ઞાન ગમે છે"
]


# 2. Assign language labels

labels = (
    ["English"] * 8 +
    ["Hindi"] * 8 +
    ["Telugu"] * 8 +
    ["Gujarati"] * 8
)


# 3. Convert sentences into character N-grams

vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(2, 5)
)

X = vectorizer.fit_transform(sentences)


# 4. Train the Naive Bayes classifier

model = MultinomialNB()
model.fit(X, labels)


# 5. Language detection function

def detect_language(text):

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)

    return prediction[0]


# 6. Test the model

if __name__ == "__main__":

    test_sentences = [
        "Hello, how are you?",
        "मुझे हिंदी सीखनी है",
        "నాకు తెలుగు తెలుసు",
        "મારે ગુજરાતી શીખવું છે"
    ]

    print("\n===== BHASHA AI LANGUAGE DETECTOR =====")

    for sentence in test_sentences:

        language = detect_language(sentence)

        print("\nInput:", sentence)
        print("Detected Language:", language)
        print("-" * 45)
