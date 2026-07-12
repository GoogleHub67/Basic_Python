# memory = {}

# print("Welcome to LearningAI!")

# while True:
#     msg = input("You: ").lower()

#     if msg in memory:
#         print("AI:", memory[msg])
#     else:
#         print("AI: I don't know how to answer that.")
#         ans = input("Teach me the correct answer: ")
#         memory[msg] = ans
#         print("AI: Got it! I learned something new.")

#     if msg == "bye":
#         print("AI: Goodbye!")
#         break


import json

# Load memory from file (or start fresh)
try:
    with open("ai_memory.json", "r") as f:
        memory = json.load(f)
except FileNotFoundError:
    memory = {}

print("Welcome to LearningAI! (Memory saved forever)")

while True:
    msg = input("You: ").lower().strip()
    
    if not msg:
        print("AI: Please type something!")
        continue
        
    if msg in memory:
        print("AI:", memory[msg])
    else:
        print("AI: I don't know how to answer that.")
        ans = input("Teach me the correct answer: ")
        memory[msg] = ans
        print("AI: Got it! I learned something new!")
        
        # Save immediately after learning
        with open("ai_memory.json", "w") as f:
            json.dump(memory, f)

    if msg == "bye":
        print("AI: Goodbye!")
        # Final save before exit
        with open("ai_memory.json", "w") as f:
            json.dump(memory, f)
        break
