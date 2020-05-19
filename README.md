### Project name: 
Finance Manager Bot

____

### Description: 
The bot allows you to control all your spendings in certain period of time. Simple and cosy in using, you may use it in any situation as it does not take any additional actions. This is an ideal bot for people whose main messanger is Telegram. Moreover, you are able to search for products you want to buy by the price you set (only Ebay, other marketplaces can be added). Bot will return you two files with the information you need (excel and pdf), you may use the more comfortable one.

____ 
### Table of contents
- [**Installation**](#installation)
- [**Usage**](#usage)
- [**Credits**](#credits)    
 
 
____
<a name="installation"/>

### Installation
First of all, if you want to set this bot you have to use Telegram's Bot Father and create your bot link and recieve a token. You have to get Ebay API as well.

You may clone the repository and install through the pip installer such modules:

1. For working with data (data_main.py):

  - ebaysdk - module for working with Ebay API
    
  - xlsxwriter - module for working with Excel files
    
  - fpdf - module for working with PDF files

2.For working with main module (mainbot.py):

   - pytelegrambotapi (telebot) - working with telegram API
    
   - emoji - for correct emoji representation, is not as important as the other ones
    
    
Now you can run the bot and see how it works! You can read the documentation in *documentation* folder

____
<a name="usage"/>

### Usage

The bot is quite simple in using, there are four commands that you can use:

1. /start - start using the bot with this command

2. /help - bot will send you the instruction if you do not know how to use it

3. /search - more functional than two prevoius commands. You can tell bot the name of the product that you want to find. Bot will ask you to enter the price range (from price1 to price2). You will be returned two files results.xlsx and results.pdf, there will be all the information you need:

    - Title
    - Price
    - Link (advertisement on Ebay)
    - Location (of the seller)
    - Shipping (always free)
    
If bot have not found any product, or if you entered something wrong, you will be informed.

4. /spends - command for controling your spends. Time counting starts when you run the bot. There are some operations you can use:
- My spending - returns you the money you have spent
- Spending in last time - returns you the money you have spent and how much time have passed (time - hours/minutes/seconds/miliseconds)
- Add spending - allows you to add the sum you spent, for buying some products in the shop, for example
- Reset - resets time and spendings

____
<a name="credits"/>

### Credits
- Meda Volodymyr