︠796f0360-9e1f-45de-aeb6-ef4b36d54b5as︠
# secp256k1's elliptic curve y^2 = x^3  + 7
p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
a = 0
b = 7
print "Is P a prime : " , p.is_prime()

GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

ec = EllipticCurve( GF(p) ,  [a,b] )
G = ec( GX , GY )
print "Is G a basepoint :" , G.order() == ec.order()
print

#print "4G :" , 4*G  # Q1
#print "5G :" , 5*G  # Q2

d = 922142
#print "Q = dG =" , d*G  # Q3

#Q6
private_key = d
pubile_key = d*G
n = G.order()
k = ZZ.random_element(0,n-1)
k_inverse = k.inverse_mod(n)
z = ZZ.random_element(0,2**256-1)

curve_x , curve_y, space = k*G
curve_x , curve_y = (int(curve_x), int(curve_y))
print 'Curve point :' , curve_x ,curve_y , '\n'

r = curve_x % n
s = (k_inverse * (z + r*d)) % n
print 'The Signature is the pair :' , (r,s)
print

#Q7
O = n*G
Q = pubile_key
print 'check pubile key is not equal to the identitly element O :' , Q != O
print 'check pubile key lies on the curve :' , ec(Q[0],Q[1]) is not None
print 'check n*Q = O :' , n*Q == O

w = s.inverse_mod(n)
u_1 = (z*w) % n
u_2 = (r*w) % n
curve_x , curve_y, space = u_1*G + u_2*Q
curve_x , curve_y = (int(curve_x), int(curve_y))
print "Is signature valid :" , (r%n) == (curve_x%n)

︡c092c364-5165-49d7-afa6-4442e1213d26︡{"stdout":"Is P a prime :  True\n"}︡{"stdout":"Is G a basepoint : "}︡{"stdout":"True\n"}︡{"stdout":"\n"}︡{"stdout":"Curve point : 70228438663104990622978102788092995139187590747290562484975438226038745116822 39805993042130232739016653224653643950313516716355456054801269141893294610818 \n\n"}︡{"stdout":"The Signature is the pair : (70228438663104990622978102788092995139187590747290562484975438226038745116822, 43028073257605019605740744457182318075964782580929013481888568887394930548174)\n"}︡{"stdout":"\n"}︡{"stdout":"check pubile key is not equal to the identitly element O : True\n"}︡{"stdout":"check pubile key lies on the curve : True\n"}︡{"stdout":"check n*Q = O : True\n"}︡{"stdout":"Is signature valid : True\n"}︡{"done":true}
︠4b5584bf-90b5-4a31-ae94-ff9c0087bc39︠









