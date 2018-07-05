import os
import unittest
from main import process_log_file

log_file = 'data/test.log'


def add_to_log(client_id, user_agent, location, referer, date, newfile=False):
    if os.path.exists(log_file) and newfile == True:
        os.remove(log_file)

    with open(log_file, 'a+') as log:
        log_line = '\n"client_id": "{}",\n"User-Agent": "{}",\n"document.location": "{}",\n' \
                   '"document.referer": "{}",\n"date": "{}"\n'.format(client_id, user_agent, location, referer, date)
        log.write('\n{'+log_line+'}')
        log.close()


class TestDataProcess(unittest.TestCase):
    def test_user_from_organic(self):
        """Organic buyer"""
        add_to_log("user15", "Firefox 59", "https://shop.com/products/?id=2",
                   "https://yandex.ru/search/?q=купить+котика", "2018-04-03T07:59:13.286000Z", newfile=True)

        add_to_log("user15", "Firefox 59", "https://shop.com/products/?id=3",
                   "https://shop.com/products/?id=2", "2018-04-03T07:59:13.286000Z")

        add_to_log("user15", "Firefox 59", " https://shop.com/checkout",
                   "https://shop.com/products/?id=3", "2018-04-03T07:59:13.286000Z")

        res = process_log_file(log_file)
        self.assertEqual(res['Total buyers'], 1)

    def test_user_from_referer(self):
        """Referer buyer"""
        add_to_log("user15", "Firefox 59", "https://shop.com/products/?id=2",
                   "https://ad.theirs1.com/?src=q1w2e3r4", "2018-04-03T07:59:13.286000Z", newfile=True)

        add_to_log("user15", "Firefox 59", "https://shop.com/products/?id=3",
                   "https://shop.com/products/?id=2", "2018-04-03T07:59:13.286000Z")

        add_to_log("user15", "Firefox 59", " https://shop.com/checkout",
                   "https://shop.com/products/?id=3", "2018-04-03T07:59:13.286000Z")

        res = process_log_file(log_file)
        self.assertEqual(res['Total buyers'], 1)
        self.assertEqual(res['ad.theirs1.com'], 1)

    def test_user_from_referer_and_organic(self):
        """First enter from referer, second enter from Organic"""
        add_to_log("user15", "Firefox 59", "https://shop.com/products/?id=2",
                   "https://ad.theirs1.com/?src=q1w2e3r4", "2018-04-03T07:59:13.286000Z", newfile=True)

        add_to_log("user15", "Firefox 59", "https://shop.com/products/?id=3",
                   "https://shop.com/products/?id=2", "2018-04-03T07:59:13.286000Z")

        add_to_log("user15", "Firefox 59", "https://shop.com/products/?id=2",
                   "https://yandex.ru/search/?q=купить+котика", "2018-04-03T07:59:13.286000Z", newfile=True)

        add_to_log("user15", "Firefox 59", " https://shop.com/checkout",
                   "https://shop.com/products/?id=3", "2018-04-03T07:59:13.286000Z")

        res = process_log_file(log_file)
        self.assertEqual(res['Total buyers'], 1)
        self.assertEqual(res['ad.theirs1.com'], 0)

    def test_two_client_one_buyer(self):
        """Two clients on site and only one buyer"""
        add_to_log("user0", "Firefox 59", "https://shop.com/products/?id=2",
                   "https://ad.theirs1.com/?src=q1w2e3r4", "2018-04-03T07:59:13.286000Z", newfile=True)

        add_to_log("user0", "Firefox 59", "https://shop.com/products/?id=3",
                   "https://shop.com/products/?id=2", "2018-04-03T07:59:13.286000Z")

        add_to_log("user15", "Firefox 59", "https://shop.com/products/?id=2",
                   "https://ad.theirs1.com/?src=q1w2e3r4", "2018-04-03T07:59:13.286000Z")

        add_to_log("user15", "Firefox 59", "https://shop.com/products/?id=3",
                   "https://shop.com/products/?id=2", "2018-04-03T07:59:13.286000Z")

        add_to_log("user15", "Firefox 59", " https://shop.com/checkout",
                   "https://shop.com/products/?id=3", "2018-04-03T07:59:13.286000Z")

        res = process_log_file(log_file)
        self.assertEqual(res['Total buyers'], 2)
        self.assertEqual(res['ad.theirs1.com'], 1)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)