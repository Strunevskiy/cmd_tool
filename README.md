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

* To set up database setting it is required to fill listed properties in the db.properties file
    * host
    * port
    * user
    * passwd

## Run utility