import random

qa = {
    "math": {
        "What is 3/4 + 1/8?": "7/8",
        "Find the value of 6x = 42.": "x = 7",
        "Area of a 9 cm by 4 cm rectangle?": "36 cm²",
        "Convert 0.75 into a fraction.": "3/4",
        "Mean of 5, 10, 15, 20?": "12.5",
        "20% off $50 → sale price?": "$40",
        "Circumference of radius 7 cm (π=3.14)?": "≈ 43.96 cm",
        "Evaluate 2^4.": "16",
        "Triangle with angles 70° and 40° → third angle?": "70°",
        "Quadrant of point (–4, 6)?": "Quadrant II"
    },

    "science": {
        "Physical vs chemical change?": 
            "Physical = no new substance; Chemical = new substance formed.",
        "Why lightning comes before thunder?":
            "Light travels faster than sound.",
        "Function of cell membrane?": "Controls what enters and leaves the cell.",
        "What is kinetic energy?": "Energy of motion.",
        "One renewable and one non-renewable resource?":
            "Renewable: solar; Non-renewable: coal.",
        "Which part of atom has a positive charge?": "Proton.",
        "Example of a simple machine?": "Lever, pulley, wedge, wheel, etc.",
        "What happens to particles when a solid melts?":
            "They move faster and spread apart.",
        "What is photosynthesis?":
            "Process plants use to make food using sunlight.",
        "What force keeps planets orbiting the Sun?": "Gravity."
    },

    "english": {
        "Subject/predicate of 'The tall boy ran quickly.'":
            "Subject: 'The tall boy'; Predicate: 'ran quickly'.",
        "What is a metaphor?":
            "A comparison without using 'like' or 'as'.",
        "Past tense of 'I walk to school every day.'":
            "I walked to school every day.",
        "What is a theme?":
            "The main message or lesson of a story.",
        "Choose correct form: their / there / they're?":
            "'Their' = possession, 'There' = location, 'They're' = they are.",
        "What is an adjective?":
            "A word that describes a noun (example: big, red).",
        "What is the main idea?":
            "The most important point of a paragraph.",
        "Fix the sentence: 'me and jake went to the park.'":
            "'Jake and I went to the park.'",
        "What is a clause?":
            "A group of words with a subject and verb.",
        "Write a sentence using a conjunction.":
            "Example: 'I wanted ice cream, but the store was closed.'"
    },

    "social_studies": {
        "Difference between democracy and dictatorship?":
            "Democracy = people vote; Dictatorship = one leader controls everything.",
        "Name an ancient civilization.": "Egyptians, Greeks, Romans, Maya, etc.",
        "What are natural resources?": "Materials from nature we use.",
        "What is an economy?": "System of producing and exchanging goods.",
        "Why do countries trade?": "They want resources they don't have.",
        "Purpose of the Constitution?":
            "Sets rules for government and citizens.",
        "One effect of colonization?":
            "Loss of land/culture, new trade routes, etc.",
        "What is the equator?":
            "Imaginary line dividing Earth into north and south.",
        "What is a primary source?":
            "First-hand evidence (diary, photo, letter).",
        "What is globalization?":
            "Countries becoming more connected."
    }
}

# ---- QUIZ BOT ----

def ask_question():
    subject = random.choice(list(qa.keys()))
    question = random.choice(list(qa[subject].keys()))
    answer = qa[subject][question]

    print(f"\n Subject: {subject.capitalize()}")
    print(f" Question: {question}")
    print(f" Bot Answer: {answer}")

# Run the bot
while True:
    ask_question()
    if input("\nAnother one? (y/n): ").lower() != "y":
        break

print("\nGoodbye!")