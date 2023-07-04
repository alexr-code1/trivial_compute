# Function to display the question interface
def question_interface():
    print("======= Question Interface =======")
    print("1. Add True/False Question")
    print("2. Add Multiple Choice Question")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")

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
        return
    else:
        print("Invalid choice. Please try again.")

    # Recursively call the question_interface function
    question_interface()

# Call the question_interface function to start adding questions
question_interface()
