def read_bit(v, b):
    if v >= 2**b:
        return (v >> b) & 1
    else:
        return 0


def set_bit(v, b, set_v):
    ov = read_bit(v, b)
    if ov == set_v:
        return v
    else:
        return v ^ (1 << b)


def flip_bit_value(v, b):
    pass


def toggle_bit(v, b):
    return v ^ (1 << b)


def trade_bits(v, b1, b2):
    if read_bit(v, b1) == read_bit(v, b2):
        return v
    else:
        v1 = toggle_bit(v, b1)
        v2 = toggle_bit(v1, b2)
        return v2


class TransKlauseEngine:
    """
        move base_klause's 3 bits to the left-most positions, and
        set them to be 0 0 0 -> self.klause. while doing this, set up 
        operators so that any klause (coming from base_klause's set) 
        will be trnasfered to a new klause compatible to self.klause
        """

    def __init__(self, base_klause, nov, set_to_value=0):
        self.start_klause = base_klause
        self.nov = nov
        self.set2v = set_to_value                 # the same as set_to_value
        self.flip_trigger = [1, 0][set_to_value]  # opposit of set_to_value
        self.setup_tx_operators()

    def setup_tx_operators(self):
        bits = sorted(list(self.start_klause.keys()))
        bits.reverse()
        # target/left-most 3 bits(names)
        hi_bits = [self.nov - 1, self.nov - 2, self.nov - 3]
        self.bitname_tx = {}
        self.bitvalue_tx = {}
        for b in bits:
            if b in hi_bits:
                hi_bits.remove(b)
                hi = b
            else:
                hi = hi_bits.pop(0)
                self.bitname_tx[b] = hi
                self.bitname_tx[hi] = b

            # if self.start_klause[b] == 1:
            if self.start_klause[b] == self.flip_trigger:
                self.bitvalue_tx[hi] = True
        n = self.nov - 1
        self.klause = {n: 0, n-1: 0, n-2: 0}

    def trans_klause(self, klause):
        dic = {}
        txn = self.bitname_tx.copy()
        for b, v in klause.items():
            if b in txn:
                new_bit = txn.pop(b)
                dic[new_bit] = v
            else:
                dic[b] = v
        for b, v in dic.items():
            if b in self.bitvalue_tx:
                dic[b] = int(not(v))
            else:
                dic[b] = v
        return dic

    def trans_value(self, v):
        d = self.bitname_tx.copy()
        ks = list(d.keys())
        vx = v
        while len(d):
            b0 = ks.pop(0)
            b1 = d[b0]
            d.pop(b0)
            d.pop(b1)
            ks.remove(b1)
            vx = trade_bits(vx, b0, b1)
        for b in self.bitvalue_tx:
            vx = toggle_bit(vx, b)
        return vx


def test():
    kdic = {
        "C001": {5: 1, 4: 1, 3: 1},
        "C002": {2: 0, 1: 1, 0: 0},
        "C003": {5: 0, 4: 0, 2: 1}
    }
    while True:
        msg = input("<base kname> <value>: ")
        if msg.startswith('e'):
            break
        kn, v = msg.split()
        tx = TransKlauseEngine(kdic[kn], 6, 1)
        vx = tx.trans_value(int(v))
        print(f'transfer({v}): {vx}')
    x = 1


if __name__ == '__main__':
    test()
