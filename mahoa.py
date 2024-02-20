import bcrypt

# vpn='123456'
# password = bytes(vpn, 'utf-8')
# # hashed=bcrypt.hashpw(password,bcrypt.gensalt())
# # # password=b''+vpn
# # # print(password)
# # # print(hashed)
# # passql='$2b$12$gZ/f/IwpfpaUTU5.ImsqDumd.PWT7Y4DN5v.8xXQi06OwDisMUcDS'.encode('utf-8')
# #
# # # print(hashed.decode("utf-8"))
# # if(bcrypt.checkpw(passql,hashed)):
# #     print('Trung nhau')
# # else:
# #     print('khac nhau')
#
# # importing re library
import re
passwd = '0123456789'
reg = "^[0-9]{1,10}$'"

# compiling regex
# pat = re.compile(reg)

# searching regex
mat = re.search(reg, passwd)
print(mat)
# validating conditions
if mat!=None:
    print("A valid password.")
else:
    print("Please enter a password between 6-20 characters long, containing at least one uppercase letter, one digit, and the characters !!")
# from database_str import Database_str
# db=Database_str()
# print(str(db.host))
