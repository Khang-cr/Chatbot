import google.generativeai as genai

# Configure with your API key
genai.configure(api_key='AIzaSyDWlTipxEyfR1Zu4F8JNC7GhMzb3VrQekw')

# Create model instance
model = genai.GenerativeModel('gemini-2.5-flash')

# Generate response
response = model.generate_content('Hello, how are you?')
print(response.text)