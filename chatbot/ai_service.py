import google.generativeai as genai
from math import sqrt
from datetime import datetime
import json
# Configure with your API key
genai.configure(api_key='AIzaSyDWlTipxEyfR1Zu4F8JNC7GhMzb3VrQekw')

# Create model instance
model = genai.GenerativeModel('gemini-2.5-flash')

def calculate_base_temperature(dass21):
    depression = dass21.depression_score
    anxiety = dass21.anxiety_score
    stress = dass21.stress_score
    # max based scoring for extreme cases
    if depression >= 28 or anxiety >= 20 or stress >= 34:
        return 7
    if depression >= 21 or anxiety >= 15 or stress >= 26:
        return 5
    
    # based on Euclidean distance
    norm_dep = depression / 42
    norm_anx = anxiety / 42
    norm_str = stress / 42
    raw_dist = sqrt(norm_dep**2 + norm_anx**2 + norm_str**2)
    return round((raw_dist / sqrt(3)) * 10, 1)

def analyze_message_distress(user_message):
    """
    Use Gemini to analyze distress level in message
    Returns: dict with distress_score (0-10), summary, and reasoning
    """
    
    analysis_prompt = """Analyze this message from a mental health perspective.

Message: "{message}"

Provide a JSON response with:
1. Distress_score: 0-10 scale
   - 0-2: Positive/neutral mood, no concerns
   - 3-4: Mild stress or everyday worries
   - 5-6: Moderate distress, notable concern
   - 7-8: Severe distress, significant concern
   - 9-10: Crisis level, immediate danger signals

2. Dndicators: List of specific distress indicators found (hopelessness, isolation, crisis language, etc.)

3. Summary: One-sentence summary of the message (max 15 words)

4. Reasoning: Brief explanation of the score (2-3 sentences)

Focus on:
- Hopelessness, helplessness
- Isolation, loneliness
- Self-harm or suicidal ideation
- Severe anxiety or panic
- Loss of meaning/purpose
- Emotional numbness

Example response:
{{
  "distress_score": 7,
  "indicators": ["hopelessness", "isolation", "loss of purpose"],
  "summary": "Feeling alone and questioning life's meaning",
  "reasoning": "Message expresses feeling disconnected and purposeless, which are significant warning signs for depression."
}}

Respond only with the JSON object, no other text.""".format(message=user_message)
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(analysis_prompt)
        
        # Remove markdown code blocks if present
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:-3]
        elif text.startswith('```'):
            text = text[3:-3]
        
        analysis = json.loads(text)
        
        return {
            'distress_score': analysis.get('distress_score', 5),
            'indicators': analysis.get('indicators', []),
            'summary': analysis.get('summary', user_message[:50]),
            'reasoning': analysis.get('reasoning', '')
        }
        
    except Exception as e:
        # Fallback: use keyword-based approach
        distress_score = calculate_distress_score(user_message)
        
        return {
            'distress_score': distress_score,
            'indicators': 'none',
            'summary': user_message,
            'reasoning': 'none'
        }
    
def calculate_distress_score(message):
    """
    Calculate distress score based on keywords and patterns
    Returns: float 0-10
    """
    message_lower = message.lower()
    
    # Crisis indicators (heavy weight)
    crisis_keywords = {
        'suicide': 10, 'kill myself': 10, 'end it all': 10,
        'want to die': 10, 'better off dead': 10,
        'no point': 9, 'can\'t go on': 9, 'give up': 8
    }
    
    # Severe distress indicators
    severe_keywords = {
        'hopeless': 8, 'worthless': 8, 'meaningless': 8,
        'can\'t take it': 7, 'breaking down': 7, 'falling apart': 7,
        'nothing matters': 8, 'numb': 7, 'empty inside': 7
    }
    
    # Self-harm indicators
    selfharm_keywords = {
        'cut myself': 9, 'hurt myself': 8, 'self-harm': 8,
        'harm myself': 8, 'injure myself': 8
    }
    
    # Moderate distress
    moderate_keywords = {
        'overwhelmed': 6, 'drowning': 6, 'can\'t cope': 6,
        'struggling': 5, 'exhausted': 5, 'scared': 5,
        'anxious': 5, 'panic': 6, 'terrified': 7
    }
    
    # Mild stress (normal)
    mild_keywords = {
        'stressed': 3, 'worried': 3, 'nervous': 3,
        'tired': 2, 'busy': 2, 'pressure': 3
    }
    
    # Positive indicators (reduce score)
    positive_keywords = {
        'better': -2, 'improving': -2, 'hopeful': -3,
        'grateful': -2, 'happy': -2, 'excited': -1
    }
    
    # Calculate base score
    max_score = 0
    matched_keywords = []
    
    # Check all keyword categories
    all_keywords = {
        **crisis_keywords,
        **severe_keywords, 
        **selfharm_keywords,
        **moderate_keywords,
        **mild_keywords,
        **positive_keywords
    }
    
    for keyword, score in all_keywords.items():
        if keyword in message_lower:
            max_score = max(max_score, score) if score > 0 else max_score
            if score > 0:
                matched_keywords.append(keyword)
            elif score < 0 and max_score > 0:
                max_score = max(0, max_score + score)
    
    # Negation detection ("not hopeless" vs "hopeless")
    if any(neg in message_lower for neg in ['not ', "don't ", 'never ']):
        # Check if negation is near high-severity keywords
        for keyword in matched_keywords:
            if f"not {keyword}" in message_lower or f"don't feel {keyword}" in message_lower:
                max_score = max(0, max_score - 2)
    
    # Multiple distress indicators = compound effect
    if len(matched_keywords) >= 3:
        max_score = min(10, max_score + 1)
    
    # Very short messages expressing crisis
    if len(message.split()) <= 5 and max_score >= 8:
        max_score = min(10, max_score + 1)
    
    # Question marks might indicate uncertainty/seeking help
    if '?' in message and max_score >= 5:
        max_score = max(4, max_score - 1)  # Slight reduction
    
    return round(max_score, 1)

def generate_summary(message, max_words=15):
    """Use heuristics to summarize a message."""
    stopwords = {'the', 'a', 'an', 'that', 'those'}

    words = message.split()
    if len(words) <= max_words:
        return message

    # Remove trivial words 
    filtered = [w for w in words if w.lower() not in stopwords]

    # If filtering makes it too short, fall back to slicing
    if len(filtered) < max_words:
        filtered = words

    return ' '.join(filtered[:max_words]) + '...'
 
def detect_crisis_keywords(message):
    """Fast keyword check for immediate crisis"""
    crisis_phrases = [ 'kms', 'smash my head', 'kill me'
        'kill myself', 'want to die', 'wanna die', 'suicide', 'end it all',
        'better off dead', 'no reason to live', 'take my life'
    ]
    message_lower = message.lower()
    return any(phrase in message_lower for phrase in crisis_phrases)

# def process_user_message(user, message_text, conversation_history):
#     """
#     Complete message processing pipeline
#     Returns: processed_data dict
#     """
    
#     # STAGE 1: Crisis Detection (immediate)
#     crisis_flag = detect_crisis_keywords(message_text)
    
#     if crisis_flag:
#         # Immediate severe protocol
#         processed_data = {
#             'timestamp': datetime.now(),
#             'original_text': message_text,
#             'summary': generate_summary(message_text),
#             'crisis_detected': True,
#             'distress_score': 10,
#             'sentiment_indicators': ['crisis_language'],
#             'immediate_action': 'SEVERE_PROTOCOL'
#         }
        
#         # Store immediately
#         store_message(user, processed_data)
        
#         return processed_data
    
#     # STAGE 2: Distress Analysis (AI-powered)
#     analysis = analyze_message_distress(message_text)
#     distress_score = analysis['distress_score']
    
#     conversation_history = ChatMessage.objects.filter(user=user).order_by('-timestamp')[:5]
#     dass21 = DASS21Result.objects.filter(user=user).latest('-date')
#     base_temp = calculate_base_temperature(dass21)
    
#     temperature = calculate_current_temperature(
#         base_temp=base_temp,
#         current_distress=distress_score,
#         conversation_history=conversation_history
#     )
#     processed_data = {
#         'timestamp': datetime.now(),
#         'original_text': message_text,
#         'summary': analysis['summary'],
#         'crisis_detected': analysis['distress_score'] >= 9,
#         'distress_score': analysis['distress_score'],
#         'sentiment_indicators': analysis.get('indicators', []),
#         'immediate_action': determine_action(analysis['distress_score'])
#     }
    
#     # Store for history
#     store_message(user, processed_data)
    
#     return processed_data

# def determine_action(distress_score):
#     """Map distress score to action protocol"""
#     if distress_score >= 9:
#         return 'SEVERE_PROTOCOL'
#     elif distress_score >= 7:
#         return 'MODERATE_PROTOCOL'
#     elif distress_score >= 4:
#         return 'MILD_SUPPORT'
#     else:
#         return 'NORMAL_CONVERSATION'

# def store_message(user, processed_data):
#     ChatMessage.objects.create(
#         user=user,
#         message=processed_data['original_text'],
#         summary=processed_data['summary'],
#         timestamp=processed_data['timestamp'],
#         crisis_flag=processed_data['crisis_detected'],
#         distress_score=processed_data['distress_score'],
#         # Store indicators as JSON
#         metadata=json.dumps({
#             'indicators': processed_data['sentiment_indicators'],
#             'action': processed_data['immediate_action']
#         })
#     )

def process_user_message(user, message_text):
    """
    Complete message processing pipeline
    Returns: processed_data dict with distress score, action, and metadata
    """
    
    # STAGE 1: Quick Crisis Detection
    crisis_flag = detect_crisis_keywords(message_text)
    
    if crisis_flag:
        return _handle_crisis_message(user, message_text)
    
    # STAGE 2: AI Distress Analysis
    analysis = analyze_message_distress(message_text)
    
    # STAGE 3: Build processed data
    processed_data = {
        'timestamp': datetime.now(),
        'original_text': message_text,
        'summary': analysis['summary'],
        'crisis_detected': analysis['distress_score'] >= 9,
        'distress_score': analysis['distress_score'],
        'indicators': analysis.get('indicators', []),
        'immediate_action': determine_action(analysis['distress_score'])
    }
    
    # Store message
    store_message(user, processed_data)
    
    return processed_data


def _handle_crisis_message(user, message_text):
    """
    Handle detected crisis - fast path
    """
    processed_data = {
        'timestamp': datetime.now(),
        'original_text': message_text,
        'summary': generate_summary(message_text),
        'crisis_detected': True,
        'distress_score': 10,
        'indicators': ['crisis_language'],
        'immediate_action': 'SEVERE_PROTOCOL'
    }
    
    store_message(user, processed_data)
    return processed_data

def determine_action(distress_score):
    if distress_score >= 9:
        return 'SEVERE_PROTOCOL'
    elif distress_score >= 7:
        return 'MODERATE_PROTOCOL'
    elif distress_score >= 4:
        return 'MILD_SUPPORT'
    else:
        return 'NORMAL_CONVERSATION'

def store_message(user, processed_data):
    """Store message in database"""
    ChatMessage.objects.create(
        user=user,
        message=processed_data['original_text'],
        summary=processed_data['summary'],
        timestamp=processed_data['timestamp'],
        crisis_flag=processed_data['crisis_detected'],
        distress_score=processed_data['distress_score'],
        metadata=json.dumps({
            'indicators': processed_data['indicators'],
            'action': processed_data['immediate_action']
        })
    )


def calculate_temperature_for_user(user, current_distress):
    """
    Calculate temperature based on user's history and current distress
    Separate function - called when generating response, not during message processing
    """
    # Get conversation history
    conversation_history = ChatMessage.objects.filter(user=user).order_by('-timestamp')[:10]
    
    # Get baseline from DASS-21
    try:
        dass21 = DASS21Result.objects.filter(user=user).latest('test_date')
        base_temp = calculate_base_temperature(
            dass21.depression_score,
            dass21.anxiety_score,
            dass21.stress_score
        )
    except DASS21Result.DoesNotExist:
        base_temp = 5.0  # Default if no test taken
    
    # Calculate current temperature
    temperature = calculate_current_temperature(
        base_temp=base_temp,
        current_distress=current_distress,
        conversation_history=conversation_history
    )
    
    return temperature

def handle_chat_request(user, message_text):
    """
    Main chat handler
    """
    
    # 1. Process incoming message
    processed = process_user_message(user, message_text)
    
    # 2. Calculate temperature for response generation
    temperature = calculate_temperature_for_user(user, processed['distress_score'])
    
    # 3. Generate system prompt
    system_prompt = generate_system_prompt(
        user.userprofile,
        temperature
    )
    
    # 4. Execute action based on distress
    if processed['immediate_action'] == 'SEVERE_PROTOCOL':
        response = handle_severe_protocol(user, message_text, system_prompt)
    elif processed['immediate_action'] == 'MODERATE_PROTOCOL':
        response = handle_moderate_protocol(user, message_text, system_prompt)
    else:
        response = generate_normal_response(user, message_text, system_prompt)
    
    # 5. Store response with temperature
    ChatMessage.objects.filter(
        user=user,
        message=message_text
    ).update(
        response=response,
        temperature=temperature
    )
    
    return {
        'response': response,
        'action': processed['immediate_action'],
        'temperature': temperature
    }
    
def calculate_current_temperature(base_temp, current_distress, conversation_history):
    if not conversation_history:
        return base_temp
    BASE_WEIGHT = 0.5       # DASS-21 baseline (stable foundation)
    RECENT_WEIGHT = 0.3     # Last 5-10 messages (medium-term trend)
    CURRENT_WEIGHT = 0.2    # Current message (immediate signal)
    
    recent_messages = conversation_history[-5:]
    recent_scores = (msg.distress_score for msg in recent_messages)
    weighted_recent = []
    
    for i, score in enumerate(reversed(recent_scores)):
        # more recent messages -> higher weights (0.5 -> 1.0)
        weight = 0.5 + (i / len(recent_messages)) * 0.5 
        weighted_recent.append(score * weight)
    avg_recent_score = sum(weighted_recent) / sum([0.5 + (i / len(recent_scores)) * 0.5 for i in range(len(recent_scores))])

    temperature = (
        base_temp * BASE_WEIGHT +
        avg_recent_score * RECENT_WEIGHT +
        current_distress * CURRENT_WEIGHT
    )
    return round(min(10, max(0, temperature)), 1)

def generate_system_prompt(user_profile, latest_dass21, current_temperature):
    
    # Base personality and boundaries
    base_prompt = """You are a compassionate mental health support assistant for university students. 

    CORE PRINCIPLES:
    - Be warm, empathetic, and non-judgmental
    - Use a calm, therapeutic tone
    - Validate feelings without being patronizing
    - Ask open-ended questions to encourage expression
    - NEVER provide medical advice, diagnoses, or prescribe treatments
    - NEVER claim to be a replacement for professional therapy
    - Encourage professional help when appropriate

    BOUNDARIES:
    - If asked for diagnosis: "I can't diagnose conditions, but I can listen and help you find professional resources"
    - If asked for medication advice: "Medication decisions should be made with a healthcare provider. I can help you explore other coping strategies"
    - If asked about serious medical symptoms: "This sounds like something to discuss with a doctor or counselor"
    """

    # Personalization based on DASS-21
    dass_context = ""
    if latest_dass21:
        depression = latest_dass21.depression_level
        anxiety = latest_dass21.anxiety_level
        stress = latest_dass21.stress_level
        
        dass_context = f"""
    Current user context (from recent mental health assessment):
    - Depression level: {depression}
    - Anxiety level: {anxiety}  
    - Stress level: {stress}

    """
        # Adjust tone based on severity
        if depression in ['Severe', 'Extremely Severe'] or anxiety in ['Severe', 'Extremely Severe'] or stress in ['Severe', 'Extremely Severe']:
            dass_context += """Be extra gentle and supportive. This person may be struggling significantly. Watch for crisis language and be prepared to offer immediate resources if needed.
    """
        elif depression == 'Moderate' or anxiety == 'Moderate':
            dass_context += """Be proactive in checking in. This person is experiencing notable distress and may benefit from encouragement to seek support. 
    """
    
    # Temperature-based guidance
    temp_guidance = ""
    if current_temperature >= 7:
        temp_guidance = """
ALERT: This conversation shows signs of distress or crisis. Priority actions:
1. Express genuine concern and empathy
2. Listen without judgment
3. Ask if they're currently safe
4. Gently offer crisis resources (hotlines, emergency contacts)
5. Encourage reaching out to someone they trust
6. DO NOT try to "solve" the crisis - focus on support and connection to help
"""
    elif current_temperature >= 4:
        temp_guidance = """
This person is experiencing moderate distress. Be extra attentive:
- Check in more frequently about how they're feeling
- Offer specific coping strategies (breathing exercises, grounding techniques)
- Validate their struggles
- Suggest helpful resources proactively
"""
    
    # Additional user context
    user_context = f"""
    User information:
    - Name: {user_profile.user.username or 'None'}
    - Gender: {user_profile.gender or 'None'}
    - University: {user_profile.university or 'None'}
    - Year of study: {user_profile.year_of_study or '0'}
    - Phone: {user_profile.phone or '0'}
    - Emergency contact: {user_profile.emergency_contact or 'None'}
    - Emergency contact name: {user_profile.emergency_contact_name or 'None'}
    - Has previous counseling: {'Yes' if user_profile.has_previous_counseling else 'No'}
    - Currently in therapy: {'Yes' if user_profile.is_currently_in_therapy else 'No'}
    """
    
    if user_profile.is_currently_in_therapy:
        user_context += "\nNote: They're already working with a therapist. Support their ongoing therapy and encourage communication with their therapist about concerns.\n"
    
    # Combine all sections
    full_prompt = base_prompt + dass_context + temp_guidance + user_context
    
    return full_prompt

def generate_chat_response(request):
    user = request.user

    # 1. Load profile
    user_profile = UserProfile.objects.get(user=user)

    # 2. Load latest DASS-21
    latest_dass21 = (
        DASS21Result.objects
        .filter(user=user)
        .order_by('-date')
        .first()
    )

    # 3. Load your conversation temperature from DB or in-memory
    current_temperature = conversation.temperature  

    # 4. Build system prompt
    system_prompt, _ = generate_system_prompt(
        user_profile, 
        latest_dass21, 
        current_temperature
    )

    # 5. Pass it to Gemini
    response = model.generate_content(system_prompt, user_message)

    return JsonResponse({"response": response})


# Generate response
response = model.generate_content('Hello, how are you?')
print(response.text)