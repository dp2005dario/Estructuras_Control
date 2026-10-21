mi_lista = ["Platano","Pera","Sandia","Manzana"]
enumerate
for i, fruta in enumerate (mi_lista):
    print(f"{i}-{fruta}")
    
    
lista_a = [1,2,3,4,5]
lista_b =[10,20,30,40,50]

print(zip(lista_a, lista_b)) #Codigo
print(list(zip(lista_a,lista_b)))


temp =zip(lista_a,lista_b)
lista = list(temp)
print(f"{list(temp)}Aqui esat") #Con todo este proceso del temp la lista sale vacio
lista_suma= list(map(sum,zip(lista_a,lista_b)))
lista_suma =  list(map(lambda x: sum(x), zip(lista_a,lista_b))) #Hace lo mismo pero con iterator


### ESTO NO CAE EN LA PRUEBA ES DE CURIOSIDAD PARA ENTENDER MAS###