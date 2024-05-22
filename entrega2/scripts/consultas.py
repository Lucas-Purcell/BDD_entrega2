#Muestre todos los restaurantes que ofrezcan un plato específico (string) ingresado y que esté disponible
def consulta1(): 
    #query devuelve id, nombre y sucursal de los restaurantes que ofrecen el plato ingresado
    query = """SELECT Restaurant.id, Restaurant.nombre, Restaurant.sucursal 
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.nombre = %(nombre)s 
        AND Plato.disponibilidad = TRUE """
    return query


#Dado un estilo de plato ingresado (string) por el usuario, muestre todas las platos que pertenezcan a ese estilo y sus restricciones
def consulta5():
    #query devuelve id, nombre, sucursal de restauramt, y nombre y restricción de los platos 
    query = """SELECT Restaurant. id, Restaurant.nombre, Restaurant.sucursal, Plato.nombre, Plato.restriccion
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.estilo = %(estilo)s 
        AND Plato.disponibilidad = TRUE"""
    return query

#Muestre todos los platos y los restaurantes que los ofrecen
def consulta8():
    #query devuelve nombre del plato, id, nombre y sucursal del restaurante
    query = """SELECT Plato.nombre, Restaurant.id, Restaurant.nombre, Restaurant.sucursal 
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.disponibilidad = TRUE"""
    return query


