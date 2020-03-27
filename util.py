import json

def imsx_StatusInfo(description=None, code_major='unsupported', severity='error'):
    if code_major not in ['success', 'processing', 'failure', 'unsupported']:
        code_major = 'unsupported'
    if severity not in ['status', 'warning', 'error']:
        severity = 'error'
    statusInfo = {
        'imsx_codeMajor': code_major,
        'imsx_severity': severity
    }
    if description:
        statusInfo['imsx_description'] = description
    return statusInfo

def parse_section_configuration(c):
    config = json.loads(c)
    return [[item['itemId'] for item in form['items']] for form in config['forms']]
