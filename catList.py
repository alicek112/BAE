import MySQLdb as mdb

con = mdb.connect('bae.cp0g2lykd7ui.us-east-1.rds.amazonaws.com', 'bae', 'bae333bae', 'bae333');

catList = {}
catList['skating'] = 'Figure Skating at Baker Rink'
catList['watching'] = 'Watch your friends do their thang!'
catList['basketball'] = 'Put balls in baskets! (Or not!)'
catList['martial'] = 'Lean to beat people up and steal their lunch money!'
catList['stephens'] = 'Get swole bruh'
catList['dillon'] = 'The campus gym, yaaay!'
catList['swimming'] = 'Hopefully you do not drown!'
catList['squash'] = 'My parents first date was playing squash!'
catList['tennis'] = 'There is an asshole in my Portuguese class on the tennis team'
catList['running'] = 'Lots of running trails!'
catList['fitness'] = 'And cupcakes for reasons!'
catList['oa'] = 'But actually just climbing'
catList['dance'] = 'Move your body in an artistic manner!'
catList['biking'] = 'Move on top of wheels. Did you know that bikes were not a thing until really late in time because roads were so bad?'
catList['yoga'] = 'One of the instructors at Gratitude used to work at Goldman!'

rec = 'http://dailyotter.com'
with con:
    
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS catList")
    cur.execute("CREATE TABLE catList(CATEGORY VARCHAR(100), DESCRIPTION VARCHAR(1000), RESOURCES VARCHAR(100))")
    for poop in catList:
        cur.execute("INSERT INTO catList (CATEGORY, DESCRIPTION, RESOURCES) VALUES (%s, %s, %s)", (poop, catList[poop], rec))
