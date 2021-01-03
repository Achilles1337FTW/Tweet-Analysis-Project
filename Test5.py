import numpy
import pandas as pd
#numpy.log10(2)
#numpy.sqrt(4)

data = {'Name':['John', 'Jacob', 'Jingleheimer', 'Schmidt'],
        'Height':[5.5, 4.5, 5.0, 6.0],
        'Qualification':['MSC', 'MS', 'MD', 'PhD']}

df = pd.DataFrame(data)

address = ['NYC', 'LA', 'Tokyo', 'Mumbai']
df['Address'] = address

#for x in df:
#    print(df[x], '\n')

print(df['Address'])

df2 = pd.DataFrame()
print(df2)
