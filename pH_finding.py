pH = float(input('Enter a pH value: '))
if pH >= 0 and pH < 7:
     print ('Acidic')
elif pH == 7:
     print ('Neutral')
elif pH > 7 and pH <= 14:
     print ('Basic')
else:
     print ('Enter a proper pH value more than or equal to 0 or less than or equal to 14.')