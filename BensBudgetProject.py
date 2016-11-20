"""
This is my first attempt at a real Python program. The purpose of this program is to:
(1) learn how to code hands-on with Python,
(2) have a project that I can show off in interviews,
(3) possibly practice incorporating machine learning principles.

This program will be a budgeting program, inspired by YNAB. It's componants shall include:
(1) A list of budget categories (and subcategories), created by the user
(2) A way to add/delete/edit budget categories
(3) A list of transactions, entered by the user
(4) A way to add/delete/edit transactions
(5) A summary of weekly/monthly/annual statistics and trends
(6) Machine learning tool that makes suggestions to the user regarding how they should change their spending habits in order to:
    a. Pay down debt
    b. Increase their savings/investment contributions
    c. Anticipate upcoming expenses, using the user's history as the training set
(7) A measure of cash available to be budgeted
(8) For each budget category, there should be an attribute for the budgeted amount assigned to that category.

I expect this to be rough, and not something that people would want to pay money for. However, it needs to be:
COMPLETE    (Must create a minimum viable product, even if missing desirable features)
WORKING,    (One should be able to track their budgeting with this)
EFFICIENT,  (The algorithms should be fast and elegant), and
CLEAN       (The code should be readable, concise, and make sense).

Let's dive in and see what happens!
"""

#__________________________________________________________________________________________________#
#I guess we need to make categories themselves into a data structure. Let's use a class.

class Categories(object):
    def __init__(self, name, budget_value):
        self.name = name
        self.budget_value = budget_value


#__________________________________________________________________________________________________#
#Next, the transactions. This should also probably be a class.

class Transactions(object):
    def __init__(self, date, payee, category, memo, amount):
        self.date = date
        self.payee = payee
        self.category = category
        self.memo = memo
        self.amount = amount

#__________________________________________________________________________________________________#
def display_categories():

    if len(my_categories) == 0:
        print("\nYou have no categories! You should make some!")
    else:
        print("Here are your categories:")

        for i in range(len(my_categories)):
            print("\t%s" % my_categories[i].name)

#__________________________________________________________________________________________________#
def new_category():
    #This function is called whenever the user wants to create a new budget category.
    #First, ask the user what the category's name should be.
    name = input("What do you want to call your new category? ")

    print("Okay! You added a new category called %s to your list!" % name)
    
    #Then, create an instance of Category class and assign the name as an attribute.
    #Return this instance.
    return Categories(name, 0)

#__________________________________________________________________________________________________#
def reciteMenuOptions(listOfOptions):

    print("\nWhat would you like to do?")
    
    for i in range(len(listOfOptions)):
        print("Press %d to %s" % (i+1, listOfOptions[i]))

    #The value in userInput will be a string
    userInput = int(input("Enter your choice here: "))
        #Once the Try...Except block is implemented, use the following statement instead of the above:
        #   userInput = input("Enter your choice here: ")

    #This is where error detection/correction should happen
    #Use a Try...Except block to test if the input can converted to an int type



    #Now that we've successfully converted the input into an int type, make sure it is in the right range.
    #That is, make sure it is in the set {i+1} for i in range(len(listOfOptions))


    #Finally, return userInput.
    return userInput

#__________________________________________________________________________________________________#
def menu_for_categories():

    CATEGORY_MENU_OPTIONS = ["see your list of budget categories,",
                             "add a new category,",
                             "return to the main menu."
                             ]

    print("\n~~You are now in the categories menu.~~")

    while True:

        choice = reciteMenuOptions(CATEGORY_MENU_OPTIONS)

        if choice == 1:
            display_categories()
    
        elif choice == 2:
            my_categories.append(new_category())
    
        elif choice == 3:
            break

#__________________________________________________________________________________________________#
def menu_for_transactions():
    pass






#__________________________________________________________________________________________________#
def save_file_menu():
    

    """
    What should the flowchart look like here? As a user, what do I want to have happen here?
    1) Be given a choice to either save in a brand new file (case 1), or to save over an existing file (case 2)
    2) In the first case, the user must enter the file name
        -No need to enter the file extension (.txt)
        -The user should be told the current working directory and see the full path
        -The user should be able to change the directory
    3) In the second case, the user needs to see a list of existing .txt files
        -The user should be told the current working directory and see the full path
        -The user should be able to change the directory
    4) Either way, once the file and path have been selected, do the actual file saving
        -In case 1, create a new file and save all data to it
        -In case 2, overwrite an existing file and then save current data to it
    5) Inform the user that the save was successful
    6) Return the user back to the main menu


    """

    returnToPrimarySaveMenu = True
    OVERWRITE_OPTIONS = []
    SAVE_MENU_OPTIONS = ["save the current state as a brand new budget,",
                         "save the current state by overwriting an existing budget,",
                         "cancel this save and return to the main menu."
                         ]

    print("\n~~Time to save your budget data!~~")

    #Loop back up to here.
    while returnToPrimarySaveMenu == True:
        returnToPrimarySaveMenu = False
        
        choice = reciteMenuOptions(SAVE_MENU_OPTIONS)

        if choice == 1:
            print("\nThe current working directory is:\n\t%s" % os.getcwd())
            choice2 = input("Would you like to save your budget here (Y) or elsewhere (N)? ").upper()
            #Need to confirm that choice2 is a member of {Y, y, N, n}

            if choice2 == 'Y':
                print("\nCool, it\'ll be saved to the current working directory.")
                dirname = input("Please choose a name for your budget directory: ")
                #How to verify that user has entered a valid filename? Can't contain '/' or ':' (I think)
                #Use a Try...Except block here, rather than anticipating all possible user errors.

                #Verify whether there is an existing directory with the same name and path
                if os.path.isdir(os.path.join(os.getcwd(), dirname)) == True:
                    
                    print("\nUmmmmm that directory already exists. Awko Taco!")
                    choice3 = input("Do you want to overwrite it (Y) or pick a new location/name (N)? ").upper()
                    #Again, need to confirm that choice3 is a member of {Y, y, N, n}

                    if choice3 == 'Y':
                        the_actual_file_saving_code(os.path.join(os.getcwd(), dirname))

                    elif choice3 == 'N':
                        returnToPrimarySaveMenu = True

                else:
                    the_actual_file_saving_code(os.path.join(os.getcwd(), dirname))
     
            elif choice2 == 'N':
                #Ask the user what directory he wants to save it to.
                #Once a directory has been selected, then prompt for the budget directory name (consider making this part its own function).
                pass
            



        elif choice == 2:
            #Present the user with the list of budgets (from the INITIALIZE.txt file)
            #Also provide an option to cancel this decision

            existingBudgets = readExistingBudgetsIntoPresentableList()

            if existingBudgets == None:
                returnToPrimarySaveMenu = True
            else:
                print("\nWhich budget would you like to save over?")
                OVERWRITE_OPTIONS.clear()
                for i in range(len(existingBudgets)):
                    OVERWRITE_OPTIONS.append("save over %s," % existingBudgets[i])
                OVERWRITE_OPTIONS.append("cancel this decision and return to the save menu.")
                
                choice4 = reciteMenuOptions(OVERWRITE_OPTIONS)

                #Since the cancel option is last, its number will be equal to the length of OVERWRITE_OPTIONS.
                if choice4 == len(OVERWRITE_OPTIONS):
                    #redirect the user to the top of this function
                    returnToPrimarySaveMenu = True
                else:
                    #We want to go to the selected budget directory and replace the old contents with the current state.
                    #This means deleting the old budget directory, and then saving to that same location.
                    #There will be no need to make any change to INITIALIZE.txt
                    the_actual_file_saving_code(existingBudgets[choice4 - 1])

        elif choice == 3:
            #No additional code needed here!
            pass

#__________________________________________________________________________________________________#
def the_actual_file_saving_code(full_path_and_directory_name):

    #First create a new directory using the name provided by the user, unless it already exists.
    try:
        os.makedirs(full_path_and_directory_name)
    except FileExistsError:
        #Directory already exists, no action required.
        pass
    else:
        #This code block only executes when a new directory is successfully created.
        #Save the full path and directory name to our fixed INITIALIZE.TXT file.
        #NOTE: The path to INITIALIZE.TXT should work for anyone, not just my specific hard-coded path below.
        with open('/Users/Benjamin/Documents/PythonPrograms/BudgetProject/BudgetRepo/INITIALIZE.TXT', mode = 'a', encoding = 'utf-8') as file1:
            file1.write("%s\n" % full_path_and_directory_name) 

    #Now save all data to the directory...
    os.chdir(full_path_and_directory_name)
    with open('savedCategories.txt', mode = 'w', encoding = 'utf-8') as file2:
        for cat in my_categories:
            file2.write("%s\n" % cat.name)

    print("\nOkay! Your budget data has been saved to:\n\t%s" % full_path_and_directory_name)

#__________________________________________________________________________________________________#
def load_file():
    #The user should be asked which budget directory to load from.
    #This means the user needs to be presented with a list of previously-saved budgets.

    #Okay so...
    #First,search for pre-existing text file containing budget names and paths
    #Then read the names to the user.
    #When the user selects a name, navigate to the path (using dictionaries?)
    #At the end of the path will be a budget folder containing two text files (categories and transactions)
    #Then the program should load both the budget categories and transactions.
    
    #Open INITIALIZE.TXT in read mode
    #Use a for loop to save each line of the file into a list.
    #WE CAN'T USE os.path.split to grab the directory name because it only works for file names at the end of the path!
    #Somehow we isolate the final directory, which the user created in a previous session. Use dictionaries here?
    #Enter these directory names into LOAD_MENU_OPTIONS
    #Use as argument for reciteMenuOptions()
    #Based on the user's choice, navigate to the appropriate budget directory
    #Load categories into my_cateogires!


    LOAD_MENU_OPTIONS = []
        
    existingBudgets = readExistingBudgetsIntoPresentableList()

    if existingBudgets == None:
        pass
    else:
        print("\n~~Please choose which budget you want to load.~~")
        #Now make each member of LOAD_MENU_OPTIONS say "load $$$" where $$$ is the user-created name from a previous instance.
        for i in range(len(existingBudgets)):
            LOAD_MENU_OPTIONS.append("load %s," % existingBudgets[i])
        #ADD AN OPTION TO CANCEL THIS DECISION AND RETURN TO THE MAIN MENU
        LOAD_MENU_OPTIONS.append("cancel this decision and return to the main menu.")
            
        choice = reciteMenuOptions(LOAD_MENU_OPTIONS)

        if choice == len(LOAD_MENU_OPTIONS):
            #redirect user back to the main menu.
            pass
        else:
            my_categories.clear()
            with open(os.path.join(existingBudgets[choice-1], 'savedCategories.txt'), mode = 'r', encoding = 'utf-8') as f:
                while True:
                    temporary2 = f.readline()
                    if temporary2 == '':
                        break
                    else:
                        my_categories.append(Categories(temporary2.strip(),0))
            
            print("\nYour budget has been loaded!")

#__________________________________________________________________________________________________#
def readExistingBudgetsIntoPresentableList():
    #All this function does is reads INITIALIZE.txt into a list (line by line), check for empty case, and then clean up names and returns list.
    #That is, it returns a list called Initialize_contents_display.
    #If there are no saved budgets, it returns None.

    Initialize_contents = []
    #Initialize_contents_display is a list which is identical to Initialize_contents except that it looks presentable.
    Initialize_contents_display = []

    #Read each line from the INITIALIZE.TXT file into the list Initialize_contents
    with open('/Users/Benjamin/Documents/PythonPrograms/BudgetProject/BudgetRepo/INITIALIZE.TXT', mode = 'r', encoding = 'utf-8') as file:
        while True:
            temporary = file.readline()
            if temporary == '':
                break
            else:
                Initialize_contents.append(temporary)
                
    if len(Initialize_contents) == 0:
        print("\nThere doesn't appear to be any existing budgets.")
        #At this point we want to immediately return to the main menu!
        return None
        
    else:
        #Now remove the newline characters (\n) from the end of each member of Initialize_contents
        #???Also remove the path (except for the final directory, which the user created in a previous instance.???
        for j in range(len(Initialize_contents)):
            Initialize_contents_display.append(Initialize_contents[j].strip())

        return Initialize_contents_display



    
######################################   START OF PROGRAM   ########################################

#Here is where I import all modules:
import os

#Here are all the CONSTANTS and Global Variables:
my_categories = []
MAIN_MENU_OPTIONS = ["go to the category menu,",
                     "go to the transactions menu,",
                     "save your current budget,",
                     "load an existing budget,",
                     "quit the program."
                     ]
    

#Here is where the user experience begins:
print("Welcome to my budget program!")

while True:

    choice = reciteMenuOptions(MAIN_MENU_OPTIONS)
    
    if choice == 1:
        menu_for_categories()
    
    elif choice == 2:
        menu_for_transactions()

    elif choice == 3:
        save_file_menu()

    elif choice == 4:
        load_file()
        
    elif choice == 5:
        break
        
    print("\n~~You are now returning to the main menu.~~")
          
print("See you later!")

#######################################   END OF PROGRAM   #########################################


"""
Here are ideas of next steps and features:
-Currently there is nothing stopping a user from saving a new budget within an existing budget's directory.
    -Ideally we would not want to allow this!
-Add a Delete Existing Budget option to the main menu.
-Implement some sense of time. Consider making the time frame variable, based on user input.
-Expand the display_categories() function to show more than just the category names. Ideas for expansion include:
    -Showing a table with category names as rows, and other attributes (such as budget_value) as columns.
    -Similar to YNAB, show total transctions for the given time period.
-Build out the transactions section of the program.
-Build out error checking whenever the user enters information
    -One for the menus; integers in range(len(...)) are expected
    -Another for new categories/transactions; strings are expected
-Consider making a function that prompts the user "Press enter to continue" and doesn't continue until they do.
    -Call this function everytime they enter some input (after the immediate results of their input is shown to them.
    -For example:
        -the program prompts them for a menu item,
        -they enter a number,
        -the program tells them what the immediate result of their input is,
        -the program calls this press_enter_to_continue function
-Python does not have a switch statement, so the current use of if/elif/else will have to do.
-Allow users to create their own subsets of categories (distinct from the idea of supercategories).
    -Allow users to see spending patterns/trends in just that subset.


*As an aside, consider putting this whole project on Dropbox, and try running it using the PythonAnywhere website as the shell.
    https://www.pythonanywhere.com/try-ipython/
    On second thought, this probably won't work because the shell may not be able to see the .py files...

"""
