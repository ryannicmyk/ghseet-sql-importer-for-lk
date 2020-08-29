import asyncio
import discord
import gspread
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
import datetime
# MAKE SURE TO ADD YOUR CREDS IN creds.py
import creds
import time

trueitemname = ''
useridglob = ''
mydb = creds.mydb
mycursor = mydb.cursor()
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
# google auth creds
credentials = ServiceAccountCredentials.from_json_keyfile_name('filename.json', scope)
bot = commands.Bot(command_prefix='.')


@bot.command()
async def movemoney(message):
    start = time.time()
    refs = 0
    dbcommits = 0
    novals = 0
    # GOOGLE CREDS JSON AUTH FILE as FILENAME
    gc = gspread.authorize(credentials)
    # CORRECT SHEET
    worksheet = gc.open_by_url(creds.sheeturl).sheet1
    lod = worksheet.get_all_records()
    for x in lod:
        for key, value in x.items():
            # DA USERNAME COLOUM
            if key == "USERNAME":

                print(key, value)
                username = value
                sql_select_query = """SELECT id FROM users WHERE alias = %s"""
                mycursor.execute(sql_select_query, (username,))
                useridt = mycursor.fetchone()
                refs += 1
                if useridt is None:
                    print("NOT IN DB")
                    break
                else:
                    print("IN SITE DB")
                    userid = int(useridt[0])
                    # NAME OF THE MONEY/CURRENCY COLLUM
            if key == "BALANCE":
                if useridt is None:
                    print("not in DB")
                else:
                    user_id = int(userid)
                    amount = value
                    moneyid = 1
                    try:
                        query = "INSERT INTO user_currencies(user_id,currency_id,quantity) VALUES(%s,%s,%s)"
                        args = (user_id, moneyid, amount)
                        mycursor.execute(query, args)
                        mydb.commit()
                    except:
                        print("ERROR")
                    dbcommits += 1
    mycursor.close()
    mydb.close()
    end = time.time()
    elapsed = (end - start)
    print("Database translation complete, DB Refs: " + str(refs) + ", DB Commits: " + str(
        dbcommits) + ", Done in: " + str(elapsed) + " Seconds, NOVALS: " + str(novals))


@bot.command()
async def adduser(message, usrarg):
    start = time.time()
    refs = 0
    dbcommits = 0
    novals = 0
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_url(creds.sheeturl).sheet1
    lod = worksheet.get_all_records()
    for x in lod:
        for key, value in x.items():
            if value == usrarg:
                if key == "USERNAME":
                    print(key, value)
                    username = usrarg
                    sql_select_query = """SELECT id FROM users WHERE alias = %s"""
                    mycursor.execute(sql_select_query, (username,))
                    useridt = mycursor.fetchone()
                    refs += 1
                    if useridt is None:
                        open('cooldownlog.txt', 'a').write(username + " Is not in SITE USER DB!" "\n")
                        break
                    else:
                        userid = int(useridt[0])
                else:
                    refs += 1
                    print(key, value)
                    sql_select_query = """select id from items where name = %s"""
                    mycursor.execute(sql_select_query, (key,))
                    row = mycursor.fetchone()
                    print(row)
                    if row is None:
                        print("error: item not in site DB")
                        break
                    else:
                        itemidtrue = row[0]
                        # temp = re.sub(r'[\[\]\(\), ]', '', str(itemidcur))
                        # res = [int(ele) for ele in set(temp)]
                        # itemid = res
                        valueint = value
                    print("ITEM " + str(itemidtrue) + " ADDED")  # WAS COVERTING TUIP TO STRING FOR INPUT
                    if valueint is not None:
                        try:
                            item_id = itemidtrue
                            user_id = int(userid)
                            amount = valueint
                            created_at = timestamp
                            updated_at = timestamp
                            # change to your username
                            datai = '{"data":"auto transfer by snupsplus","notes":null}'
                            query = "INSERT INTO user_items(item_id,user_id,count,data,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s)"
                            args = (item_id, user_id, amount, datai, created_at, updated_at,)
                            print(item_id, user_id, amount, datai, created_at, updated_at)
                            mycursor.execute(query, args)
                            mydb.commit()
                            dbcommits += 1
                        except:
                            print("Fatal Error")
                        finally:
                            print("Done")
                    if valueint is None:
                        novals += 1
                if key == "USERNAME":
                    print(key, value)
                    username = value
                    sql_select_query = """SELECT id FROM users WHERE alias = %s"""
                    mycursor.execute(sql_select_query, (username,))
                    useridt = mycursor.fetchone()
                    refs += 1
                    if useridt is None:
                        print("NOT IN DB")
                        break
                    else:
                        print("IN SITE DB")
                        userid = int(useridt[0])
                if key == "BALANCE":
                    if useridt is None:
                        print("not in DB")
                    else:
                        user_id = int(userid)
                        amount = value
                        moneyid = 1
                        try:
                            query = "INSERT INTO user_currencies(user_id,currency_id,quantity) VALUES(%s,%s,%s)"
                            args = (user_id, moneyid, amount)
                            mycursor.execute(query, args)
                            mydb.commit()
                        except:
                            print("ERROR")
                        dbcommits += 1
    mycursor.close()
    mydb.close()
    end = time.time()
    elapsed = (end - start)
    print("Database translation complete, DB Refs: " + str(refs) + ", DB Commits: " + str(
        dbcommits) + ", Done in: " + str(elapsed) + " Seconds, NOVALS: " + str(novals))


@bot.command()
async def moveusers(message):
    start = time.time()
    refs = 0
    dbcommits = 0
    novals = 0
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_url(creds.sheeturl).sheet1
    lod = worksheet.get_all_records()
    for x in lod:
        for key, value in x.items():
            if key == "USERNAME":
                print(key, value)
                username = value
                sql_select_query = """SELECT id FROM users WHERE alias = %s"""
                mycursor.execute(sql_select_query, (username,))
                useridt = mycursor.fetchone()
                refs += 1
                if useridt is None:
                    open('cooldownlog.txt', 'a').write(username + " Is not in SITE USER DB!" "\n")
                    break
                else:
                    userid = int(useridt[0])
            else:
                refs += 1
                print(key, value)
                sql_select_query = """select id from items where name = %s"""
                mycursor.execute(sql_select_query, (key,))
                row = mycursor.fetchone()
                print(row)
                if row is None:
                    print("error: item not in site DB")
                    break
                else:
                    itemidtrue = row[0]
                    # temp = re.sub(r'[\[\]\(\), ]', '', str(itemidcur))
                    # res = [int(ele) for ele in set(temp)]
                    # itemid = res
                    valueint = value
                print("ITEM " + str(itemidtrue) + " ADDED")  # WAS COVERTING TUIP TO STRING FOR INPUT
                if valueint is not None:
                    try:
                        item_id = itemidtrue
                        user_id = int(userid)
                        amount = valueint
                        created_at = timestamp
                        updated_at = timestamp
                        # change to your username
                        datai = '{"data":"auto transfer by snupsplus","notes":null}'
                        query = "INSERT INTO user_items(item_id,user_id,count,data,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s)"
                        args = (item_id, user_id, amount, datai, created_at, updated_at,)
                        print(item_id, user_id, amount, datai, created_at, updated_at)
                        mycursor.execute(query, args)
                        mydb.commit()
                        dbcommits += 1
                    except:
                        print("Fatal Error")
                    finally:
                        print("Done")
                if valueint is None:
                    novals += 1
            if key == "USERNAME":
                print(key, value)
                username = value
                sql_select_query = """SELECT id FROM users WHERE alias = %s"""
                mycursor.execute(sql_select_query, (username,))
                useridt = mycursor.fetchone()
                refs += 1
                if useridt is None:
                    print("NOT IN DB")
                    break
                else:
                    print("IN SITE DB")
                    userid = int(useridt[0])
            if key == "BALANCE":
                if useridt is None:
                    print("not in DB")
                else:
                    user_id = int(userid)
                    amount = value
                    moneyid = 1
                    try:
                        query = "INSERT INTO user_currencies(user_id,currency_id,quantity) VALUES(%s,%s,%s)"
                        args = (user_id, moneyid, amount)
                        mycursor.execute(query, args)
                        mydb.commit()
                    except:
                        print("ERROR")
                    dbcommits += 1
    mycursor.close()
    mydb.close()
    end = time.time()
    elapsed = (end - start)
    print("Database translation complete, DB Refs: " + str(refs) + ", DB Commits: " + str(
        dbcommits) + ", Done in: " + str(elapsed) + " Seconds, NOVALS: " + str(novals))

bot.run(creds.apikey)