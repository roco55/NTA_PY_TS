import itertools
from itertools import *
import random
import math
import numpy as np
from datetime import datetime
rand = random.SystemRandom()

###### ADDITIONAL FUNCTIONS ######
##################################
def gcd(a, n):
    u = [1, 0]
    v = [0, 1]
    if(a ==0 or n ==0):
        return(0,[],[])
    if a > n:
        rn = a
        rn1 = n
        rn2 = 1
    elif a < n:
        rn = n
        rn1 = a
        rn2 = 1
        u,v = v, u
    else:
        rn2 = 0
        return(0,[],[])
    i = 0
    while rn2 != 0:
        i += 1
        q = int(rn / rn1)
        u.append(u[i-1]-u[i]*q)
        v.append(v[i-1]-v[i]*q)
        rn2 = rn - q * rn1
        #print(f"{rn} = {rn1}*{q} + {rn2}")
        rn = rn1
        rn1 = rn2
    return (abs(rn),u,v)

def inverse(a,n):
    u = gcd(a,n)[1]
    #print(u)
    invers = u[len(u)-2]
    if(invers<0):
        invers+=n
    return invers


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
def smoothness(a,b, n, prime_numbers,k,keys,keys3):
    for i in range(len(prime_numbers)):
        for j in range(n):
            if(len(decompose(b*(a**k),prime_numbers))>0):
                keys.append(k)
                keys3.append([b,k])
                return keys,keys3

      
def mod(a,n):
    ans = a
    while(a>=n):
        a = a - n
        #if(a ==1):
            #print("Your answer is", ans )
            #break
    if(a<0):
        a=a+n
    return a

def inverse_modulo(a, n):
    x, y = 1, 0
    n_0 = n
    if n == 1:
        return 0
    while a > 1:
        q = a // n
        t = n
        n = a % n
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + n_0
    return int(x)


##################################
##################################


########## MAINFUNCTION ##########
##################################
#
def system_of_linear_equations(a,b,b1,n,prime_numbers,keys,keys3):
    system = []
    lenght = len(keys)
    i = 0
    while i < len(keys):
        if(b1 == 1 ):
            power =pow(a,keys[i],n)
        else:
            power = mod(b1*pow(a,keys[i],n),n)
        
        #if (power == b):
        #   print("random success, answer is: ", keys[i] )
        #   break
        var = decompose(power,prime_numbers)
        #print(a,keys[i], n, pow(a,keys[i],n))
        if(len(var)==0):
            keys.pop(i)
            if(len(keys3)!= 0):
                keys3.pop(i)
            i -=1
        else:
            system.append(var)
        i+=1
        
    return keys, system , keys3

#      
def linear_equations(a,b,n,prime_numbers):
    c=15
    keys3= []
    keys = []
    k = random.sample(range(1, n + 1), len(prime_numbers)+c)
    for i in range(len(prime_numbers)+c):
        keys = smoothness(a,1, n ,prime_numbers, k[i], keys, keys3)[0]
    #print("keys", keys)
    keys, system = system_of_linear_equations(a,b,1,n,prime_numbers,keys,keys3)[0],system_of_linear_equations(a,b,1,n,prime_numbers,keys,keys3)[1]
    return keys,system


def edit_matrix(system,prime_numbers):
    l = len(system)
    matrix = np.array([np.zeros(len(prime_numbers))]*(l))
    for i in range(len(system)):
        raw = np.zeros(len(prime_numbers))
        for k in system[i]:
            raw[k]+=1
        matrix[i] = raw
    return matrix






def solve_system(n,keys,system,prime_numbers):
    system = edit_matrix(system, prime_numbers)
    keys = np.array(keys)
    l = len(system)
    print(system, keys)
    good_vectors = []
    good_answers = []
    for i in range(len(keys)):
        index = 0
        len_vec = len(system[i])
        var = 0
        for j in range(len_vec):
            var = int(var + system[i][j])
            if(system[i][j] !=0):
                index+=1
                ind = j
        if (index == 1):
            if(gcd(var,(n-1))[0] != 1):
                continue
            else:
                keys[i] = mod(keys[i]*inverse(system[i][ind],(n-1)),n-1)
                system[i][ind] = 1
                good_vectors.append(list(system[i]))
                good_answers.append(keys[i])
    #after this we have array of ez numbers *x = num*
    
    return keys, system

            


def unsolved_answers(a,b,n,prime_numbers):
    keys2 = []
    keys3 = []

    l = random.sample(range(1, n), len(prime_numbers))
    for i in range(len(prime_numbers)):
        keys2,keys3 = smoothness(a,b, n ,prime_numbers, l[i], keys2, keys3)
    #print("keys2", keys2)
    keys2, system2 = system_of_linear_equations(a,1,b,n,prime_numbers,keys2,keys3)[2],system_of_linear_equations(a,b,b,n,prime_numbers,keys2,keys3)[1]
    
    return keys2,system2




def solve_index_calculus(keys,system,keys2,system2):
    x = 0
    print(keys2[0][1])
    print("apappa",keys,"apappa",system,"apappa",keys2,"apappa",system2)
    for i in range(len(system2)):
        idx = np.where((system == (system2[i])).all(axis=1))
        if(len(idx[0])>0):
            if(len(idx)>1):
                idx = int(idx[0])
                print(keys[idx], keys2[i][1])
                x = mod(keys[idx] - keys2[i][1],n-1)
                return x
            else:
                print(keys[idx], keys2[i][1])
                x = mod(keys[idx] - keys2[i][1],n-1)
                return x
    


def index_calculus(a,b,n):
    prime_numbers = choose_prime_numbers(n)
    keys, system = linear_equations(a,b,n,prime_numbers)
    keys, system = solve_system(n,keys,system,prime_numbers)
    keys2, system2 = unsolved_answers(a,b,n,prime_numbers)
    system2 = edit_matrix(system2,prime_numbers)
    x = solve_index_calculus(keys,system,keys2,system2)
    return x

a = 2
b = 13
n = 37

print("X = ",index_calculus(a,b,n))


# prime_numbers = choose_prime_numbers(n)
# print(prime_numbers)
# key, sys = linear_equations(a, b, n, prime_numbers)
# print(key, sys)
# matrix = edit_matrix(sys,prime_numbers)

# print(solve_system(n,key,sys, prime_numbers))


# key2, sys2 = unsolved_answers(a, b, n, prime_numbers)
# print(key2, sys2)
# matrix2 = edit_matrix(sys2,prime_numbers)
# print(matrix2)
##################################
##################################  


