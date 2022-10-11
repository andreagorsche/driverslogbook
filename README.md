Welcome to the drivers logbook,

it logs and retrieves travel data of car drivers for accounting purposes. No matter if a private car is also used for business or a business car is also used for private purposes, a detailed documentation is required. This software is a fast and simple alternative to the tedious task of handwritten documentation in a manual drivers logbook (see sample image of manual log book below).

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

Another strength of the progam is that the stored data is used to gain new and relevant information for the user. Using a car for different purposes calls for an overview. This is guaranteed through the status report consisting of the sum private and business kilometers driven. Furthermore the state subvention calculation gives the user additional important information out of the entered data. Otherwise these sums and subvention would have to be calculated manually and this is much more daunting and time-consuming than using this simple and straight forward software.

### Possible future applications
The software drivers logbook could gain even more relevance with additional future features, like:
* more number plate formats of other countries
* additional input options for special driver groups that need logbooks too, like e.g. truck drivers
* additional inputs and calculations for driver training e.g. for (driving schools) 
* additional inputs and calculations for racing (e.g. go-carting, racing training)

## Testing


### Bugs
With each written function the debuggin took place right away to avoid cross-functional errors. The key functionalities of the software that cost the most attention and trials where:
* RegEx for number plate validation
* validation and change of data type for entered date
* handling nested lists with the collected input
* filtering relevant data rows from the dataframe
* retrieving the relevant data for calculation

#### RegEx for number plate validation
The use of RegEx was recommended by my mentor. The major challenge during the development process was to define the

## Deployment

## Credits

* Thanks to the Code Instute for the provided learning materials on Python and the deployment terminal.
* Thanks to my mentor for the continuous support, his hint to use RegEx for the number plate validation and his help with nested lists.
* Dataframe!

