from deep_translator import GoogleTranslator

def tamil_to_english(tamil_text):
    try:
        translator = GoogleTranslator(source='ta', target='en')  # 'ta' for Tamil, 'en' for English
        english_text = translator.translate(tamil_text)
        return english_text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

if __name__ == "__main__":
    # Test the function with a sample Tamil text
    test_text = "வணக்கம்"
    result = tamil_to_english(test_text)
    print(f"Translated English text: {result}")  # Should print "Hello"