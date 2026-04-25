from datetime import datetime
import random

PRIMARY_GREETINGS = {
    "morning": "Good morning.",
    "afternoon": "Good afternoon.",
    "evening": "Good evening.",
    "night": "You're still up?"
}

MORNING_LINES = [
    "What's the plan for today?",
    "Shall we review the latest global developments?",
    "We can start with a quick intelligence briefing if you like.",
    "Would you like a status update before you begin?",
    "I can pull the latest data while you get started.",
    "Shall we go over anything important before the day unfolds?",
    "If you're ready, we can begin with a quick overview of current events.",
    "Need a quick rundown before you dive in?",
    "I can prepare a briefing while you settle in.",
    "We can start with whatever matters most to you today."
]

AFTERNOON_LINES = [
    "What would you like to focus on next?",
    "Need an update on anything important?",
    "We can pick up where you left off.",
    "Anything you'd like me to analyze?",
    "I can gather updates while you continue working.",
    "Want a quick snapshot of what's happening globally?",
    "We can optimize the rest of your day if needed.",
    "Let me know what requires attention.",
    "I’m ready when you are.",
    "Shall we continue?"
]

EVENING_LINES = [
    "Would you like a summary of today's developments?",
    "We can review what changed throughout the day.",
    "Anything you'd like to wrap up?",
    "I can prepare a closing briefing if needed.",
    "Shall we go over the highlights?",
    "We can analyze today's outcomes if you want.",
    "Let me know if anything still needs attention.",
    "I can give you a quick end-of-day overview.",
    "Ready to wind things down or keep going?",
    "Your call."
]

NIGHT_LINES = [
    "Still working?",
    "Need something before you call it a day?",
    "We can keep things light if you prefer.",
    "I can assist with anything quick.",
    "Let me know what you need.",
    "Not done yet?",
    "I'm here if something requires attention.",
    "We can keep this brief.",
    "Just say the word.",
    "What’s on your mind?"
]

def get_time_period():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"

def generate_greeting():
    period = get_time_period()
    primary = PRIMARY_GREETINGS[period]
    
    if period == "morning":
        secondary = random.choice(MORNING_LINES)
    elif period == "afternoon":
        secondary = random.choice(AFTERNOON_LINES)
    elif period == "evening":
        secondary = random.choice(EVENING_LINES)
    else:
        secondary = random.choice(NIGHT_LINES)
        
    return f"{primary} {secondary}"
