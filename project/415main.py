import sys
from sequentialAlgorithm import *
from dataProcess import *

def main():
    #选择跑哪个function
    #菜单
    print("Welcome!")
    print("This is Cpts415 group 2 project")
    print("Main Menu")
    print("----------")
    print("1: Simple sequential sql")
    print("2: BBB")
    print("3: CCC")
    print("4: AAA")
    print("5: Exit")
    print("----------")

    user_option = input("What do you want to do?")
    if user_option == '1':
        print("----------Simple sequential sql-----------")                 # function 1
        user_file = input("Please print the file name you want to work with:")
        user_M = input("How many value do you want to get?")
        user_conditions = input("Please give me the conditions you want:")
        user_select = input("Which attribute do you want to work with?")

        sqAlg1(user_file, user_M, user_conditions, user_select)
    if user_option == '2':
        print("Hello")              # function 2
    if user_option == '3':
        print("Whats up")           # function 3
    if user_option == '4':
        print("Sup")                # function 4
    if user_option == '5':
        print("Okay bye")
        sys.exit()                  # exit





if __name__ == '__main__':
    main()
