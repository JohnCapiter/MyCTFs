from pwn import *

passphrase = '8a80f25990e1e0154c6481ef7757a799362aade82c3013c998ffebafabafc665b0cab71d55d54c5c954fe2903f69ce3086c2cfea2ae1f478ad3d400000000000'.decode('hex')[:-1]
host = 'lab04.matesctf.org'
port = 1337
#r = process('./booklibrary')
r = remote(host, port)

r.recvuntil('$>')
# login as root
r.sendline('5')
r.recvuntil(':')
r.sendline(passphrase[:-1])

# Read the book
r.sendline('3')
# book id = 0
r.sendline('0')
r.interactive()

'''
Title:flag
Content:
matesctf{Take a walk for about 11 miles and find your password cracked}
'''
