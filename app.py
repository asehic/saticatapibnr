import connexion, json, uuid, base64, random
import ss
from util import imsx_StatusInfo, parse_section_configuration

def createSection(section):
    section_id = str(uuid.uuid1().int)
    c = base64.b64decode(section['sectionConfiguration'].encode()).decode()
    ss.put(section_id, parse_section_configuration(c))
    ss.put('s' + section_id, section)
    response = {'sectionIdentifier': section_id}
    return response, 201

def deleteSection(sectionIdentifier):
    if not ss.get(sectionIdentifier) and not ss.get('s' + sectionIdentifier):
        return imsx_StatusInfo(
            "Section identifier '" + sectionIdentifier + "' not fuound", 'failure', 'error'), 404
    ss.delete(sectionIdentifier)
    ss.delete('s' + sectionIdentifier)
    return '', 204

def getSection(sectionIdentifier):
    section_configuration = ss.get(sectionIdentifier)
    section = ss.get('s' + sectionIdentifier)
    if not section_configuration or not section:
        return imsx_StatusInfo(
            "Section identifier '" + sectionIdentifier + "' not fuound", 'failure', 'error'), 404
    item_identifiers = list(set(item_id for form in section_configuration for item_id in form))
    response = {
        'items': {
            'itemIdentifiers': item_identifiers
        },
        'section': section
    }
    return response, 200

def createSession(sectionIdentifier, session):
    session_id = str(uuid.uuid1().int)
    form = random.choice(ss.get(sectionIdentifier))
    session_state = {
        'sessionIdentifier': session_id,
        'nextItemIdentifiers': form
    }
    response = {
        'sessionIdentifier': session_id,
        'nextItems': {
            'itemIdentifiers': form,
            'stageLength': len(form)
        },
        'sessionState': base64.b64encode(json.dumps(session_state).encode()).decode()
    }
    return response, 201

def deleteSession(sectionIdentifier, sessionIdentifier):
    return imsx_StatusInfo('Not implemented'), 500

def getNextItems(sectionIdentifier, sessionIdentifier, resultSet):
    session_state = json.loads(base64.b64decode(resultSet['sessionState'].encode()).decode())
    if session_state['sessionIdentifier'] != sessionIdentifier:
        return imsx_StatusInfo('Session identifier mismatch', 'failure', 'error'), 400
    next_items = [identifier for identifier in session_state['nextItemIdentifiers'] if \
        identifier not in [i['identifier'] for i in resultSet['assessmentResult']['itemResult']]]
    new_session_state = {
        'sessionIdentifier': sessionIdentifier,
        'nextItemIdentifiers': next_items
    }
    response = {
        'nextItems': {
            'itemIdentifiers': next_items,
            'stageLength': len(next_items)
        },
        'sessionState': base64.b64encode(json.dumps(new_session_state).encode()).decode()
    }
    return response, 201

app = connexion.FlaskApp(__name__, specification_dir='openapi/', server='tornado')
app.add_api('FSCATAPI.json')
app.run(port=8080)