#Author  : Ahmed Zurba
#Python 3.10
import math
import re

#Given an IP address as input,
#the task is to write a Python program to check whether the given IP Address is Valid or not


def is_ip(ip_address): #asd127.21.12.2
    ip_regex="^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"
    ip_regex_2="^([0-9]{1,3}\.){3}[0-9]{1,3}$"
    ip_regex_3="^(((25[0-5])|(2[0-4][0-9])|([0-1][0-9][0-9])|([0-9][0-9]?))\.){3}((25[0-5])|(2[0-4][0-9])|([0-1][0-9][0-9])|([0-9][0-9]?))"
    if not re.search(ip_regex_2, ip_address):
        print(f"The IP address {ip_address} is not valid")
        return False
    octa = ip_address.split(".")
    for ip_octa in octa:
        if int(ip_octa) < 0 or int(ip_octa) > 255:
            print(f"The IP address {ip_address} is not valid")
            return False
    print(f"The IP address {ip_address} is valid")
    return True


#function gets an ip address and returns the cidr of it depends on ip class
def get_cidr(ip_address):
    cidr=0
    ip=ip_address.split(".") #Splitting the ip
    num=int(ip[0]) #getting the first octet
    if(num>=0 and num<=127): #class A       # (0 <= num <=127)
         cidr=8
    elif(num>127 and num<=191): #class B
       cidr=16
    elif(num>=192 and num<=223): #class C
        cidr=24
    return cidr


def get_subnet(ip, cidr):
    if (cidr < 32):
        octa = cidr//8                                     #ocat-1
        target_octa_value = int(ip.split(".")[octa])
        host_bit = 8 - cidr % 8                          #every octa 8 bits
        group_size = 2 ** host_bit
        octa_subnet_id = target_octa_value-(target_octa_value % group_size)
        new_ip = "" #192.168.135.31/23 -> 192.168.135.0
        octa_index = 0
        while (octa_index < 4):
            if (octa_index < octa):
                new_ip += ip.split(".")[octa_index]+"."
            elif (octa_index == octa):
                new_ip += str(octa_subnet_id)
                if (octa_index <3 ):
                    new_ip +="."
            else:
                new_ip +="0"
                if (octa_index < 3):
                    new_ip += "."
            octa_index += 1
        print(new_ip)
    else:
        print(ip)

def get_subnetmask(cidr):
    octa=cidr//8
    subnet_bits_in_octa=8-cidr%8
    subnet_num=256-2**subnet_bits_in_octa
    index=0
    subnetmask=""
    while index < 4:
        if(index<octa):
            subnetmask += "255"+"."
        elif(index==octa):
            subnetmask += str(subnet_num) + "."
        else:
            subnetmask += "0"
        index+=1
    return subnetmask

        # Input positive number
def get_bits_number(num):
    bit = math.log2(num)
    return math.ceil(bit)

def calc_new_cidr(part_type, bit_num, cidr):
    if (part_type == "Subnets"):
        return (cidr+bit_num)
    else:
        return (32-bit_num)

def get_mask(cidr):
    bitsLength = 32
    binarySubnetMask = ""

    for i in range(1, bitsLength + 1):
        if (i <= cidr):
            binarySubnetMask+="1"
        else:
            binarySubnetMask += "0"
    binarySubnetMaskToDecimal = int(binarySubnetMask, 2)
    subnetMask = calc_address_from_decimal(binarySubnetMaskToDecimal)
    #print(subnetMask)
    return subnetMask



###Calculates regular ip address, in suitable format, from a decimal representation
###Accepts decimal redpresantaion of the whole ip address
###Returns ip address
def calc_address_from_decimal(decAddress):
    binaryAddress = bin(decAddress)  # translate back to binary
    binaryAddress = '{:032}'.format(int(binaryAddress[2:]))  # removes 0b from the beginning
    #print(binaryAddress)
    # break into list of octets
    networkAdList = re.findall('........', binaryAddress)
                            #networkAdList=int(networkAdList, 2)
    # convert to decimal, add "."
                             #ipAddress=(".").join(networkAdList)
    ipAddress = ""
    for index, octate in enumerate(networkAdList):
        ipAddress += str(int(octate, 2))
        if (index < 3):
           ipAddress += "."
    return ipAddress



### Calculates regular ip address, in suitable format, from a decimal representation
### Accepts ip, subnetMask, cidr, newCIDR
### Returns a list of lists of id&broadcast addresses          #calculates subnets and hosts as well
### [[id,broadcast],[id,broadcast]...], from max 2 first and 2 last subnets
def calc_first_last_subnets(ip, subnetMask, cidr, newCIDR):

    NetworkAddressBroadcastlist=[]

    #group size
    addressesNum = 2 ** (32-newCIDR)

    ### Calculates usable hosts for output:
    usable_hostsNum= addressesNum-2

    ### Calculates number of subnets' for output & later use:
    subnetsNum = 2 ** (newCIDR - cidr)

    ipList= ip.split(".")
    maskList = subnetMask.split(".")

    #converts ip to a string consisting of 4 octets
    binaryIP = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(int(ipList[0]), int(ipList[1]), int(ipList[2]), int(ipList[3]))

    #converts to decimal in order to be able to use & - binary and
    decIP = int(binaryIP, 2)  # 192.1.1.1     1100 0001 0001 0001  92934992932

    #converts mask to a string consisting of 4 octets
    binaryMask = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(int(maskList[0]),int(maskList[1]),int(maskList[2]),int(maskList[3]))
    #converts to decimal in order to be able to use & - binary and
    decMask = int(binaryMask, 2)

    # calculates network address
    binaryNetworkAd = bin(decIP & decMask)    # 111111110000000  111010101010011100

    binNetworkAdToDecimal = int(binaryNetworkAd[2:], 2)  # removes '0b' from the beginning of the string,changes to decimal

    # convert to decimal, add ".", ready for output after the loop
    decNetworkAd=calc_address_from_decimal(binNetworkAdToDecimal)

    # turns the whole string to decimal, for broadcast calc.
    binaryNetworkAdToDecimal = int(binaryNetworkAd, 2)

    binaryBroadcastToDecimal = binaryNetworkAdToDecimal + addressesNum - 1  # calc. decimal from whole binary
    decBroadcast = calc_address_from_decimal(binaryBroadcastToDecimal)
    #Adds the network and broadcast addresses of the first subnet as a list, to a list
    NetworkAddressBroadcastlist.append([decNetworkAd, decBroadcast])

    if (1 < subnetsNum <= 4):

        for subnetNum in range(1, subnetsNum): # i=1 => for 2nd subnet; i=2 => for 3rd subnet; i=3 => for 4th subnet
            nextNetAdToDecimal = binaryNetworkAdToDecimal + (subnetNum * addressesNum)
            nextNetAd = calc_address_from_decimal(nextNetAdToDecimal)
            nextBroadcastToDecimal = binaryBroadcastToDecimal + subnetNum * addressesNum
            nextBroadcast = calc_address_from_decimal(nextBroadcastToDecimal)
            NetworkAddressBroadcastlist.append([nextNetAd, nextBroadcast])
    else:
        subnetNumDisplayList = [2, subnetsNum-1, subnetsNum]
        for subnetNum in subnetNumDisplayList:
            nextNetAdToDecimal = binaryNetworkAdToDecimal + subnetNum * addressesNum
            nextNetAd = calc_address_from_decimal(nextNetAdToDecimal)
            nextBroadcastToDecimal = binaryBroadcastToDecimal + subnetNum * addressesNum
            nextBroadcast = calc_address_from_decimal(nextBroadcastToDecimal)
            NetworkAddressBroadcastlist.append([nextNetAd, nextBroadcast])

    ### returns a list of network id and broadcast addressess, for max 2 first and 2 last subnets
    #return NetworkAddressBroadcastlist
        print(subnetNumDisplayList)
    print("binaryNetworkAd", binaryNetworkAd)
    print(f'{decNetworkAd}/{newCIDR}')  # Gives the network address
    print("total addresses", addressesNum)
    print("total subnets", subnetsNum)
    print(decBroadcast)
    print(NetworkAddressBroadcastlist)

def ip_input():
    ip_address = input('Please enter an IP address in the shape: '
                     'XXX.XXX.XXX.XXX: ')
    while (not is_ip(ip_address)):  # if not ip address
        ip_address = input('Please enter an IP address in the shape: '
                           'XXX.XXX.XXX.XXX: ')
    print(ip_address)
    cidr = input("\nenter the CIDR\n(CIDR is optional): ")
    while not cidr.isdigit() or not 0 <= int(cidr) <= 32:
        if(cidr == ""):
            break
        cidr = input("\nenter the CIDR number between (0-32)\n(CIDR is optional): ")
    if (not cidr):
        cidr = get_cidr(ip_address)
    cidr=int(cidr)

    partitioning = input(
        "\nDo you want the ip address to be partitioned as Hosts or "
        "Subnets?\nenter \"h\" for hosts and \"s\" for subnets:\n")
    hosts = ['h', 'H']
    subnets = ['s', 'S']
    if partitioning in hosts:
        partition_type="Hosts"
    elif partitioning in subnets:
        partition_type = "Subnets"
    else:
        while not (partitioning in hosts) and not (partitioning in subnets):
            partitioning = input(
                "\nDo you want the ip address to be partitioned as Hosts or "
                "Subnets?\nenter \"h\" for hosts and \"s\" for subnets:\n")
            if partitioning in hosts:
                partition_type = "Hosts"
            elif partitioning in subnets:
                partition_type = "Subnets"

    print("\nSelected:", partition_type)
    number_of_hosts = input("\nEnter the desired number of hosts: ")
    while not ( number_of_hosts.isdigit()):
        number_of_hosts = input("\nWrong input! You should insert number!\nEnter the desired number of hosts: ")
    bit_number = get_bits_number(int(number_of_hosts))
    if (cidr + bit_number > 32):
        print("the requested number is larger than what we have")
        exit()
    newcidr=calc_new_cidr(partition_type,bit_number, cidr)
    return (ip_address, cidr, newcidr)

def main():

    ip_address, cidr, newCidr = ip_input()
    subnetMask = get_mask(cidr)
    calc_first_last_subnets(ip_address, subnetMask, cidr, newCidr)

if __name__ == '__main__':
    main()
