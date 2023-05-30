import itertools
from itertools import *
import random
import math
import numpy as np
from datetime import datetime
rand = random.SystemRandom()

###### ADDITIONAL FUNCTIONS ######
##################################


def decomposing_number(n, a):
    exp = n - 1
    while not exp & 1:  # while exp is even
        exp >>= 1  # divide by 2
    if pow(a, exp, n) == 1:
        return True  # number is composite
    while exp < n - 1:
        if pow(a, exp, n) == n - 1:
            return True  # number is composite
        exp <<= 1  # multiply by 2
    return False  # number is probably prime


def miller_rabbin_test(n, k=20):
    for i in range(k):
        if(n == 2):
            return True
        a = rand.randrange(1, n - 1)
        if not decomposing_number(n, a):
            return False  # number is composite
    return True  # number is probably prime

#works.
def choose_prime_numbers(n):
    c = 3.38
    prime_numbers = []
    B = int(c*math.exp(1/2*(math.log2(n)*math.log2(math.log2(n)))**(1/2)))
    for i in range(2,B):
        if (miller_rabbin_test(i) == True):
            prime_numbers.append(i)
    return prime_numbers

#
def decompose(n,prime_numbers):
    decompose = []
    i = 0 
    while prime_numbers[i] * prime_numbers[i] <= n:
       while n % prime_numbers[i] == 0:
           decompose.append(i)
           n = n / prime_numbers[i]
           if(n ==1):
               return decompose
       i = i + 1
    if(n not in prime_numbers):
        return []
    elif(n > 1):
        decompose.append(prime_numbers.index(n))
    return decompose

#
def smoothness(a, n, prime_numbers,k,keys):
    for i in range(len(prime_numbers)):
        for j in range(n):
            if((a**k)==(prime_numbers[i]**j)):
                keys.append(k)
    return keys

      
def mod(a,n):
    ans = a
    while(a>=n):
        a = a - n
        if(a ==1):
            print("Your answer is", ans )
            break
    return a


##################################
##################################


########## MAINFUNCTION ##########
##################################
#
def system_of_linear_equations(a,b,n,prime_numbers,keys):
    system = []
    lenght = len(keys)
    i = 0
    while i < len(keys):
        power = pow(a,keys[i],n)
        if (power == b):
            print("random success, answer is: ", keys[i] )
            break
        var = decompose(power,prime_numbers)
        print(a,keys[i], n, pow(a,keys[i],n),)
        if(len(var)==0):
            keys.pop(i)
            i -=1
        else:
            system.append(var)
        i+=1
        
    return keys, system

#      
def linear_equations(a,b,n,prime_numbers):
    c=15
    keys = []
    for i in range(len(prime_numbers)+c):
        k = random.randrange(n)
        keys = smoothness(a, n ,prime_numbers, k, keys)
    print("keys", keys)
    keys, system = system_of_linear_equations(a,b,n,prime_numbers,keys)
    return keys,system


def edit_matrix(system,prime_numbers):
    l = len(system)
    matrix = np.array([np.zeros(len(prime_numbers))]*(l))
    print(matrix)
    
    for i in range(len(system)):
        raw = np.zeros(len(prime_numbers))
        for k in system[i]:
            raw[k]+=1
        matrix[i] = raw
    return matrix





def solve_system(keys,system,prime_numbers):
#[[indexes of prime numbers][][][]]=[k_i]#
    system = edit_matrix(system, prime_numbers)
    

    for i in range(len(keys)):
        index = 0
        len_vec = len(system[i])
        for j in range(len_vec):
            if(system[i][j] !=0):
                index+=1
        if (index == 1):
            True
        






def solve_index_calculus(a,b,n,prime_numbers):
    for i in range(n):
        k = random.randrange(n)
        var = mod(b*(a**k),n)
        vector = decompose(var,prime_numbers)
        if(len(vector)!=0):
            True
    return True

def index_calculus(a,b,n):
    prime_numbers = choose_prime_numbers(n)
    keys, system = linear_equations(a,n,prime_numbers)
    solve_index_calculus(a,b,n,prime_numbers)
    return 1

prime_numb = choose_prime_numbers(37)

print(prime_numb)
dec = decompose(37, prime_numb)
print (dec)
k,s = linear_equations(2,13,37,prime_numb)
print(k,s)

print(edit_matrix(s,prime_numb))



##################################
##################################  


