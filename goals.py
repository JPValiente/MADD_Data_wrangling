
# librerias
import xml.etree.ElementTree as ET

# conexion postgresql

#pip install psycopg2-binary
import psycopg2
con = psycopg2.connect(database="european-soccer",
                        host="34.16.139.222",
                        user="postgres",
                        password="password",
                        port="5432")

cur = con.cursor()

############################## proceso
# query
cur.execute('''
SELECT	match_api_id, goal, country_id, league_id, season, stage
FROM 	"Match"
WHERE   goal IS NOT NULL
'''
)

data = [tuple(i[0] for i in cur.description)] + cur.fetchall()



goals = []
goal_id = 0
for i in range(len(data)-1):
    root = ET.fromstring(data[i+1][1])
    # Lista para almacenar los goles que cumplen con los criterios
    goles = []
    # Iterar sobre los elementos 'value' dentro de 'goal'
    for value in root.findall('value'):
        goal_id = goal_id + 1
        try:
            team = int(value.find('team').text)
        except AttributeError:
            team = None
        try: 
            player1 = int(value.find('player1').text)
        except AttributeError:
            player1 = None
        try:
            player2 = int(value.find('player2').text)
        except AttributeError:
            player2 = None
        elapsed = int(value.find('elapsed').text)
        try:
            shoton = int(value.find('stats/shoton').text)
        except AttributeError:
            shoton = None
        try:
            type_ = value.find('type').text
        except AttributeError:
            type_ = None

        try:
            subtype = value.find('subtype').text
        except AttributeError:
            subtype = None
        try:
            penalties = int(value.find('stats/penalties').text)
        except AttributeError:
            penalties = None
        try:
            sortorder = int(value.find('sortorder').text)
        except AttributeError:
            sortorder = None
        try:
            goal_type = value.find('goal_type').text
        except AttributeError:
            goal_type = None
        try:
            event_incident_typefk = int(
                value.find('event_incident_typefk').text)
        except AttributeError:
            event_incident_typefk = None
        try:
            goals_ = int(
                value.find('stats/goals').text)
        except AttributeError:
            goals_ = None
        try:
            owngoals = int(
                value.find('stats/owngoals').text)
        except AttributeError:
            owngoals = None
        try:
            id_ = int(value.find('id').text)
        except AttributeError:
            id_ = None
        try:
            n_ = int(value.find('n').text)
        except AttributeError:
            n_ = None
        temp = (goal_id, data[i+1][0], team, player1, player2, elapsed, shoton, type_, subtype,
                penalties, sortorder, goal_type, event_incident_typefk, goals_, owngoals, id_, n_,
                data[i+1][2], data[i+1][3], data[i+1][4], data[i+1][5])
        goles.append(temp)

    goals = goals + goles


cur = con.cursor()
cur.execute('''
DROP TABLE IF EXISTS "Goals"
''')

# Crear la tabla Goals
cur = con.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS "Goals" (
 goal_id INTEGER PRIMARY KEY,
 match_api_id INTEGER,
 team_api_id  INTEGER,
 player1_id INTEGER,
 player2_id INTEGER,
 elapsed INTEGER,
 shoton INTEGER,
 type TEXT,
 subtype TEXT,
 penalties INTEGER,
 sortorder INTEGER
 goal_type TEXT,
 event_incident INTEGER,
 goals INTEGER,
 owngoals INTEGER,
 id INTEGER,
 n INTEGER,
 country_id INTEGER, 
 league_id INTEGER, 
 season TEXT, 
 stage INTEGER
 )
''')

# Insertar los datos en la tabla

values = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", x).decode('utf-8') for x in goals)

for i in goals:
    cur = con.cursor()
    cur.execute('''INSERT INTO "Goals" VALUES ''' + cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8'))
    print(i)

# Guardar los cambios y cerrar la conexión
con.commit()
con.close()

