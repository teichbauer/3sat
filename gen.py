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


def make_config(fname, base_kname):
    conf = eval(open(fname).read())
    if base_kname == 'C001':
        return conf
    else:
        tx = TransKlauseEngine(conf['kdic'][base_kname], conf['nov'])
        new_conf = {'nov': conf['nov'], 'kdic': {}}
        for k, kl in conf['kdic'].items():
            new_conf['kdic'][k] = tx.trans_klause(kl)
        return new_conf


def print_kdic(kdic):
    ks = sorted(list(kdic.keys()))
    for k in ks:
        klause_string = str(kdic[k])
        print(f'{k}: {klause_string}')


def print_data(lst):
    for index, line in enumerate(lst):
        head = str(index).zfill(3) + ': '
        print(head + line)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        name = 'C002'
    else:
        name = sys.argv[1].strip()

    conf = make_config('config.py', name)
    lst = gen_data(conf['nov'], conf['kdic'])
    print_kdic(conf['kdic'])
    print('-'*70)
    print_data(lst)
