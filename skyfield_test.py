import skyfield

if skyfield.VERSION < (1, 24):
    print('Too old')
else:
  print(skyfield.VERSION)
