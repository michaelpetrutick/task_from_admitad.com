import re
import sys
import json
from splitstream import splitfile

SHOP_URL = 'shop.com'
OUR_REFERERS = ['referal.ours.com', 'ad.theirs1.com', 'ad.theirs2.com']
referer_poins = {}

class Buyer():
    """Class Buyer contains client_id, client history and referers hystory"""
    def __init__(self, client_id):
        self.history = []
        self.referer = []
        self.client_id = client_id

    def parse(self, log_line):
        """Parse log item"""
        global referer_poins

        if SHOP_URL in log_line['document.referer']:
            self.history.append(log_line['document.referer'])
        else:
            referer = re.findall('https?://((?:[-\w.]|(?:%[\da-fA-F]{2}))+)', log_line['document.referer'])
            self.referer.append(referer)

        self.history.append(log_line['document.location'])

        if ('https://{}/checkout'.format(SHOP_URL) in log_line['document.location'] and
            self.referer[-1][0] in OUR_REFERERS):
            referer_poins[self.referer[-1][0]] += 1

def generate_json(log_file):
    """Reads log file as JSON"""
    with open(log_file, 'r') as f:
        for jsonstr in splitfile(f, format="json"):
            yield json.loads(jsonstr)

def process_log_file(log_file):
    """Log file processing"""
    global referer_poins

    for ref in OUR_REFERERS:
        referer_poins[ref] = 0

    buyers = []
    for item in generate_json(log_file):
        # Get exist buyer or create new
        buyer = [buyer for buyer in buyers if buyer.client_id == item['client_id']]
        if not buyer:
            buyer = Buyer(item['client_id'])
            buyers.append(buyer)
        else:
            buyer = buyer[0]

        # Parse logfile item
        buyer.parse(item)

    res = referer_poins
    res.update({'Total buyers': len(buyers)})
    return res

if len(sys.argv) > 1:
    log_file = sys.argv[1]
else:
    log_file = 'data/test.log'

if __name__ == "__main__":
    res = process_log_file(log_file)
    print(res)



