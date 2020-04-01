import sys
from klause import Klause
from TransKlauseEngine import TransKlauseEngine


def gen_data(nov, kdic):
    lst = []
    upper = 2**(nov)
    for v in range(upper):
        m = bin(v)[2:].zfill(nov)
        m1 = [e for e in m]
        cov = get_cover(kdic, v)
        m1.append(cov)
        lst.append('   '.join(m1))
    return lst


def get_cover(kdic, v):
    ks = sorted(list(kdic.keys()))
    msg = ' $'
    for k in ks:
        klause = Klause(k, kdic[k])
        if klause.check_block(v):
            msg += f' {k}'
    return msg


def make_new_kdic(kdic, base_kname, nov):
    if base_kname == 'C001':
        return kdic, None
    else:
        tx = TransKlauseEngine(
            kdic[base_kname],
            nov,
            1
        )
        new_kdic = {}
        for k, kl in kdic.items():
            new_kdic[k] = tx.trans_klause(kl)
        return new_kdic, tx


def print_kdic(base_name, kdic, tx=None):
    print(f'{base_name}:')
    print('-'*60)
    if tx:
        m = 'name-tx: ' + str(tx.bitname_tx)
        m += ',   value-tx: ' + str(tx.bitvalue_tx)
        print(m)
    ks = sorted(list(kdic.keys()))
    for k in ks:
        klause_string = str(kdic[k])
        print(f'{k}: {klause_string}')


def print_data(lst):
    for index, line in enumerate(lst):
        head = str(index).zfill(3) + ': '
        print(head + line)


if __name__ == '__main__':
    ''' cmd line:
        python gen.py C001 C002 C003 C004 C005 C006 C007 C008 C009 C010 C011 C012
        output will be 12 blocks of data:
        - (64)cover-lines for the original 12 klause-set: S1
        - (64)cover-lines for Tx(C002): S1  -> S2 : transformed 12 klause-set
        - (64)cover-lines for Tx(C003): S2  -> S3 : transformed 12 klause-set
        - (64)cover-lines for Tx(C004): S3  -> S4 : transformed 12 klause-set
        - (64)cover-lines for Tx(C005): S4  -> S5 : transformed 12 klause-set
        - (64)cover-lines for Tx(C006): S5  -> S6 : transformed 12 klause-set
        - (64)cover-lines for Tx(C007): S6  -> S7 : transformed 12 klause-set
        - (64)cover-lines for Tx(C008): S7  -> S8 : transformed 12 klause-set
        - (64)cover-lines for Tx(C009): S8  -> S9 : transformed 12 klause-set
        - (64)cover-lines for Tx(C010): S9  -> S10 : transformed 12 klause-set
        - (64)cover-lines for Tx(C011): S10 -> S11 : transformed 12 klause-set
        - (64)cover-lines for Tx(C012): S11 -> S12 : transformed 12 klause-set
        ----------------------------------------------------------------------
        in each of the 12 data-blocks, the last 8 lines are 
        covered by base-klause
        '''
    if len(sys.argv) < 2:
        name = 'C002'
    else:
        names = sys.argv[1:]

    conf0 = eval(open('config.py').read())
    kdic = conf0['kdic']
    nov = conf0['nov']

    while len(names) > 0:
        name = names.pop(0)
        kdic, tx = make_new_kdic(kdic, name, nov)
        lst = gen_data(nov, kdic)
        print_kdic(name, kdic, tx)
        print('-'*70)
        print_data(lst)
        print('='*70)
