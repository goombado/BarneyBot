import schoolopy
import yaml
import webbrowser as wb
import datetime

with open('example_config.yml', 'r') as f:
    cfg = yaml.load(f)

# Instantiate with 'three_legged' set to True for three_legged oauth.
# Make sure to replace 'https://www.schoology.com' with your school's domain.
DOMAIN = 'https://schoology.sydgram.nsw.edu.au/'

auth = schoolopy.Auth(cfg['key'], cfg['secret'], three_legged=True, domain=DOMAIN)
# Request authorization URL to open in another window.
url = auth.request_authorization()

# Open OAuth authorization webpage. Give time to authorize.
if url is not None:
    wb.open(url, new=2)

# Wait for user to accept or deny the request.
input('Press enter when ready.')

# Authorize the Auth instance as the user has either accepted or not accepted the request.
# Returns False if failed.

if not auth.authorize():
    raise SystemExit('Account was not authorized.')

# Create a Schoology instance with Auth as a parameter.
sc = schoolopy.Schoology(auth)
sc.limit = 500  # Only retrieve 10 objects max

print('Your name is %s' % sc.get_me().name_display)
event_list = []
uid = sc.get_me().id
for event in sc.get_events(user_id=uid):
    if event.type == 'assignment':
        url = event.web_url
    elif event.type == 'assessment':
        url = f'https://schoology.sydgram.nsw.edu.au/assignment/{event.assignment_id}/assessment'
    else:
        url = None
    if url is not None:
        if int(event.start[:4]) >= datetime.datetime.now().year and int(event.start[5:7]) >= datetime.datetime.now().month and int(event.start[8:10]) >= datetime.datetime.now().day:
            print(event)
            event_list.append(f'{event.title} due on {event.start}. Link: {url}')

response = "\n".join(event_list)
print(f'Your assignments are:\n{response}')
    #print(event)
    #event = sc.get_user(update.uid)
    #print('By: ' + user.name_display)
    #print(update.body[:40].replace('\r\n', ' ').replace('\n', ' ') + '...')
    #print('%d likes\n' % update.likes)