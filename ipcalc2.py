import math
import sys

#-----------------------------------------------------

def base_convert(string, base):
    string = string.split('.')
    if len(string) == 1:
        return ""
    result_array = [bin(int(x))[2:] if base == 2 else hex(int(x))[2:] for x in string]
    
    for i in range(len(result_array)):
        if base == 2:
            if len(result_array[i]) < 8:
                while len(result_array[i]) < 8:
                    result_array[i] = '0' + result_array[i]
        elif base == 16:
            if len(result_array[i]) < 2:
                result_array[i] = '0' + result_array[i]
                
    return '.'.join(result_array).upper()

#result table

def get_matrix(address, netmask):
    result = []

    for i in range(4):
        result.append([])

    result[0].append("Имя")
    result[1].append("Значение")
    result[2].append("16-ричный код")
    result[3].append("Бинарное значение")

    result[0].append("Адрес")
    result[0].append("Bitmask")
    result[0].append("Netmask")
    result[0].append("Wildcard")
    result[0].append("Network")
    result[0].append("Broadcast")
    result[0].append("Hostmin")
    result[0].append("Hostmax")
    result[0].append("Hosts")

    address = address.split('/')

    if not len(address) == 2 and netmask == None:
        return "Invalid data"

    result[1].append(address[0]) #ip

    if len(address) == 2:
        if not address[1].isdigit():
            return "invalid bitmask"

    result[1].append(int(address[1]) if len(address) == 2 else None) #bitmask

    for i in address[0].split('.'):
        if not i.isdigit():
            return "invalid ip"

    for i in range(4):  #netmask
        result[1].append([])

    #-----------------------------------------------------
    if result[1][2] == None:
        result[1][3] = netmask
        for i in result[1][3].split('.'):
            if not i.isdigit():
                print("invalid netmask")
                sys.exit()
    else:    
        for i in range(4):
            bitnum = ""
            for j in range(8):
                bitnum = bitnum + ('1' if ((i * 8) + j) < result[1][2] else '0')        
            result[1][3].append(str(int(bitnum, 2)))
        result[1][2] = str(result[1][2])
        result[1][3] = '.'.join(result[1][3])
                    
    #-----------------------------------------------------

    #bitmask

    if result[1][2] == None:
        result[1][2] = 0
        for part in base_convert(result[1][3], 2).split('.'):
            for i in part:
                if int(i) == 1:    
                    result[1][2] = result[1][2] + 1
        result[1][2] = str(result[1][2])
        
    #wildcard

    netmask_parts = result[1][3].split('.')

    for i in range(4):
        result[1][4].append(str(255 - int(netmask_parts[i])))
        
    #network

    ip_parts = result[1][1].split('.')

    for i in range(len(ip_parts)):
        bin_num = str(int(ip_parts[i]) & int(netmask_parts[i]))
        result[1][5].append(bin_num)

    #broadcast 

    network_nums = result[1][5]
    wildcard_nums = result[1][4]

    for i in range(4):
        result[1][6].append(str(int(network_nums[i]) + int(wildcard_nums[i])))

    #hostmin

    result[1].append(list(result[1][5]))

    result[1][7][3] = str(int(result[1][7][3]) + 1)

    #hostmax

    result[1].append(list(result[1][6]))

    result[1][8][3] = str(int(result[1][8][3]) - 1)

    #hosts

    result[1].append(str(int(math.pow(2, 32 - int(result[1][2]))) - 2))

    hosts_nums = []

    for i in range(len(result[1][9])):
        if (len(result[1][9]) - i) % 3 == 0 and i != 0:
            hosts_nums.append(',')
        hosts_nums.append(result[1][9][i])
            

    result[1][9] = ''.join(hosts_nums)

    for i in range(9):
        if isinstance(result[1][i], list):
            result[1][i] = '.'.join(result[1][i])

    for i in range(2):
        for j in range(9):
            num = result[1][j + 1]
            num = base_convert(num, 2) if i == 1 else base_convert(num, 16)
            result[i + 2].append(num)

    return result

        
