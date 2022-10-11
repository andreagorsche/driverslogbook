Welcome to the drivers logbook,

the software logs and retrieves travel data of car drivers for accounting purposes. No matter if a private car is also used for business or a business car is also used for private purposes, a detailed documentation is required. This software is a fast and simple alternative to the tedious task of handwritten documentation in a manual drivers logbook.

![Manual drivers logbook sample](/images/logbook_sample.jpg)

## Target Group: Who is the software 'drivers logbook' for?
The software was written for approximately 5.1 million car drivers in Austria. This current limitation is due to the number plate check and the calculation of the state subvention for business rides according to Austrian law. 
The software was written in a way that it can be easily extended to further countries' usage, like e.g. Ireland, US or Germany. 
The only adaptions needed would be:
* additional variables for the number plate check with according RegEx criteria of the specific country (e.g. defining the format of Irish or German number plates)
* exchange of the Austrian state subvention constant for the country-specific subvention - or if such a subvention doesn't exist in the users country, simply disable the state subvention calculation
Since Germany has similar regulations on business trips by car, the Germans would be the logical next choice for implementation. This would add up the total number of potential users to 53.6 million (48.5 for Germany and 5.1 for Austria). 

## Features: What does the software 'drivers logbook' do?
The software initially welcomes the users and gives them 2 options:
* enter new data
* retrieve existing data (from a Google spreadsheet where the entered data was saved to)

### Entering new data
When choosing to enter new data, the user is asked to enter the following information:
* number plate
* initial mileage (total mileage before the trip, in kilometers)
* current mileage (total mileage after the trip, in kilometers)
* date of the trip
* starting point and destination
* purpose of the trip (business or private)

The list of data is then entered into a Google spreadsheet that`s connected to the software through gspread.

### Retrieving existing data
When choosing to retrieve existing data, the user is asked to enter the following information:
*number plate the user wants to get information about
*year the user wants to get information about

The data is filtered according to the entered user data. The filtered data is then used to calculate the following information:
*driven private kilometers in the requested year
*driven business kilometrs in the requested year
*state subvention the driver can claim from the state for the driven business kilometers

### Main Strengths
A main strength of the software is its data validation. It checks each user input for format requirements and plausibility.
* number plate check: based on the defined RegEx formats the number plates are check for validity. In Austria there are two possible formats that are both considered in this software.
* initial mileage: The software checks if the initial mileage is an integer and if its value is not below 0 or higher than 200000 kilometers. Because a negative mileage does not make sense and a total mileage higher than 200000 is rare. In both cases a faulty data entry is assumed (e.g. due to a typo).
* current mileage: The software checks if the current mileage is an integer and if its value is not below 0 or higher than 1500 kilometers. Because a negative mileage does not make sense and driving more than 1500 kilometers a day is unlikely. In both cases a faulty data entry is assumed (e.g. due to a typo).
* travel date: The validation check of the travel date makes sure that the day is a value between 1 and 31, the month is a value between 1 and 12, the year is a value between 2016 and 2022 (because in accounting the last 7 business are relevant) 
* starting point and destination: RegEx is used to define a minimum and maximum number of characters for the starting point and destination entry. This way it is avoid that other irrelevant string data is entered.
* travel purpose: When entering travel purpose only 2 inputs are allowed: private or business. This is checked in the data validaton.

Another strength of the progam is that the stored data is used to gain new and relevant information for the user. Using a car for different purposes calls for an overview. This is guaranteed through the status report consisting of the sum private and business kilometers driven. Furthermore, the state subvention calculation gives the user additional important information out of the entered data. Otherwise these sums and subvention would have to be calculated manually and this would be much more daunting and time-consuming than using this simple and straight forward software.

### Possible future applications
The software drivers logbook could gain even more relevance with additional future features, like:
* more number plate formats of other countries
* additional input options for special driver groups that need logbooks too, like e.g. truck drivers
* additional inputs and calculations for driver training e.g. for (driving schools) 
* additional inputs and calculations for racing (e.g. go-carting, racing training)

## Data Model
The software is connected to the Google sheet document drivers logbook. In order to save the input data provided by the user, the list of data is stored in the spreadsheet logbook. Each ride consists of a set of data which is entered as a new row. So each row equals a new ride.
When retrieving data the user is asked for the number plate and the year. The relevant data is filtered and used for the calculation of total private kilometers, total business kilometers and state subvention.

### Connecting APIS with Python
As basis for the software a Google sheets document was created. The headings of the columns equal the data entry required by the software user.
In order to connect the software with the spreadsheet, APIs for Google drive and Google sheets were created and integrated in the Python code according to the sample walkthrough project "Love Sandwiches" by Code Institute.

## Testing
### Manual Testing
I tested the code of "drivers logbook" extensively regarding wrong data input. In detail I tested the following scenarios:
* Entering various wrong number plates (not enough numbers, not enough letters, not the right order, too short in characters, too long in characters)
* entering strings were ints were required
* entering ints were strings were required
* with the initial and current mileage I entered too high and too low values
* ignoring date conventions (e.g. entering 2023/13/32)
* when certain data entry was required (like e.g. e or r for enter or retrieval, or private or business) I on purpose entered wrong data.

### Automated Testing
Since the recommended website PEP8online was down at the time of testing, I checked if pycodestyle is installed with my Gitpod and it was. I worked through the probems and got rid of all the indentation issues (mainly spaces missing between functions, 80 characters per line etc.).
At the time of final check ups there were 8 problems remaining - 3 connected to the gitpod.yml file, 4 connected to the variable name 'df' (a standard name used in pandas) and a "Missing module docstring" which (according to web research doesn't need to be resolved by all means.) There were no errors left just warnings and information. Thus, it was decided to hand the project in, in this current state.

### Bugs
With each written function the debugging took place right away to avoid cross-functional errors. The key functionalities of the software that cost the most attention and trials where:
* RegEx for number plate validation
* Validation and change of data type for entered date
* Handling nested lists with the collected input
* Filtering relevant data rows from the dataframe

#### RegEx for number plate validation
The use of RegEx was recommended by my mentor. The major challenge during the development process was to define the order of the letters and numbers needed (2 plate versions). At the same time it was needed to restrict the total amount of characters to 6 or 7 characters. This challenge required a bit of research. The solution was presented by stackoverflow (https://stackoverflow.com/questions/11197549/regular-expression-limit-string-size).

#### Validation of date format and change of date data type
The date input was the biggest challenge of all the inputs in this software. First, the datetime import was used but the change to an integer format proofed to be tricky. Intensive research on the web showed that timestamp is usually used for current date and time display. Since the software was not working with the date of today but rather with the date input of the user. What was needed, were integers that were within a certain range (days of a month being between 1 and 31 etc.). Thus, the decision was to not use datetime and instead focus on checking the range of entered integers.

#### Handling nested lists with the collected input
After having all the input data, the function 'take_data_input()' creates a list of all the data input. This list is then saved in the Google spreadsheet. Since the date input is a list of integers (year, month, day), a nested list was created. After looking through solutions with for loops and list comprehensions my mentor presented the most simply solution: using the asterisk to create flatten the lists and therefore get the data transfered to the Google spreadsheet with out further issues.

#### Filtering relevant data rows from the dataframe
The created data structure in the Google spreadsheet equals a 2-dimensional matrix. Filtering relevant data rows from the dataframe proved to be a bit challenging at the beginning. Especially because there needed to be 3 requirements met in order for the data row to be relevant. It required some trial and error. Some additional reading on the webpages of W3 schools and statology was very helpful (https://www.w3schools.com/python/pandas/pandas_dataframes.asp, https://www.statology.org/pandas-select-rows-based-on-column-values/)

#### Final debugging
The final debugging was mostly centered around indentation and the 80 characters restriction in line length. Two local variables were created in the main function that turned out to be not needed because they were not needed for further calculations(sum_private and state_sub). Thus only the functions were called instead.

## Deployment
In order to handle the backend software 'drivers logbook' written in Python, I need the platform Heroku.
Code Institute provided a Github template that allows the software I wrote to run in a mock terminal.

In preparation for the deployment I took the following steps:
* I added a new line character at the end of the text inside the input method
* Create the list of requirements with the command 'Pip3 freeze > requirements.txt'.

The Deployment steps were:
* Register with Heroku
* Create a new app in Heroku
* Set the buildbacks to Python and Node.js (strictly in this order)
* Link the Heroku app to the repository
* Click on deploy branch

## Credits
* Thanks to the Code Instute for the provided learning materials on Python and the deployment terminal.
* Thanks to my mentor for the continuous support, his hint to use RegEx for the number plate validation and his help with nested lists.
* For this project stackoverflow, w3 and statology were very helpful sources of information.

