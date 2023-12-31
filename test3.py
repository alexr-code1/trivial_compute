import pygame
import speech_recognition as sr

# Initialize pygame
pygame.init()

# Set up the display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Trivial Compute")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define board layout
board_layout = [
    [WHITE, RED, WHITE, RED, WHITE, RED, WHITE, RED, WHITE],
    [BLUE, WHITE, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE, BLUE],
    [WHITE, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE],
    [RED, WHITE, RED, WHITE, RED, WHITE, RED, WHITE, RED],
    [WHITE, RED, WHITE, RED, WHITE, RED, WHITE, RED, WHITE],
    [BLUE, WHITE, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE, BLUE],
    [WHITE, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE],
    [RED, WHITE, RED, WHITE, RED, WHITE, RED, WHITE, RED],
    [WHITE, RED, WHITE, RED, WHITE, RED, WHITE, RED, WHITE]
]

# Define player colors and names
player_colors = [GREEN, YELLOW, BLUE, RED]
player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]

num_players = 4

# Define category names
category_names = ["Category 1", "Category 2", "Category 3", "Category 4"]
current_player = 0
players = [(0, 0), (1, 0), (0, 1), (1, 1)]

# Define question window dimensions and other variables
question_window_width = 600
question_window_height = 400
question_window_x = (width - question_window_width) // 2
question_window_y = (height - question_window_height) // 2
recognizer = sr.Recognizer()

# Define question state
question_displayed = False
question_answered = False
question_correct = False
user_answer = ""

# Store the questions, answers, and media files
questions = []
answers = []
media_files = []

# Function to add a true/false question
def add_true_false_question(question, answer):
    questions.append(question)
    answers.append(answer)

# Function to add a multiple-choice question
def add_multiple_choice_question(question, choices, answer):
    formatted_question = question + " [" + "/".join(choices) + "]"
    questions.append(formatted_question)
    answers.append(answer)

# Function to add a multimedia question
def add_multimedia_question(question, media_file):
    questions.append(question)
    answers.append(None)
    media_files.append(media_file)

def question_interface():
    print("======= Question Interface =======")
    print("1. Add True/False Question")
    print("2. Add Multiple Choice Question")
    print("3. Add Multimedia Question")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        question = input("Enter the true/false question: ")
        answer = input("Enter the answer (True/False): ")
        add_true_false_question(question, answer)
        print("Question added successfully!")
    elif choice == "2":
        question = input("Enter the multiple-choice question: ")
        choices = input("Enter the choices (separated by commas): ").split(",")
        answer = input("Enter the answer (choice number): ")
        add_multiple_choice_question(question, choices, answer)
        print("Question added successfully!")
    elif choice == "3":
        question = input("Enter the multimedia question: ")
        media_file = input("Enter the path to the media file: ")
        add_multimedia_question(question, media_file)
        print("Question added successfully!")
    elif choice == "4":
        return
    else:
        print("Invalid choice. Please try again.")

    # Recursively call the question_interface function
    question_interface()

# Call the question_interface function to start adding questions
question_interface()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if question_displayed and not question_answered:
                    try:
                        with sr.Microphone() as source:
                            print("Listening...")
                            audio = recognizer.listen(source)
                            user_answer = recognizer.recognize_google(audio)
                            print("You said:", user_answer)
                            # Process the answer (check if it's correct, update game state, etc.)
                            if user_answer.lower() == answers[current_question].lower():
                                question_correct = True
                                current_player_score += 1
                            else:
                                # Move to the next player's turn
                                current_player = (current_player + 1) % num_players
                    except sr.UnknownValueError:
                        print("Sorry, I could not understand your answer.")
                    except sr.RequestError:
                        print("Sorry, speech recognition service is unavailable.")
                elif question_displayed and question_answered:
                    question_correct = True if input("Was the answer correct? (y/n): ").lower() == 'y' else False
                    if question_correct:
                        current_player_score += 1
                    else:
                        # Move to the next player's turn
                        current_player = (current_player + 1) % num_players
                elif not question_displayed and not question_answered:
                    question_displayed = True
                    # Display the question and options
                    question_text = font.render("Question: " + questions[current_question], True, BLACK)
                    screen.blit(question_text, (question_window_x + 10, question_window_y + 10))

                    # Display the options
                    options_text = []
                    for i, option in enumerate(options[current_question]):
                        text = f"{i+1}. {option}"
                        options_text.append(text)

                    for i, text in enumerate(options_text):
                        option_text = font.render(text, True, BLACK)
                        screen.blit(option_text, (question_window_x + 10, question_window_y + 50 + i * 30))

    # Draw the board
    for row in range(9):
        for col in range(9):
            pygame.draw.rect(screen, board_layout[row][col], (col * 80, row * 80, 80, 80))

    # Draw player tokens
    for player in range(num_players):
        pygame.draw.circle(screen, player_colors[player], (players[player][0] * 80 + 40, players[player][1] * 80 + 40), 30)

    # Draw current player indicator
    pygame.draw.circle(screen, player_colors[current_player], (10, 10), 10)

    # Draw question window
    if question_displayed:
        pygame.draw.rect(screen, WHITE, (question_window_x, question_window_y, question_window_width, question_window_height))
        # Display the question and options
        question_text = font.render("Question: " + questions[current_question], True, BLACK)
        screen.blit(question_text, (question_window_x + 10, question_window_y + 10))

        options_text = []
        for i, option in enumerate(options[current_question]):
            text = f"{i+1}. {option}"
            options_text.append(text)

        for i, text in enumerate(options_text):
            option_text = font.render(text, True, BLACK)
            screen.blit(option_text, (question_window_x + 10, question_window_y + 50 + i * 30))

    pygame.display.flip()

# Quit the game
pygame.quit()
