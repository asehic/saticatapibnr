import connexion, json, uuid, base64, random
import ss

def parse_section_configuration(c):
    config = json.loads(c)
    return [[item['itemId'] for item in form['items']] for form in config['forms']]

def createSection(section):
    section_id = str(uuid.uuid1().int)
    c = base64.b64decode(section['sectionConfiguration'].encode()).decode()
    ss.put(section_id, parse_section_configuration(c))
    response = {'sectionIdentifier': section_id}
    return response, 201

def getSection(sectionIdentifier):
    return 'Not Implemented', 500

def deleteSection(sectionIdentifier):
    return 'Not Implemented', 500

def createSession(sectionIdentifier, session):
    session_id = str(uuid.uuid1().int)
    form = random.choice(ss.get(sectionIdentifier))
    response = {
        'sessionIdentifier': session_id,
        'nextItems': {
            'itemIdentifiers': form,
            'stageLength': len(form)
        },
        'sessionState': ''
    }
    return response, 201

def deleteSession(sectionIdentifier, sessionIdentifier):
    return 'Not Implemented', 500

def getNextItems(sectionIdentifier, sessionIdentifier, resultSet):
    return 'Not Implemented', 500

app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app.add_api('FSCATAPI.json')
app.run(port=8080)