import hy

class Predvidac:

    def __init__(self, znamky, vahy):
        self.znamky = znamky
        self.vahy = vahy
        self.prumer = self.vypocitej_prumer(znamky, vahy)

    def vypocitej_prumer(self, znamky, vahy):
        return hy.pyops.hyx_Xplus_signX(*[i * j for i, j in zip(znamky, vahy)]) / hy.pyops.hyx_Xplus_signX(*[i for i in vahy])

    def vypis_menu(self):
        print('1. Přidat známku')
        print('2. Odebrat známku')
        print('3. Ukázat známky')
        return print('4. Ukončit')

    def spustit(self):
        while True:
            self.vypis_menu()
            print(f'Průměr: {self.prumer}')
            try:
                vyber = input()
                _hy_anon_var_1 = None
            except KeyboardInterrupt:
                _hy_anon_var_1 = None
            except EOFError:
                raise SystemExit
                _hy_anon_var_1 = None
            if vyber == '1':
                vstup = input('Zadej známku a váhu: ')
                vstup = vstup.split()
                self.znamky.append(int(vstup[0]))
                _hy_anon_var_5 = self.vahy.append(int(vstup[1]))
            else:
                if vyber == '2':
                    print('Číslo Známka Váha')
                    print(hy.pyops.hyx_Xplus_signX(*[f'  {i + 1}.     {j}    {self.vahy[i]}\n' for i, j in zip(range(len(self.znamky)), self.znamky)]))
                    vstup = int(input('Vyber známku: '))
                    del self.znamky[vstup - 1]
                    del self.vahy[vstup - 1]
                    _hy_anon_var_4 = None
                else:
                    if vyber == '3':
                        print('Známka Váha')
                        _hy_anon_var_3 = print(hy.pyops.hyx_Xplus_signX(*[f'   {i}     {j}\n' for i, j in zip(self.znamky, self.vahy)]))
                    else:
                        if vyber == '4':
                            raise SystemExit
                            _hy_anon_var_2 = None
                        else:
                            _hy_anon_var_2 = None
                        _hy_anon_var_3 = _hy_anon_var_2
                    _hy_anon_var_4 = _hy_anon_var_3
                _hy_anon_var_5 = _hy_anon_var_4
            self.prumer = self.vypocitej_prumer(self.znamky, self.vahy)
if __name__ == '__main__':
    p = Predvidac([1, 2, 3], [3, 2, 1])
    _hy_anon_var_6 = p.spustit()
else:
    _hy_anon_var_6 = 1 + 1
