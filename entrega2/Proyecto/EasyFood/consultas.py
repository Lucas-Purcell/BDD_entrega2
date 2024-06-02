#Muestre todos los restaurantes que ofrezcan un plato específico (string) ingresado y que esté disponible
def consulta1(): 
    #query devuelve id, nombre y sucursal de los restaurantes que ofrecen el plato ingresado
    query = """SELECT DISTINCT Restaurant.nombre as nombre_restaurant, Restaurant.sucursal, Restaurant.direccion
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.nombre ILIKE %(nombre)s 
        AND Plato.disponibilidad = TRUE
        AND Restaurant.vigente = TRUE"""
    return query

#Muestre todos los pedidos de un usuario específico ingresado (email string) y su gasto mensual (solo los pedidos concretados)
def consulta2():
    query = """SELECT Pedido.fecha, Pedido.estado
        FROM Pedido
        JOIN Usuario ON Pedido.usuario_id = Usuario.id
        WHERE Usuario.email ILIKE %(email)s
        ORDER BY Pedido.fecha DESC"""
    
    query1 = """SELECT month, year, gasto_mensual_pedido, SUM(suscripcion_mesual) as gasto_mensual_suscripciones, (gasto_mensual_pedido + SUM(suscripcion_mesual)) as gasto_mensual_total
                FROM  (SELECT month, year, SUM(gasto_mensual_pedido) as gasto_mensual_pedido,
                    CASE
                        WHEN (Suscripcion.ciclo = 'anual' AND Suscripcion.fecha_ultimo_pago >= (TO_DATE(CONCAT(year, '/', month, '/', 1), 'YYYY/MM/DD') - INTERVAL '1' YEAR) AND Empresa.vigente = TRUE)  
                        THEN Empresa.precio_anual / 12
                        WHEN (Suscripcion.ciclo = 'mensual' AND Suscripcion.fecha_ultimo_pago >= (TO_DATE(CONCAT(year, '/', month, '/', 1), 'YYYY/MM/DD') - INTERVAL '1' MONTH) AND Empresa.vigente = TRUE)
                        THEN Empresa.precio_mensual
                        ELSE 0
                    END AS suscripcion_mesual
        FROM (SELECT month, year, SUM(gasto_pedido) as gasto_mensual_pedido, gasto_pedido.usuario_id
                FROM (SELECT Pedido.id, gasto_pedido_comida.month, gasto_pedido_comida.year, (SUM(gasto_pedido_comida.precio_comida) + SUM(gasto_pedido_comida.precio_despacho)) as gasto_pedido, usuario.id as usuario_id
                FROM Pedido
                JOIN (SELECT Pedido.id as pedido_id, usuario.id as usuario_id,
                        EXTRACT(YEAR FROM Pedido.fecha) as year,
                        EXTRACT(MONTH FROM Pedido.fecha) as month,
                        CASE
                            WHEN (Suscripcion.ciclo = 'anual' AND Suscripcion.fecha_ultimo_pago >= (NOW() - INTERVAL '1' YEAR) AND Empresa.vigente = TRUE)  
                            OR  (Suscripcion.ciclo = 'mensual' AND Suscripcion.fecha_ultimo_pago >= (NOW() - INTERVAL '1' MONTH) AND Empresa.vigente = TRUE)
                            THEN 0
                            ELSE Empresa.precio_despacho
                        END AS precio_despacho,
                        SUM(Plato.precio * ContenidoPedido.cantidad) as precio_comida
                    FROM Pedido
                    JOIN Despacho ON Despacho.pedido_id = Pedido.id
                    JOIN Empresa ON Despacho.empresa_id = Empresa.id
                    JOIN ContenidoPedido ON ContenidoPedido.pedido_id = Pedido.id
                    JOIN Plato ON ContenidoPedido.plato_id = Plato.id
                    JOIN Usuario ON Pedido.usuario_id = Usuario.id AND Usuario.email ILIKE %(email)s
                    FULL OUTER JOIN Suscripcion ON Usuario.id = Suscripcion.usuario_id AND Suscripcion.empresa_id = Empresa.id
                    WHERE Pedido.estado IN ('entregado a cliente')
                    GROUP BY Pedido.id, precio_despacho, Empresa.vigente, suscripcion.ciclo, suscripcion.fecha_ultimo_pago, usuario.id) as gasto_pedido_comida
                ON Pedido.id = gasto_pedido_comida.pedido_id
                JOIN Usuario ON Pedido.usuario_id = Usuario.id
                GROUP BY Pedido.id, gasto_pedido_comida.precio_comida, gasto_pedido_comida.precio_despacho, gasto_pedido_comida.month, gasto_pedido_comida.year, usuario.id
                ORDER BY Pedido.id) as gasto_pedido
            GROUP BY month, year, gasto_pedido.usuario_id) as gasto_mensual_pedido
        JOIN Usuario ON Usuario.id = gasto_mensual_pedido.usuario_id
        JOIN Suscripcion ON Usuario.id = Suscripcion.usuario_id
        JOIN Empresa ON Suscripcion.empresa_id = Empresa.id
        GROUP BY month, year, gasto_mensual_pedido, suscripcion.ciclo, suscripcion.fecha_ultimo_pago, empresa.vigente, empresa.precio_anual, empresa.precio_mensual) as gasto
        GROUP BY year, month, gasto_mensual_pedido
        """
    return query, query1

#Muestre todos pedidos concretados y cancelados y el valor total de ellos
def consulta3():
    #query devuelve id, nombre y email del usuario, estado del pedido, gasto total del pedido, precio de la comida y precio del despacho
    query = """SELECT Pedido.id, Usuario.nombre, Usuario.email, Pedido.estado, (SUM(gasto_pedido_comida.precio_comida) + SUM(gasto_pedido_comida.precio_despacho)) as gasto_pedido, gasto_pedido_comida.precio_comida, gasto_pedido_comida.precio_despacho
            FROM Pedido
            JOIN (SELECT DISTINCT Pedido.id as pedido_id, Usuario.nombre, Usuario.email,
                    CASE
                        WHEN (Suscripcion.ciclo = 'anual' AND Suscripcion.fecha_ultimo_pago >= (NOW() - INTERVAL '1' YEAR) AND Empresa.vigente = TRUE)  
                        OR  (Suscripcion.ciclo = 'mensual' AND Suscripcion.fecha_ultimo_pago >= (NOW() - INTERVAL '1' MONTH) AND Empresa.vigente = TRUE)
                        THEN 0
                        ELSE Empresa.precio_despacho
                    END AS precio_despacho,
                    SUM(Plato.precio * ContenidoPedido.cantidad) as precio_comida
                FROM Pedido
                JOIN Despacho ON Despacho.pedido_id = Pedido.id
                JOIN Empresa ON Despacho.empresa_id = Empresa.id AND Empresa.vigente = TRUE
                JOIN ContenidoPedido ON ContenidoPedido.pedido_id = Pedido.id
                JOIN Plato ON ContenidoPedido.plato_id = Plato.id
                JOIN Usuario ON Pedido.usuario_id = Usuario.id
                FULL OUTER JOIN Suscripcion ON Usuario.id = Suscripcion.usuario_id AND Suscripcion.empresa_id = Empresa.id
                WHERE Pedido.estado IN ('entregado a cliente', 'Cliente cancela', 'delivery cancela', 'restaurant cancela')
                GROUP BY Pedido.id, precio_despacho, Empresa.vigente, suscripcion.ciclo, suscripcion.fecha_ultimo_pago, usuario.nombre, usuario.email) as gasto_pedido_comida
            ON Pedido.id = gasto_pedido_comida.pedido_id
            JOIN Usuario ON Pedido.usuario_id = Usuario.id
            GROUP BY Pedido.id, usuario.nombre, usuario.email, Pedido.estado, gasto_pedido_comida.precio_comida, gasto_pedido_comida.precio_despacho
            ORDER BY Pedido.id"""
    
    return query

#Dado un estilo de plato ingresado por el usuario (string) , muestre todas los platos con ese tipo, los restaurantes que las ofrecen y las opciones de delivery.
def consulta4():
    #query devuelve nombre del plato, nombre y sucursal del restaurante, nombre de empresa
    query = """SELECT DISTINCT Plato.nombre as nombre_plato, Res_em.nombre_restaurant, Res_em.sucursal, Res_em.direccion, Res_em.nombre_empresa,  Res_em.tiempo_despacho, Res_em.precio_despacho
        FROM Plato
        JOIN PlatoRestaurant ON Plato.id = PlatoRestaurant.plato_id
        JOIN (SELECT Restaurant.id as id_restaurant, Restaurant.nombre as nombre_restaurant, Restaurant.sucursal, Restaurant.direccion, Empresa.nombre as nombre_empresa, Empresa.tiempo_despacho, Empresa.precio_despacho
                    FROM Restaurant
                    JOIN ConvenioEmpresaRestaurant ON Restaurant.id = ConvenioEmpresaRestaurant.restaurant_id
                    JOIN Empresa ON Empresa.id = ConvenioEmpresaRestaurant.empresa_id
                    WHERE Restaurant.vigente = TRUE
                    AND Empresa.vigente = TRUE) AS Res_em ON PlatoRestaurant.restaurant_id = Res_em.id_restaurant
        WHERE Plato.estilo ILIKE %(estilo)s 
        AND Plato.disponibilidad = TRUE
        ORDER BY nombre_plato, nombre_restaurant, sucursal, nombre_empresa"""
    
    return query

#Dado un estilo de plato ingresado (string) por el usuario, muestre todas las platos que pertenezcan a ese estilo y sus restricciones
def consulta5():
    #query devuelve id, nombre, sucursal de restauramt, y nombre y restricción de los platos 
    query = """SELECT Plato.nombre as plato_nombre, Plato.restriccion, Restaurant.nombre as restaurant_nombre, Restaurant.sucursal, Restaurant.direccion 
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.estilo ILIKE %(estilo)s 
        AND Plato.disponibilidad = TRUE
        AND Restaurant.vigente = TRUE
        ORDER BY plato_nombre, restaurant_nombre, sucursal"""
    return query

#Dado un cliente ingresado por el usuario (email string), muestre todas las restaurantes a las que tiene acceso con sus suscripciones.

def consulta6():
    #query devuelve nombre del restaurante y nombre de la empresa
    query = """SELECT DISTINCT Restaurant.nombre as nombre_restaurant, Restaurant.sucursal, Restaurant.direccion, Empresa.nombre as nombre_empresa, Suscripcion.ciclo as tipo_suscripcion
        FROM Restaurant 
        JOIN ConvenioEmpresaRestaurant ON Restaurant.id = ConvenioEmpresaRestaurant.restaurant_id
        JOIN Empresa ON Empresa.id = ConvenioEmpresaRestaurant.empresa_id
        JOIN Suscripcion ON Empresa.id = Suscripcion.empresa_id
        JOIN Usuario ON Suscripcion.usuario_id = Usuario.id
        WHERE Usuario.email ILIKE %(email)s
        AND Restaurant.vigente = TRUE
        AND Empresa.vigente = TRUE
        AND ( (Suscripcion.ciclo = 'anual' AND Suscripcion.fecha_ultimo_pago >= (NOW() - INTERVAL '1' YEAR) )  
        OR  (Suscripcion.ciclo = 'mensual' AND Suscripcion.fecha_ultimo_pago >= (NOW() - INTERVAL '1' MONTH) ) )
        ORDER BY nombre_restaurant, sucursal, nombre_empresa, tipo_suscripcion"""

    return query

# Muestre la suma de dinero gastada por cada cliente en pedidos no incluidas en planes de suscripcion

def consulta7():
    #query devuelve nombre, email y gasto total de los usuarios
    query = """SELECT Usuario.nombre, Usuario.email, (SUM(gasto_pedido.precio_comida) + SUM(gasto_pedido.precio_despacho)) as gasto_total
        FROM Usuario
        JOIN (SELECT Pedido.id as pedido_id, Pedido.usuario_id, Empresa.id as empresa_id, Empresa.precio_despacho, SUM(Plato.precio * ContenidoPedido.cantidad) as precio_comida 
            FROM Pedido
            JOIN Despacho ON Despacho.pedido_id = Pedido.id
            JOIN Empresa ON Despacho.empresa_id = Empresa.id
            JOIN ContenidoPedido ON ContenidoPedido.pedido_id = Pedido.id
            JOIN Plato ON ContenidoPedido.plato_id = Plato.id
            JOIN Usuario ON Pedido.usuario_id = Usuario.id
            LEFT JOIN Suscripcion ON Usuario.id = Suscripcion.usuario_id AND Empresa.id = Suscripcion.empresa_id
            WHERE (Suscripcion.usuario_id IS NULL 
                    OR (Suscripcion.ciclo = 'anual' AND Suscripcion.fecha_ultimo_pago < (NOW() - INTERVAL '1' YEAR) )  
                    OR  (Suscripcion.ciclo = 'mensual' AND Suscripcion.fecha_ultimo_pago < (NOW() - INTERVAL '1' MONTH) ) )
            AND Pedido.estado = 'entregado a cliente'  
            GROUP BY Pedido.id, Pedido.usuario_id, Empresa.id, Empresa.precio_despacho) as gasto_pedido
        ON Usuario.id = gasto_pedido.usuario_id
        JOIN Pedido ON Pedido.id = gasto_pedido.pedido_id
        GROUP BY Usuario.nombre, Usuario.email"""  
    return query

#Muestre todos los platos y los restaurantes que los ofrecen
def consulta8():
    #query devuelve nombre del plato, nombre y sucursal del restaurante
    query = """SELECT Plato.nombre as nombre_plato, Restaurant.nombre as nombre_restaurant, Restaurant.sucursal, Restaurant.direccion
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.disponibilidad = TRUE
        AND Restaurant.vigente = TRUE
        ORDER BY nombre_plato, nombre_restaurant, sucursal"""
    return query

#Dado un numero (1-5) ingresado por el usuario, muestre todos las evaluaciones de Clientes, Delivery, Despachador superiores o iguales a  ́el

def consulta9(tipo: str):

    if tipo == 'cliente':
        #query devuelve id, evaluación del cliente y email del usuario
        query = """SELECT Pedido.id, Usuario.nombre as cliente, Usuario.email, Pedido.evaluacion_cliente
        FROM Pedido
        JOIN Usuario ON Pedido.usuario_id = Usuario.id
        WHERE Pedido.evaluacion_cliente >= %(numero)s
        ORDER BY Pedido.id"""
        return query
    elif tipo == 'delivery':
        #query devuelve id, evaluación del delivery y nombre de la empresa de delivery
        query = """SELECT DISTINCT Pedido.id, Pedido.evaluacion_servicio as evaluacion_delivery, Empresa.nombre as empresa
        FROM Pedido 
        JOIN Despacho ON Pedido.id = Despacho.pedido_id
        JOIN Empresa ON Despacho.empresa_id = Empresa.id
        WHERE Pedido.evaluacion_servicio >= %(numero)s
        ORDER BY Pedido.id"""
        return query
    elif tipo == 'despachador':
        #query devuelve id, evaluación del despachador y nombre del despachador
        query = """SELECT DISTINCT Pedido.id, Pedido.evaluacion_servicio as evaluacion_despachador, Despachador.nombre as despachador
        FROM Pedido 
        JOIN Serviciodespacho ON Pedido.id = Serviciodespacho.pedido_id
        JOIN Despachador ON Serviciodespacho.despachador_id = Despachador.id
        WHERE Pedido.evaluacion_servicio >= %(numero)s
        ORDER BY Pedido.id"""
        return query


#Dado una un alergeno ingresado por el usuario (string), muestre todos los platos que lo contengan en sus ingredientes (Ejemplo: maní)
def consulta10():
    #query devuelve id, nombre y sucursal de restauramt, y nombre de los platos
    query = """SELECT Plato.nombre as nombre_plato, Restaurant.nombre as nombre_restaurant, Restaurant.sucursal, Restaurant.direccion
        FROM Plato
        JOIN Platorestaurant ON Plato.id = Platorestaurant.plato_id 
        JOIN Restaurant ON Platorestaurant.restaurant_id = Restaurant.id
        WHERE Plato.ingredientes ILIKE %(alergeno)s 
        AND Plato.disponibilidad = TRUE
        AND Restaurant.vigente = TRUE"""
    return query