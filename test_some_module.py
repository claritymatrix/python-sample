# import some_module
from datetime import datetime,date,time

from some_module import PI as pi,f as gf


#result = some_module.f(5)

result = gf(5)


print(result)
template = '{0:.2f} {1:s} are worth US${2:d}'

print(template.format(4.5560,'Argentine Pesos',1))

val = "中国"


print(val)

print(val.encode('utf-8'))

print(type(val.encode('utf-8')))
dt = datetime(2019,12,31,22,10,21)


print(dt)

print(dt.day)
