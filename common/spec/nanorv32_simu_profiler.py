import re
import collections
import pprint as pp
def read_objdump_map_file(filename):
    "Read a map file generated by objdump using the -t option, return a sorted dict indexed by address"
    re_func = re.compile(r'\s*(?P<addr>\S+)\s+(l|g)\s+(F|O)*\s+\.text\s+(?P<size>\S+)\s+(?P<func_name>\S+)')
    tmp = dict()
    res = collections.OrderedDict()
    with open(filename) as f:
        for line in f:
            match_func = re_func.match(line)
            if match_func:
                addr_str_hex = match_func.group('addr')
                addr_int = int(addr_str_hex, 16)
                func_name = match_func.group('func_name')
                # print "Function <{}> at address 0x{} ({})".format(func_name,
                #                                                  addr_str_hex,
                #                                                  addr_int)
                tmp[addr_int] = func_name
    for k in sorted(tmp.keys()):
        res[k] = tmp[k]
    return res


def get_function_at(func_map,f_addr_a, f_addr_l, addr):
    """return the name of function mapped at address 'addr'
    func_map : dictionnary addr -> function name
    f_addr_a : table of the keys of func_map
    f_addr_l : length of f_addr_a
    """
    def get_base_address(idx,r, addr):
        #print "-D- get_base_address - idx : {} r : {} addr : {}".format( idx, r, addr)
        #print "-D-                    f_addr_a[idx] : {}".format(f_addr_a[idx])

        if (idx <0) :
                return f_addr_a[0]
        if idx >(f_addr_l-1) :
            return f_addr_a[f_addr_l-1]
        elif r == 0 :
            if addr < f_addr_a[idx]:
                return f_addr_a[idx-1]
            else:
                return f_addr_a[idx]
        elif addr == f_addr_a[idx]:
            return addr
        elif addr < f_addr_a[idx]:
            rge = r/2
            n_idx = idx - rge -1
            return get_base_address(n_idx, rge, addr)
        elif addr > f_addr_a[idx]:
            rge = r/2
            n_idx = idx + rge +1
            return get_base_address(n_idx, rge, addr)
        pass

    return func_map[get_base_address(f_addr_l/2, f_addr_l/2 , addr)]

if __name__ == '__main__':
    func_map = read_objdump_map_file("../../../opus/opus.map")
    pp.pprint(func_map)
    func_addr_array = func_map.keys()
    func_addr_array_l = len(func_addr_array)
    f1 = get_function_at(func_map, func_addr_array, func_addr_array_l, 600)
    print "f1 = {}".format(f1)
    print "f2 = {}".format(get_function_at(func_map, func_addr_array, func_addr_array_l,211180 ))
    print "f3 = {}".format(get_function_at(func_map, func_addr_array, func_addr_array_l, 40000 ))
    print "f4 = {}".format(get_function_at(func_map, func_addr_array, func_addr_array_l, 450 ))
    print "f5 = {}".format(get_function_at(func_map, func_addr_array, func_addr_array_l, 333 ))
    print "f6 = {}".format(get_function_at(func_map, func_addr_array, func_addr_array_l, 0 ))
