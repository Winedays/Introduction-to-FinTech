from ecpy.curves     import Curve,Point
from ecpy.keys       import ECPublicKey, ECPrivateKey
from ecpy.ecdsa      import ECDSA
import random
import re
import csv

'''
ECPy 0.10.0 : https://pypi.org/project/ECPy/
document : http://cslashm.github.io/ECPy/#module-ecpy.curves
'''

def readStudentsCSV( file ) :
    studentData = []
    
    f = open( file , 'r' , encoding = 'utf-8' )
    rows = csv.reader( f )
    next(rows) # skip title
    for row in rows :
        studentData.append( [row[5] , row[4]] ) # name , id
    f.close()
        
    return studentData

def saveResult( resultList ) :
    f = open( "HW6.csv" , 'w' , encoding = 'utf-8' )
    writer = csv.writer( f )
    writer.writerows( resultList )
    f.close()
    return 

# pattern replace function
def repl(p) :
    return '1' + '0' * p.group().count('1')
   
# Evaluate dG.
def dG( G , d ):
    return d*G ;
    
# convert dec integer to bin string
def dec_to_bin( dec ):
    dec = int( dec )
    # bin = bin(dec)[2:]
    bin = "{0:b}".format(dec)
    return bin
    
# convert dec integer to hex string
def dec_to_hex( dec ):
    dec = int( dec )
    hex_ = hex(dec)[2:]
    return hex_
   
# convert bin string to do a Double-and Add algorithm with Inverse Add
def convertInverseAdd( d ) :
    bin = dec_to_bin( d )
    count_invAdd = 0
    # check is prefix start with "111..."
    if re.match( r'^[1]{3,}' , bin ) :  
        bin = re.sub( r'^[1]{3,}' , repl , bin ) # convert prefix to "1000..."
        count_invAdd = 1
    # check all with "11..."
    count_invAdd += len( re.findall( r'[0][1]{2,}' , bin ) )  # find & count  all '11...' pattern
    invAdd_bin = re.sub( r'[0][1]{2,}' , repl , bin )  # replace any '111...' pattern to "100..." pattern
    double , add = doubleAdd( int(invAdd_bin,2) ) # run Double-and Add algorithm
    return invAdd_bin , double , add , count_invAdd
    
# Double-and Add algorithm
def doubleAdd( d ) :
    bin = dec_to_bin( d )
    count_double = len( bin[1:] ) # total step of double , skip the first bin on LHS.
    count_add = bin[1:].count( '1' ) # total step of add , skip the first bin on LHS.
    return count_double , count_add

def HW6() :
    # result : [<Q1_x>,<Q1_y>,"Q1_x_hex","Q1_y_hex",<Q2_x>,<Q2_y>,"Q2_x_hex","Q2_y_hex"]
    result = []
    
    # elliptic curve “secp256k1”
    curve = 'secp256k1'
    # base point of secp256k1
    GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    
    # get curve
    cv = Curve.get_curve( curve )
    # get base point & p & a & b & order of curve
    G = cv._domain['generator']
    p = cv._domain['field']
    a = cv._domain['a']
    b = cv._domain['b']
    order = cv._domain['order']
    
    # Q1 : Evaluate 4G.
    fourG = dG( G , 4 )
    result.append( fourG.x )
    result.append( fourG.y )
    # append Hex. result
    result.append( "0x"+dec_to_hex(fourG.x) )
    result.append( "0x"+dec_to_hex(fourG.y) )
    # print( "4G :" ) # Q1
    # print( " " , fourG ) # Q1
    
    # Q2 : Evaluate 5G.
    fiveG = dG( G , 5 )
    result.append( fiveG.x )
    result.append( fiveG.y )
    # append Hex. result
    result.append( "0x"+dec_to_hex(fiveG.x) )
    result.append( "0x"+dec_to_hex(fiveG.y) )
    # print( "5G :" ) # Q2
    # print( " " , fiveG ) # Q2
    
    return result 
    

def studentHW6( stu_id ) : 
    # result : [<d>,<Q3_x>,<Q3_y>,"Q3_x_hex","Q3_y_hex",<Q4>,<Q4_double_step>,<Q4_add_step>,<Q4_bin>,<Q5>,<Q5_double_step>,<Q5_add_step>,<Q5_inv_add_step>,<Q5_inv_bin>]
    result = []
    
    # elliptic curve “secp256k1”
    curve = 'secp256k1'
    # base point of secp256k1
    GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    
    # get curve
    cv = Curve.get_curve( curve )
    # get base point & p & a & b & order of curve
    G = cv._domain['generator']
    p = cv._domain['field']
    a = cv._domain['a']
    b = cv._domain['b']
    order = cv._domain['order']
    
    # d be the last 6 digits of your student ID number.
    d = int(stu_id[ -6 : ])
    result.append( d )
    
    # Q3 : Evaluate Q = dG.
    dg = dG( G , d )
    result.append( dg.x )
    result.append( dg.y )
    # append Hex. result
    result.append( "0x"+dec_to_hex(dg.x) )
    result.append( "0x"+dec_to_hex(dg.y) )
    # print( "Q = dG :" ) # Q3
    # print( " " , dg ) # Q3
    # print()
    
    # Q4 : With standard Double-and Add algorithm for scalar multiplications, how many doubles and additions respectively are required to evaluate dG?
    double , add = doubleAdd( d )
    result.append( double+add )
    result.append( double )
    result.append( add )
    result.append( dec_to_bin(d) )
    
    # Q5 : Note that it is effortless to find P from any P on a curve. If the addition of an inverse point is allowed, try your best to evaluate dG as fast as possible. Hint: 31P = 2(2(2(2(2P)))) P.
    invAdd_bin , double , add , inv_add = convertInverseAdd( d )
    result.append( double+add+inv_add )
    result.append( double )
    result.append( add )
    result.append( inv_add )
    result.append( invAdd_bin )
    
    return result 
    
    '''
    # Q6 : Take a Bitcoin transaction as you wish. Sign the transaction with a random number k and your private key d.
    private_key = d
    pubile_key = dg
    n = order
    k = random.randint(1,n-1)
    k_inverse = pow(k, n-2, n)
    z = random.randint(1,2**256-1)
        
    sign = dG( G , k )
    print( 'Curve point :' , sign )
    r = sign.x % n
    s = (k_inverse * (z + r*d)) % n
    print( 'The Signature is the pair :' , (r,s) )
    print()
    
    # Q7 : Verify the digital signature with your public key Q.
    # O = dG( G , n )
    Q = pubile_key
    # print( 'check pubile key is not equal to the identitly element O :' , Q != O )
    # print( 'check pubile key lies on the curve :' ,  cv.is_on_curve(Q) )
    # print( 'check n*Q = O :' , n*Q == O )
    
    w = pow(s, n-2, n)
    u_1 = (z*w) % n
    u_2 = (r*w) % n
    
    unsign = dG( G , u_1 ) + dG( Q , u_2 )
    print( "Is signature valid :" , (r % n) == (unsign.x % n) )
    '''
 
if __name__ == "__main__":
    # get all students data
    studentsData = readStudentsCSV( "./41883e.csv" )
    
    resultList = []
    # get result of Q1 & Q2 
    result = HW6()
    resultList.append( ["Q1_x","Q1_y","Q1_x_hex","Q1_y_hex","Q2_x","Q2_y","Q2_x_hex","Q2_y_hex"] )
    resultList.append( result )
    resultList.append( [] )
    
    # get result of each students
    resultList.append( ["Name","Std_id","d","Q3_x","Q3_y","Q3_x_hex","Q3_y_hex","Q4","Q4_double_step","Q4_add_step","Q4_bin","Q5","Q5_double_step","Q5_add_step","Q5_inv_add_step","Q5_inv_bin"] )
    for student in studentsData :
        stu_id = student[1]
        stu_id = stu_id.replace( 'a' , '0' )
        result = studentHW6( stu_id )
        resultList.append( student + result ) # append result with student info.
    
    saveResult( resultList )
    