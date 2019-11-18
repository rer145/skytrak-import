import pandas as pd
import os
import sqlalchemy
import urllib.parse
import pyodbc


ROOT_FOLDER = "D:\\projects\\skytrak-import\\logs"

cols = [
    'ShotNumber', 'Hand', 'BallMPG', 'LaunchAngle', 'BackSpinRPM', 'SideSpinRPM',
    'SideDegrees', 'OfflineYds', 'CarryYds', 'RollYds', 'TotalYds', 'FlightSeconds',
    'DescentDegrees', 'HeightYds', 'ClubMPH', 'PTIScore'
]


def import_file(f):
    print('Importing', f)
    filepath = os.path.join(ROOT_FOLDER, f)
    content = open(filepath).read().split('\n')
    #print(content)

    if len(content) > 0:
        dt = content[1].replace('  PRACTICE: ', '').replace(',', '')
        player = content[2].replace('  PLAYER: ', '').replace(',', '')
        club = content[6].replace(',', '').replace('IRON', 'I').replace('HYBRID', 'H')\
                .replace('WOOD', 'W').replace('DRIVER', 'D').replace(' ','')\
                .replace('Â°', '')
        #print(dt, player, club)

    df = pd.read_csv(filepath, sep=',', skiprows=7, header=None, names=cols)
    df = df[:-2] # remove last two rows (averages)
    #print(df)

    params = urllib.parse.quote_plus(
        "DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE=SkyTrak;UID=skytrak;PWD=skytrak")
    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    conn = engine.connect().connection
    cursor = conn.cursor()

    base_sql = '''
        INSERT INTO [Shots] ([OverallShotNumber],[ClubShotNumber],[Club],[Hand],[BallSpeed],[LaunchAngle]
            ,[Backspin],[Sidespin],[SideDegree],[OfflineYardage],[CarryYardage],[RollYardage],[TotalYardage],
            [FlightTime],[DescentDegree],[HeightYardage],[ClubSpeed],[PTIScore],[TakenOn])
        VALUES
    '''

    temp = []
    for index, row in df.iterrows():
        if row['ShotNumber'] == 'AVG':
            break
        else:
            temp.append([
                row['ShotNumber'], row['ShotNumber'], club,
                row['Hand'],
                row['BallMPG'], row['LaunchAngle'],
                row['BackSpinRPM'], row['SideSpinRPM'],
                row['SideDegrees'], row['OfflineYds'],
                row['CarryYds'], row['RollYds'],
                row['TotalYds'], row['FlightSeconds'],
                row['DescentDegrees'], row['HeightYds'],
                row['ClubMPH'], row['PTIScore'], dt
            ])
    rows = ""
    for x in temp:
        rows += "("+ ','.join("'" + str(e).replace("'", "''").replace('nan', '0') + "'" for e in x) + "), "
    sql = base_sql + rows
    sql = sql[:-2]
    #print(sql)

    print('  Executing sql...')
    try:
        cursor.execute(sql)
        conn.commit()
        print('  Moving file...')
        try:
            os.rename(filepath, os.path.join(ROOT_FOLDER, "imported", f))
        except:
            print('Could not move file', f)
    except:
        print(sql)
    print('  Done')


#import_file("Export_ShotsHistory_11162019_174829.csv")

for filename in os.listdir(ROOT_FOLDER):
    if filename.endswith(".csv") and filename.startswith("Export_ShotsHistory_"):
        import_file(filename)
