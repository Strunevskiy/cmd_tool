## Commandline utility
The utility is used by salesmen and managers of the "Coffee For Me" company.
It has two roles, namely salesman and manager.
Whereas salesman is allowed to look up available items and create an order
by combining items with generated bill of the order,
a manager can generate financial reports in different formats to see sales figures.

## Resources available to salesman

* There are two sorts of resources: bill and menu
    * After an order is submitted, corresponding bill is generated.
    The generated bill is stored in the folder that is called outcome named as date when it was submitted.
    * All items available to salesman are stored in the property file that is called menu.
    Any item has a format item name=item cost.

## Setup environment

* The steps to setup environment:
	* Install [python](https://www.python.org)
	* Install [MySQL](https://www.mysql.com)


## Setup database setting

* To set up database setting it is required to fill listed properties in the db.cfg file stored in the config folder.
    * host
    * port
    * user
    * passwd


## Commands
The utility can be used by users with different roles depending on provided role a user can execute a specific set of operations.

* salesman role:
    * show - arg is {beverage or ingredient}. It returns names of all the available beverages or ingredients.
    * price - arg is {beverage or ingredient}. It returns price of all the available beverages or ingredients.
    * add_items - args are list of beverage or ingredient names passed vie whitespace. It adds items to order.
    * submit_order - no arg is required. It persists order data to DB and generates the bill of the order that is stored in folder outcome.
    * clean - no arg is required. It is used to remove items added to the order.
* manager role:
    * generate_report - arg is {console or sheet}. It produces summary of all the sales records by putting it in depending on the provided argument
    (console - the utility console, sheet - it has not been implemented yet)


## Mode
The utility has two modes in which it can operate, namely command_line and interactive mode.
* command_line - since that mode executes one command per launch it can be used with commands that are accountable for displaying information.
* interactive - that mode can be used with all commands listed and provides prompts while executing commands.

## Run utility
After setting up environment is carried out, the utility can be run.

* To run the utility using the command line it is required to specify mandatory arguments in the following order:
    * first name
    * last name
    * user role (user role can be either salesman or manager)
    * the utility mode (mode can be either command_line or interactive)
    * -c (a command to be executed)


## Example

```
>> python run.py Aleh Struneuski salesman interactive -c price
```