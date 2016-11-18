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

    SAVE_MENU_OPTIONS = ["save the current state as a brand new budget,",
                         "save the current state by overwriting an existing budget,",
                         "cancel this save and return to the main menu."
                         ]

    print("\n~~Time to save your budget data!~~")
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
            #if os.path.isfile(os.path.join(os.getcwd(), filename)) == True:
            if os.path.isdir(os.path.join(os.getcwd(), dirname)) == True:
                
                print("\nUmmmmm that directory already exists. Awko Taco!")
                choice3 = input("Do you want to overwrite it (Y) or pick a new directory/filename (N)? ").upper()
                #Again, need to confirm that choice3 is a member of {Y, y, N, n}

                if choice3 == 'Y':
                    the_actual_file_saving_code(os.getcwd(), dirname)

                elif choice3 == 'N':
                    #Loop back and ask user to enter specifications again, including the directory.
                    #The top of the loop should be inside the "choice == 1" block
                    pass

            else:
                the_actual_file_saving_code(os.getcwd(), dirname)
 

        elif choice2 == 'N':
            #Ask the user what directory he wants to save it to.
            #Once a directory has been selected, then prompt for the budget directory name (consider making this part its own function).
            pass
        

    elif choice == 2:
        #Need to present the user with a list of existing budget directories.
        #Start by presenting all .txt files in the CWD and ask if the desired file is there.
        #If so, then confirm that the user wants to save over that file. If so, then save over it!
        #If not, then ask the user to enter the directory that contains the file he has in mind.
        #Present all .txt files in this new directory and ask if the desired file is there.
        #Loop as necessary until the user chooses a file.
        #Also, provide the user with a CANCEL option at all times, should he decide that he doesn't want to
        pass

    elif choice == 3:
        #This part is finished!
        pass

#__________________________________________________________________________________________________#
def the_actual_file_saving_code(path, directory_name):
    
    full_path_and_directory_name = os.path.join(path, directory_name)

    #Save the full path and directory name to our fixed INITIALIZE.TXT file.
    #NOTE: The path to INITIALIZE.TXT should work for anyone, not just my specific hard-coded path below.
    with open('/Users/Benjamin/Documents/PythonPrograms/BudgetProject/BudgetRepo/INITIALIZE.TXT', mode = 'a', encoding = 'utf-8') as file1:
        file1.write("%s\n" % full_path_and_directory_name) 

    #Next create a new directory using the name provided by the user, if necessary
    os.makedirs(full_path_and_directory_name)
    #NOTE: IF THIS DIRECTORY ALREADY EXISTS, THE PROGRAM WILL THROW AN EXCEPTION HERE!!!
    #Probbaly can be quickly solved using a Try...Except block

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

    #NEW IDEA! When the program first launches, it should pull a list of previously-saved budget names from a text-file at
    #a previously determined fixed location. This means that every time you save a budget, the full path and the user-created
    #name will be saved to this fixed text-file.

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


    Initialize_contents = []
    #Initialize_contents_display is a list which is identical to Initialize_contents except that it looks presentable.
    Initialize_contents_display = []
    LOAD_MENU_OPTIONS = []
    my_categories.clear()

    #Read each line from the INITIALIZE.TXT file into the list Initialize_contents
    with open('/Users/Benjamin/Documents/PythonPrograms/BudgetProject/BudgetRepo/INITIALIZE.TXT', mode = 'r', encoding = 'utf-8') as file:
        while True:
            temporary = file.readline()
            if temporary == '':
                break
            else:
                Initialize_contents.append(temporary)
                
    if len(Initialize_contents) == 0:
        print("\nThere doesn't appear to be any existing budgets...Why don't you make one?")
        #At this point we want to immediately return to the main menu!
        
    else:
        print("\n~~You need to choose which budget you want to load.~~")

        #Now remove the newline characters (\n) from the end of each member of Initialize_contents
        #???Also remove the path (except for the final directory, which the user created in a previous instance.???
        for j in range(len(Initialize_contents)):
            Initialize_contents_display.append(Initialize_contents[j].strip())
        
        #Now make each member of LOAD_MENU_OPTIONS say "load $$$" where $$$ is the user-created name from a previous instance.
        for i in range(len(Initialize_contents_display)):
            LOAD_MENU_OPTIONS.append("load %s," % Initialize_contents_display[i])
            
        choice = reciteMenuOptions(LOAD_MENU_OPTIONS)           
            
        with open(os.path.join(Initialize_contents_display[choice-1], 'savedCategories.txt'), mode = 'r', encoding = 'utf-8') as f:
            while True:
                temporary2 = f.readline()
                if temporary2 == '':
                    break
                else:
                    my_categories.append(Categories(temporary2.strip(),0))
        

        print("\nYour budget has been loaded!")



    
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
-Save the list of budget categories to a text file, and load them the next time the user runs the program.
    -Add a Save option and a Load option to the main menu?
    -I think that any saved data for a single budget should be packaged in a single directory.
        -Within that directory there can be separate text files: one for categories, one for transactions, etc.
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
