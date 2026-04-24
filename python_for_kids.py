"""
🐍 Python Adventure for Kids! 🎮
A fun, interactive way to learn Python basics!
"""

import time
import random
import sys

# Color codes for fun terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_slow(text, delay=0.03):
    """Print text with a typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_colorful(text, color):
    """Print colorful text"""
    print(f"{color}{text}{Colors.RESET}")

def welcome():
    """Welcome screen"""
    print_colorful("\n" + "="*60, Colors.CYAN)
    print_colorful("🐍  WELCOME TO PYTHON ADVENTURE FOR KIDS!  🐍", Colors.YELLOW)
    print_colorful("="*60, Colors.CYAN)
    print()
    print_slow("🎮 Get ready to learn Python in a fun way!")
    print_slow("🌟 Let's go on a coding adventure!\n")

def quiz_question(question, options, correct_answer, explanation):
    """Ask a quiz question"""
    print_colorful(f"\n❓ {question}", Colors.BLUE)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    while True:
        try:
            answer = int(input("\nYour answer (1-4): "))
            if 1 <= answer <= 4:
                break
            print("Please choose a number between 1 and 4!")
        except ValueError:
            print("Oops! Please enter a number!")
    
    if answer == correct_answer:
        print_colorful("✅ CORRECT! Great job! 🎉", Colors.GREEN)
        print(f"💡 {explanation}")
        return True
    else:
        print_colorful("❌ Not quite! Let's learn!", Colors.RED)
        print(f"💡 The correct answer was {correct_answer}: {options[correct_answer-1]}")
        print(f"   {explanation}")
        return False

def variables_game():
    """Learn about variables"""
    print_colorful("\n" + "="*60, Colors.PURPLE)
    print_colorful("📦 LEVEL 1: VARIABLES - The Magic Boxes!", Colors.PURPLE)
    print_colorful("="*60, Colors.PURPLE)
    
    print_slow("\nImagine variables are like magic boxes where you can store things!")
    print_slow("You can put numbers, words, or even lists inside them!\n")
    
    # Interactive example
    print_colorful("\n✨ Let's create some variables together!", Colors.CYAN)
    name = input("What's your name? ")
    age = input("How old are you? ")
    favorite_color = input("What's your favorite color? ")
    
    print_slow(f"\n🎉 Awesome! Now let's see what we stored:")
    print(f"  👤 Name: {name}")
    print(f"  🎂 Age: {age}")
    print(f"  🎨 Favorite Color: {favorite_color}")
    
    print_slow("\n💡 In Python, we write it like this:")
    print_colorful(f"""
    name = "{name}"
    age = {age}
    favorite_color = "{favorite_color}"
    """, Colors.GREEN)
    
    # Quiz
    score = 0
    questions = [
        {
            "question": "What is a variable in Python?",
            "options": [
                "A type of snake",
                "A box to store data",
                "A math operation",
                "A kind of loop"
            ],
            "correct": 2,
            "explanation": "Variables are like containers that store data values!"
        },
        {
            "question": "Which is the correct way to create a variable?",
            "options": [
                "variable: 5",
                "5 = my_var",
                "my_var = 5",
                "create my_var as 5"
            ],
            "correct": 3,
            "explanation": "In Python, we write: variable_name = value"
        }
    ]
    
    for q in questions:
        if quiz_question(q["question"], q["options"], q["correct"], q["explanation"]):
            score += 1
    
    return score

def data_types_game():
    """Learn about data types"""
    print_colorful("\n" + "="*60, Colors.YELLOW)
    print_colorful("🔢 LEVEL 2: DATA TYPES - Different Kinds of Data!", Colors.YELLOW)
    print_colorful("="*60, Colors.YELLOW)
    
    print_slow("\nPython has different types of data, just like different types of toys!")
    print_slow("Let's meet them:\n")
    
    print_colorful("1️⃣  Strings (str) - Text in quotes", Colors.CYAN)
    print_colorful('   Example: "Hello", "Python", "🐍"', Colors.GREEN)
    
    print_colorful("\n2️⃣  Integers (int) - Whole numbers", Colors.CYAN)
    print_colorful("   Example: 5, 10, 100, -3", Colors.GREEN)
    
    print_colorful("\n3️⃣  Floats (float) - Decimal numbers", Colors.CYAN)
    print_colorful("   Example: 3.14, 2.5, 0.1", Colors.GREEN)
    
    print_colorful("\n4️⃣  Booleans (bool) - True or False", Colors.CYAN)
    print_colorful("   Example: True, False", Colors.GREEN)
    
    # Interactive game
    print_colorful("\n🎯 Let's play: Guess the Data Type!", Colors.PURPLE)
    
    examples = [
        ('"Hello World"', "str"),
        ("42", "int"),
        ("3.14", "float"),
        ("True", "bool"),
        ('"123"', "str"),
        ("-10", "int"),
    ]
    
    score = 0
    random.shuffle(examples)
    
    for value, actual_type in examples[:4]:
        print_colorful(f"\nWhat type is: {value} ?", Colors.BLUE)
        print("  1. str (text)")
        print("  2. int (whole number)")
        print("  3. float (decimal)")
        print("  4. bool (True/False)")
        
        guess = input("Your guess (1-4): ")
        type_map = {"1": "str", "2": "int", "3": "float", "4": "bool"}
        
        if type_map.get(guess) == actual_type:
            print_colorful("✅ Correct! 🎉", Colors.GREEN)
            score += 1
        else:
            print_colorful(f"❌ It's actually {actual_type}!", Colors.RED)
    
    return score

def loops_game():
    """Learn about loops"""
    print_colorful("\n" + "="*60, Colors.GREEN)
    print_colorful("🔄 LEVEL 3: LOOPS - Doing Things Again and Again!", Colors.GREEN)
    print_colorful("="*60, Colors.GREEN)
    
    print_slow("\nLoops help us repeat things without writing the same code over and over!")
    print_slow("It's like telling Python: 'Do this 5 times!' 🔄\n")
    
    print_colorful("✨ Two main types of loops:", Colors.CYAN)
    print_colorful("  1. for loops - Loop through items", Colors.YELLOW)
    print_colorful("  2. while loops - Loop while condition is true", Colors.YELLOW)
    
    # Visual example
    print_colorful("\n🎪 Let's see a for loop in action!", Colors.PURPLE)
    print_slow("\nCounting from 1 to 5:")
    
    for i in range(1, 6):
        print(f"  {'🎈' * i} {i}")
        time.sleep(0.3)
    
    print_colorful("\n\nCode that made this happen:", Colors.CYAN)
    print_colorful("""
    for i in range(1, 6):
        print("🎈" * i, i)
    """, Colors.GREEN)
    
    # Quiz
    score = 0
    questions = [
        {
            "question": "What does a 'for' loop do?",
            "options": [
                "Stops the program",
                "Repeats code for each item in a sequence",
                "Creates a variable",
                "Deletes data"
            ],
            "correct": 2,
            "explanation": "For loops iterate through sequences like lists or ranges!"
        },
        {
            "question": "How many times will this run: for i in range(3)?",
            "options": [
                "2 times",
                "3 times (0, 1, 2)",
                "4 times",
                "1 time"
            ],
            "correct": 2,
            "explanation": "range(3) gives us 0, 1, 2 - that's 3 iterations!"
        }
    ]
    
    for q in questions:
        if quiz_question(q["question"], q["options"], q["correct"], q["explanation"]):
            score += 1
    
    return score

def functions_game():
    """Learn about functions"""
    print_colorful("\n" + "="*60, Colors.RED)
    print_colorful("⚙️  LEVEL 4: FUNCTIONS - Your Code Superpowers!", Colors.RED)
    print_colorful("="*60, Colors.RED)
    
    print_slow("\nFunctions are like reusable spells in Python! 🪄")
    print_slow("You define them once and use them whenever you need!")
    
    print_colorful("\n✨ Why use functions?", Colors.CYAN)
    print("  ✅ Reuse code without copying")
    print("  ✅ Make code organized")
    print("  ✅ Easy to fix bugs")
    print("  ✅ Share with friends!")
    
    # Example function
    print_colorful("\n🎯 Let's create a greeting function!", Colors.PURPLE)
    
    def greet(name):
        return f"🌟 Hello, {name}! Welcome to Python! 🐍"
    
    name = input("Enter your name to test the function: ")
    print_colorful(f"\n{greet(name)}", Colors.GREEN)
    
    print_colorful("\nHere's the code:", Colors.CYAN)
    print_colorful("""
    def greet(name):
        return f"🌟 Hello, {name}! Welcome to Python! 🐍"
    
    greet("Alex")
    """, Colors.GREEN)
    
    # Quiz
    score = 0
    questions = [
        {
            "question": "What keyword is used to create a function?",
            "options": [
                "func",
                "define",
                "def",
                "function"
            ],
            "correct": 3,
            "explanation": "We use 'def' to define functions in Python!"
        },
        {
            "question": "What does a function return if no return statement is used?",
            "options": [
                "0",
                "None",
                "Error",
                "Empty string"
            ],
            "correct": 2,
            "explanation": "Functions return None by default if no return is specified!"
        }
    ]
    
    for q in questions:
        if quiz_question(q["question"], q["options"], q["correct"], q["explanation"]):
            score += 1
    
    return score

def final_challenge():
    """Final challenge combining all concepts"""
    print_colorful("\n" + "="*60, Colors.BOLD)
    print_colorful("🏆 FINAL CHALLENGE - Show What You've Learned!", Colors.YELLOW)
    print_colorful("="*60, Colors.BOLD)
    
    print_slow("\nTime to put it all together! Let's create a simple program!")
    
    print_colorful("\n📝 Challenge: Create a number guessing game!", Colors.PURPLE)
    
    print_slow("\nHere's how it works:")
    print("  1. Computer picks a random number")
    print("  2. You guess the number")
    print("  3. Computer tells you if you're right!")
    
    secret_number = random.randint(1, 10)
    attempts = 0
    
    while True:
        try:
            guess = int(input("\nGuess a number between 1 and 10: "))
            attempts += 1
            
            if guess == secret_number:
                print_colorful(f"🎉 YES! You got it in {attempts} tries!", Colors.GREEN)
                break
            elif guess < secret_number:
                print_colorful("📈 Too low! Try again!", Colors.YELLOW)
            else:
                print_colorful("📉 Too high! Try again!", Colors.YELLOW)
        except ValueError:
            print("Please enter a valid number!")
    
    print_colorful("\n💻 Here's the code that made this game:", Colors.CYAN)
    print_colorful("""
    import random
    
    secret_number = random.randint(1, 10)
    attempts = 0
    
    while True:
        guess = int(input("Guess: "))
        attempts += 1
        
        if guess == secret_number:
            print(f"You won in {attempts} tries!")
            break
        elif guess < secret_number:
            print("Too low!")
        else:
            print("Too high!")
    """, Colors.GREEN)
    
    return 3  # Bonus points for completing the challenge

def certificate(name, total_score):
    """Generate a completion certificate"""
    print_colorful("\n" + "="*60, Colors.BOLD)
    print_colorful("🎓 CERTIFICATE OF COMPLETION 🎓", Colors.YELLOW)
    print_colorular("="*60, Colors.BOLD)
    
    print(f"""
    {Colors.CYAN}╔══════════════════════════════════════════════════╗{Colors.RESET}
    {Colors.CYAN}║                                                  ║{Colors.RESET}
    {Colors.YELLOW}║          PYTHON ADVENTURE GRADUATE!            ║{Colors.RESET}
    {Colors.CYAN}║                                                  ║{Colors.RESET}
    {Colors.GREEN}║  This certifies that                             ║{Colors.RESET}
    {Colors.GREEN}║                                                  ║{Colors.RESET}
    {Colors.BOLD}║      {name:<40}  ║{Colors.RESET}
    {Colors.GREEN}║                                                  ║{Colors.RESET}
    {Colors.GREEN}║  Has successfully completed the                  ║{Colors.RESET}
    {Colors.GREEN}║  Python Adventure for Kids!                      ║{Colors.RESET}
    {Colors.CYAN}║                                                  ║{Colors.RESET}
    {Colors.PURPLE}║  Score: {total_score}/15 ⭐                              ║{Colors.RESET}
    {Colors.CYAN}║                                                  ║{Colors.RESET}
    {Colors.YELLOW}║  Keep coding and have fun! 🐍🎮                ║{Colors.RESET}
    {Colors.CYAN}║                                                  ║{Colors.RESET}
    {Colors.CYAN}╚══════════════════════════════════════════════════╝{Colors.RESET}
    """)

def main():
    """Main game flow"""
    welcome()
    
    name = input("What should we call you, young coder? ")
    print_colorful(f"\n🌟 Great to meet you, {name}! Let's start our adventure!", Colors.GREEN)
    
    total_score = 0
    
    # Level 1: Variables
    print_colorful("\n\n🚀 Starting Level 1...", Colors.CYAN)
    time.sleep(1)
    total_score += variables_game()
    
    # Level 2: Data Types
    print_colorful("\n\n🚀 Starting Level 2...", Colors.CYAN)
    time.sleep(1)
    total_score += data_types_game()
    
    # Level 3: Loops
    print_colorful("\n\n🚀 Starting Level 3...", Colors.CYAN)
    time.sleep(1)
    total_score += loops_game()
    
    # Level 4: Functions
    print_colorful("\n\n🚀 Starting Level 4...", Colors.CYAN)
    time.sleep(1)
    total_score += functions_game()
    
    # Final Challenge
    print_colorful("\n\n🚀 Starting Final Challenge...", Colors.CYAN)
    time.sleep(1)
    total_score += final_challenge()
    
    # Certificate
    certificate(name, total_score)
    
    # Final message
    print_colorful("\n\n🎉 Congratulations on completing Python Adventure! 🎉", Colors.YELLOW)
    print_slow("\nRemember:")
    print("  💡 Practice makes perfect!")
    print("  💡 Don't be afraid to make mistakes!")
    print("  💡 Coding is about creativity!")
    print("  💡 Have fun and keep exploring! 🚀")
    
    print_colorful("\n🐍 Happy Coding! 🐍\n", Colors.GREEN)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colorful("\n\n👋 Thanks for playing! Come back soon!", Colors.YELLOW)
        print()
