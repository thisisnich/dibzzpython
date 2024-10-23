def get_int(question="enter an integer"):
    """
    loops input statement until a valid integer is given
    """
    while True:
        ans = input(question)
        if ans.isdigit():
            ans = int(ans)
            break
        
    return ans


def menu(options, question="Please choose an option"):
    """
    Displays a menu based on the input list of options and prompts the user to select one.

    :param options: List of menu options to display.
    :return: A number from 0 to len(options) - 1 based on the user's selection.
    """
    print(question)
    for i, option in enumerate(options):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input(f"Enter a number (0 to {len(options) - 1}): "))
            if 0 <= choice < len(options):
                return choice
            else:
                print(f"Invalid choice. Please enter a number between 0 and {len(options) - 1}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """
    Main function that generates the menu, processes user input, and displays the selected option.
    """
    options_list = ["Start Game", "Options", "Help", "Exit"]

    # Display the menu and get the user's choice
    choice = menu(options_list)

    # Handle the choice (this is where you'd add your program logic)
    print(f"You selected {choice}: {options_list[choice]}")

    # Optional: You can add more logic based on the user's choice
    if choice == len(options_list) - 1:  # If "Exit" is selected
        print("Exiting the program...")

# This block ensures that the `main` function runs if the script is executed directly
if __name__ == "__main__":
    main()
