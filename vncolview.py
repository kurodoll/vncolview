import os
import pickle
import time

import tornado.ioloop
import tornado.web

import asyncio
import Shosetsu

import sys
sys.setrecursionlimit(100000)

setsu = Shosetsu.Shosetsu()
novel_data = []


async def getNovelData():
    novels = os.listdir('F:/Games/VNs/')

    for n in novels:
        if n[0] == '[':
            break

        try:
            n = n.split(' - ', 1)[1]
            res = await setsu.get_novel(n)
            novel_data.append(res)
            time.sleep(3)

        except IndexError:
            pass
        except Shosetsu.errors.VNDBNoResults:
            pass

    pickle.dump(novel_data, open('db', 'wb'))


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.render('index.html', novels=novel_data)


def makeApp():
    return tornado.web.Application([
        (r'/', MainHandler)
    ])


if __name__ == '__main__':
    if not os.path.exists('db'):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(getNovelData())

    else:
        novel_data = pickle.load(open('db', 'rb'))

    app = makeApp()
    app.listen(3000)
    tornado.ioloop.IOLoop.current().start()
