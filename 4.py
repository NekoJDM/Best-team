l = []
lis = [1,56,'x',32,2.34,['s','t','r','i','n','g']]
print (lis)

a=[a+b for a in 'list' if a != 's' for b in 'soup' if b != 'u']
print (a)
l.append (23)
l.append (15)
b=[12,13,14,15]

l.extend(b)
print(l)
l.insert(0,12)
l.remove(15)
l.append(9)
print (l,'pop')
l.pop(3)
print (l)
l.sort()
print (l,'sort')
l.reverse()
print (l,'reverse')

print (l.index(23),'index 23')
print (l.count(23),'count 23')
print(l)
l.clear()
