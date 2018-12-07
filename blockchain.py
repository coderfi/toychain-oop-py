#!/usr/bin/env python

import hashlib
import time


class Block(object):
    ''' An individual block in the blockchain. '''
    def __init__(self, idx, data, ts=None):
        self.idx = idx
        self.data = data
        self.nonce = 0
        self.timestamp = ts if ts else int(time.time())
        self.prevHash = ''
        self.updateBlockHash()

    def updateBlockHash(self):
        h = hashlib.sha256('%s%s%s%s%s' % (self.idx, self.prevHash, self.timestamp, self.data, self.nonce))
        self.hash = h.hexdigest()

    def mineBlock(self, difficulty):
        s = '0' * difficulty

        while self.hash[:difficulty] != s:
            self.nonce += 1
            self.updateBlockHash()

        print("Block mined: " + self.hash)


class Blockchain(object):
    ''' Contains the blocks and provides operations to manage the chain. '''
    def __init__(self, genesis, startDifficulty=5):
        self._chain = []
        self._chain.append(genesis)
        self._difficulty = startDifficulty

    def __add__(self, block):
        last = self.getLastBlock()
        block.prevHash = last.hash
        block.mineBlock(self._difficulty)
        self._chain.append(block)
        return self

    def getLastBlock(self):
        return self._chain[-1]


if __name__ == '__main__':
    from datetime import datetime

    epoch = long(time.mktime(datetime(2018, 1, 1).timetuple()))

    genesis = Block(0, "Genesis Block", ts=epoch)
    chain = Blockchain(genesis, startDifficulty=5)

    print("Init Blockchain[ts=%d]: '%s'\n" % (genesis.timestamp, genesis.data))

    for i in xrange(1, 4):
        label = "Block #%d Data" % i
        ts = epoch + i
        print("%d. Mining[ts=%d]: '%s'" % (i, ts, label))
        chain += Block(i, label, ts=ts)
