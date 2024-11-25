n=int(input("no of times leading party own the election : "))
m=int(input("no of times opposeing party own the election : "))
print("predicting the output ...")
for i in range(0,10000000):
      print("",end='')
if(n>m):
  print("ruling party will win from past election")
else:
  print("opposeing party will win from past election")
