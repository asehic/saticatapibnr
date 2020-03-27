import connexion, uuid, base64, random
import ss
from util import imsx_StatusInfo, parse_section_configuration

def createSection(section):
    section_id = str(uuid.uuid1().int)
    c = base64.b64decode(section['sectionConfiguration'].encode()).decode()
    ss.put(section_id, parse_section_configuration(c))
    response = {'sectionIdentifier': section_id}
    return response, 201

def getSection(sectionIdentifier):
    return imsx_StatusInfo('Not Implemented'), 500

def deleteSection(sectionIdentifier):
    return imsx_StatusInfo('Not Implemented'), 500

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
    return imsx_StatusInfo('Not Implemented'), 500

def getNextItems(sectionIdentifier, sessionIdentifier, resultSet):
    return imsx_StatusInfo('Not Implemented'), 500

app = connexion.FlaskApp(__name__, specification_dir='openapi/', server='tornado')
app.add_api('FSCATAPI.json')
app.run(port=8080)