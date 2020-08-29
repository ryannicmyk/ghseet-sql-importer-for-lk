# ghseet-sql-importer-for-lk
A google sheets to Lorekeeper database importer to import items and currency, meant specifically for MySql

```
Hi
i wrote some code, its meant for moving items for users who are allredy signed up on the site
i also left comments so you know how to use it
PLEASE READ THE COMMENTS  !!!!
it uses python 3.8.5
there is a requirements.txt
tabel should be set up in a
------
      BAL ITEM ITEM ITEM
USER   5   1     1  
USER   0         1
USER   1
USER   3   1         4
----------
0 or a null value works for the nothing aeras
make sure to check that your item names are the same as they are in both sheet/site
usernames are based off of looking up the name in the sheet against the sites DA alais, so if the name is the same on the sheet as it is on DA, itll work
any users not in the site will me skipped and will be logged for future ref

.movemoney
- moves everyones balance for currency

.adduser USERNAME
  - moves a specific user, example: .adduser snpuspaws
  - also moves said users  items + balance
.moveusers 
  - moves all users items
```
