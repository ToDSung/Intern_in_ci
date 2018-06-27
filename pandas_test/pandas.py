
import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(10, 4), columns=['A', 'B', 'C', 'D'])
print(df)

#           A         B         C         D
# 0  0.884505  0.280714 - 0.291447 - 0.274222
# 1  0.868194  1.646631 - 0.379584 - 0.417132
# 2 - 1.286504  0.409008  0.042410  2.291191
# 3 - 0.730055 - 0.226875 - 0.328384  1.878240
# 4  1.010964  0.835222 - 1.632600 - 1.187731
# 5 - 0.626689 - 0.629906 - 1.352317  0.449757
# 6 - 2.182064  1.135211  1.453380  0.774203
# 7  0.173441  0.447666  1.351563  1.324603
# 8 - 0.553088  0.430695  0.492865  1.350175
# 9  1.975406  0.868987  1.060937 - 1.893944

pop = df.pop('C')

print(pop)

# 0 - 0.291447
# 1 - 0.379584
# 2    0.042410
# 3 - 0.328384
# 4 - 1.632600
# 5 - 1.352317
# 6    1.453380
# 7    1.351563
# 8    0.492865
# 9    1.060937
# Name: C, dtype: float64

print(df)

#           A         B         D
# 0  0.884505  0.280714 - 0.274222
# 1  0.868194  1.646631 - 0.417132
# 2 - 1.286504  0.409008  2.291191
# 3 - 0.730055 - 0.226875  1.878240
# 4  1.010964  0.835222 - 1.187731
# 5 - 0.626689 - 0.629906  0.449757
# 6 - 2.182064  1.135211  0.774203
# 7  0.173441  0.447666  1.324603
# 8 - 0.553088  0.430695  1.350175
# 9  1.975406  0.868987 - 1.893944

#dict to dataframe
data = {'state': ['Ohino', 'Ohino', 'Ohino', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}

df = pd.DataFrame(data, index=['one', 'two', 'three', 'four', 'five'],
               columns=['year', 'state', 'pop', 'debt'])

print(df)

#        year   state  pop debt
# one    2000   Ohino  1.5  NaN
# two    2001   Ohino  1.7  NaN
# three  2002   Ohino  3.6  NaN
# four   2001  Nevada  2.4  NaN
# five   2002  Nevada  2.9  NaN

print(df[['year', 'state']])
print(df.loc[:, ['year', 'state']])

#        year   state
# one    2000   Ohino
# two    2001   Ohino
# three  2002   Ohino
# four   2001  Nevada
# five   2002  Nevada

print(df.loc['two':'four', ['year', 'state']])

#        year   state
# two    2001   Ohino
# three  2002   Ohino
# four   2001  Nevada

print(df.loc[['two','four'], ['year', 'state']])

#       year   state
# two   2001   Ohino
# four  2001  Nevada

print(df.loc['five'])

# year       2002
# state    Nevada
# pop         2.9
# debt        NaN
# Name: five, dtype: object

print(df.iloc[1:3])

#        year  state  pop debt
# two    2001  Ohino  1.7  NaN
# three  2002  Ohino  3.6  NaN

print(df.iloc[1:3, 1])

# two      Ohino
# three    Ohino
# Name: state, dtype: object

print(df.loc[:, lambda df: ['pop', 'debt']])

#        pop debt
# one    1.5  NaN
# two    1.7  NaN
# three  3.6  NaN
# four   2.4  NaN
# five   2.9  NaN

print(df.loc[lambda df: df['pop'] > 2, :])

#        year   state  pop debt
# three  2002   Ohino  3.6  NaN
# four   2001  Nevada  2.4  NaN
# five   2002  Nevada  2.9  NaN
