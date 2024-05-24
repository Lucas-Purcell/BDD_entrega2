#REVISAR LOS OUTPUTS QUE SE MUESTRAN, VER SI ARGEGAMOS MÁS O SI SACAMOS ALGUNAS. 


#Muestre todos los restaurantes que ofrezcan un plato específico (string) ingresado y que esté disponible
def consulta1(): 
    #query devuelve id, nombre y sucursal de los restaurantes que ofrecen el plato ingresado
    query = """SELECT Restaurant.id, Restaurant.nombre, Restaurant.sucursal 
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.nombre = %(nombre)s 
        AND Plato.disponibilidad = TRUE
        AND Restaurant.vigente = TRUE"""
    return query

def consulta4():
    #query devuelve nombre del plato, id, nombre y sucursal del restaurante, nombre de empresa
    query = """SELECT Plato.nombre, Res_em.id_restaurant, Res_em.nombre_restaurant, Res_em.sucursal, Res_em.nombre_empresa
        FROM Plato
        JOIN PlatoRestaurant ON Plato.id = PlatoRestaurant.plato_id
        JOIN (SELECT Restaurant.id as id_restaurant, Restaurant.nombre as nombre_restaurant, Restaurant.sucursal, Empresa.nombre as nombre_empresa
                    FROM Restaurant
                    JOIN ConvenioEmpresaRestaurant ON Restaurant.id = ConvenioEmpresaRestaurant.restaurant_id
                    JOIN Empresa ON Empresa.id = ConvenioEmpresaRestaurant.empresa_id
                    WHERE Restaurant.vigente = TRUE) AS Res_em ON PlatoRestaurant.restaurant_id = Res_em.id_restaurant
        WHERE Plato.estilo = %(estilo)s 
        AND Plato.disponibilidad = TRUE"""
    
    return query


#Dado un estilo de plato ingresado (string) por el usuario, muestre todas las platos que pertenezcan a ese estilo y sus restricciones
def consulta5():
    #query devuelve id, nombre, sucursal de restauramt, y nombre y restricción de los platos 
    query = """SELECT Restaurant. id, Restaurant.nombre, Restaurant.sucursal, Plato.nombre, Plato.restriccion
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.estilo = %(estilo)s 
        AND Plato.disponibilidad = TRUE
        AND Restaurant.vigente = TRUE"""
    return query

#Muestre todos los platos y los restaurantes que los ofrecen
def consulta8():
    #query devuelve nombre del plato, id, nombre y sucursal del restaurante
    query = """SELECT Plato.nombre, Restaurant.id, Restaurant.nombre, Restaurant.sucursal 
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.disponibilidad = TRUE
        AND Restaurant.vigente = TRUE"""
    return query


#Dado una un alergeno ingresado por el usuario (string), muestre todos los platos que lo contengan en sus ingredientes (Ejemplo: maní)
def consulta10():
    #query devuelve id, nombre y sucursal de restauramt, y nombre de los platos
    query = """SELECT Restaurant.id, Restaurant.nombre, Restaurant.sucursal, Plato.nombre 
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.ingredientes LIKE %(alergeno)s 
        AND Plato.disponibilidad = TRUE"""
    return query
