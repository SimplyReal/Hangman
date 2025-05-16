# A fabulous and glamorous version of the classic Hangman game
import random
import sqlite3
from tabulate import tabulate

# 🎀 Word Collections for Each Category
WORD_SETS = {
    "Animals": ["ant", "baboon", "badger", "bat", "bear", "beaver", "camel", "cat", "clam", "cobra"],
    "Shapes": ["square", "triangle", "rectangle", "circle", "ellipse", "rhombus", "trapezoid"],
    "Places": ["Cairo", "London", "Paris", "Baghdad", "Istanbul", "Riyadh"]
}

# 💾 Create or connect to Hall of Fame database
def setup_database():
    conn = sqlite3.connect("hangman_scores.db")
    cur = conn.cursor()

    # Creating HallOfFame table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS HallOfFame (
            level TEXT PRIMARY KEY,
            winner TEXT,
            remaining_lives INTEGER
        )
    """)

    # Insert default rows if empty
    for level in ["Easy", "Moderate", "Hard"]:
        cur.execute("INSERT OR IGNORE INTO HallOfFame VALUES (?, ?, ?)", (level, "-", 0))

    conn.commit()
    conn.close()

# 💅 Display Main Menu with Pretty Formatting
def show_main_menu(player_name):
    print(f"\nHey {player_name} 💖")
    print("Welcome to the Glamorous World of HANGMAN!\n")

    menu = [
        ["1", "Easy Level 🐣"],
        ["2", "Moderate Level ⚡"],
        ["3", "Hard Level 🔥"],
        ["4", "Hall of Fame 🏆"],
        ["5", "About the Game 📖"],
        ["6", "Exit ❌"]
    ]

    print(tabulate(menu, headers=["Option", "Menu"], tablefmt="fancy_grid"))

# 🧠 About the Game
def show_about():
    print("\n📚 About the Game - Super Simple\n")
    description = [
        ["Easy", "Choose category, 8 lives, chill mode 😌"],
        ["Moderate", "Choose category, 6 lives, stay sharp 🔎"],
        ["Hard", "Random word, no clues, 6 lives, bring it on 💪"]
    ]
    print(tabulate(description, headers=["Level", "What Happens"], tablefmt="fancy_grid"))
    print("\nGuess the word one letter at a time. Fewer mistakes = more glory 💅")

# 🌟 View the Hall of Fame
def show_hall_of_fame():
    conn = sqlite3.connect("hangman_scores.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM HallOfFame")
    rows = cur.fetchall()

    print("\n🏆 HALL OF FAME — Legends Only\n")
    print(tabulate(rows, headers=["Level", "Winner", "Lives Left"], tablefmt="fancy_grid"))

    conn.close()

# 🎮 Let the game begin!
def play_game(level, player_name):
    # Determine number of lives and word selection style
    lives = 8 if level == "Easy" else 6
    word = select_secret_word(level).lower()
    guessed = []
    wrong_guesses = 0

    # Display for debugging (you can remove this)
    # print(f"[DEBUG] Secret word: {word}")

    print(f"\n🎲 Level: {level} | Lives: {lives}")
    print("Guess the word, one letter at a time!\n")

    while wrong_guesses < lives:
        # Display current word progress
        display_word = ''.join([letter if letter in guessed else '_' for letter in word])
        print("Word: ", ' '.join(display_word.upper()))
        print(f"Guessed so far: {', '.join(sorted(guessed)) if guessed else 'None'}")
        print(f"Lives left: {lives - wrong_guesses}")

        guess = input("Enter a letter: ").strip().lower()

        if not guess.isalpha() or len(guess) != 1:
            print("🚫 One letter at a time, please.")
            continue

        if guess in guessed:
            print("⚠️ You've already guessed that!")
            continue

        guessed.append(guess)

        if guess in word:
            print("✅ Nice guess!\n")
            if all(letter in guessed for letter in word):
                print(f"\n🎉 YOU WON, {player_name.upper()}! The word was '{word.upper()}'")
                update_hall_of_fame(level, player_name, lives - wrong_guesses)
                return
        else:
            wrong_guesses += 1
            print("❌ Nope! Try again.\n")

    # If loop ends, they lost
    print(f"\n💀 GAME OVER! The word was '{word.upper()}'")

# 🔮 Secret word selection
def select_secret_word(level):
    if level in ["Easy", "Moderate"]:
        set_menu = [["1", "Animals"], ["2", "Shapes"], ["3", "Places"]]
        print(tabulate(set_menu, headers=["Option", "Category"], tablefmt="grid"))
        choice = input("Choose a category (1-3): ").strip()
        selected = {"1": "Animals", "2": "Shapes", "3": "Places"}.get(choice, "Animals")
        return random.choice(WORD_SETS[selected])
    else:
        random_category = random.choice(list(WORD_SETS.keys()))
        return random.choice(WORD_SETS[random_category])

# 🏆 Update Hall of Fame if score is better
def update_hall_of_fame(level, player_name, score):
    conn = sqlite3.connect("hangman_scores.db")
    cur = conn.cursor()
    cur.execute("SELECT remaining_lives FROM HallOfFame WHERE level=?", (level,))
    current_high = cur.fetchone()[0]

    if score > current_high:
        cur.execute("UPDATE HallOfFame SET winner=?, remaining_lives=? WHERE level=?",
                    (player_name, score, level))
        conn.commit()
        print("🌟 New Hall of Fame record! You're iconic 👑")
    else:
        print("You did great! But didn’t beat the top score. Keep shining ✨")

    conn.close()



# 👑 Start Here
def main():
    setup_database()
    player_name = input("Enter your name, superstar: ").strip().title()

    while True:
        show_main_menu(player_name)
        choice = input("\nChoose your vibe (1-6): ").strip()

        if choice == "1":
            play_game("Easy", player_name)
        elif choice == "2":
            play_game("Moderate", player_name)
        elif choice == "3":
            play_game("Hard", player_name)
        elif choice == "4":
            show_hall_of_fame()
        elif choice == "5":
            show_about()
        elif choice == "6":
            print("Bye gorgeous 👋 See you soon!")
            break
        else:
            print("Hmm, invalid option. Try again 💁")


if __name__ == "__main__":
    main()
    