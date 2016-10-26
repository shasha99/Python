import requests;
import sys;


class SlackError(Exception):
    pass

class SlackClient(object):
    BASE_URL = 'https://slack.com/api'

    def __init__(self, token):
        self.token = token
        self.blocked_until = None
        self.channel_name_id_map = {}
		
    def chat_post_message(self, channel, text, **params):
        method = 'chat.postMessage'
        params.update({
            'channel': channel,
            'text': text,
        })
        print(method)
        print(params)
        return self._make_request(method, params)
		
    def _make_request(self, method, params):
        if self.blocked_until is not None and \
                datetime.datetime.utcnow() < self.blocked_until:
            raise SlackError("Too many requests - wait until {0}" \
                    .format(self.blocked_until))

        url = "%s/%s" % (SlackClient.BASE_URL, method)
        params['token'] = self.token
        print(params)
        response = requests.post(url, data=params, verify=False)
        print("got the response")
        if response.status_code == 429:
            # Too many requests
            retry_after = int(response.headers.get('retry-after', '1'))
            self.blocked_until = datetime.datetime.utcnow() + \
                    datetime.timedelta(seconds=retry_after)
            raise SlackError("Too many requests - retry after {0} second(s)" \
                    .format(retry_after))

        result = response.json()
        if not result['ok']:
            raise SlackError(result['error'])
        return result
        
client = SlackClient("xoxp-6943337843-6943337859-96519393874-6de4fa97927b355c96f65b9b79c7106f")

try:
	client.chat_post_message('#roar', "A Roar from th Jungle again !!!", username='shashank awasthi')
except Exception as e:
	print(e)
