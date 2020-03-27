import base64, requests, json

settings_file_path = 'EFTScienceForms.json'
sectionIdentifier = ''

def test_post_sections():

    global settings_file_path, sectionIdentifier

    with open(settings_file_path) as settings_file:
        section_configuration = settings_file.read()
    encoded_section_configuration = base64.b64encode(section_configuration.encode())

    url = 'http://localhost:8080/ims/cat/v1p0/sections'
    payload = '{\n    "sectionConfiguration": "' + encoded_section_configuration.decode() + '"\n}'
    headers = {'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data = payload)

    sectionIdentifier = response.json()['sectionIdentifier']
    assert response.status_code == 201
    assert isinstance(sectionIdentifier, str)
    assert len(sectionIdentifier) > 8

def test_post_sessions():

    global settings_file_path, sectionIdentifier

    with open(settings_file_path) as settings_file:
        settings = json.load(settings_file)

    url = 'http://localhost:8080/ims/cat/v1p0/sections/' + sectionIdentifier + '/sessions'
    payload = '{}'
    headers = {'Content-Type': 'application/json'}

    for _ in range(100):
        response = requests.request('POST', url, headers=headers, data = payload)

        assert response.status_code == 201
        assert response.json()['nextItems']['itemIdentifiers'] in \
            [[item['itemId'] for item in form['items']] for form in settings['forms']]
