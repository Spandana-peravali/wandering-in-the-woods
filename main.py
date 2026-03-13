from mode_35 import run_35
# from mode_k2 import run_k2
# from mode_68 import run_68


def main():
    while True:
        print("\n=== Wandering in the Woods ===")
        # print("1. Grades K–2")
        print("2. Grades 3–5")
        # print("3. Grades 6–8")
        print("4. Exit")

        choice = input("Select level (2-4): ")

        if choice == "2":
            run_35()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again!")


if __name__ == "__main__":
    main()
