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
