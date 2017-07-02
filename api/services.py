'''
Gets track id from sharing url
'''

def parse_track_id(url):
    id = url.split('/')[-1]
    return id