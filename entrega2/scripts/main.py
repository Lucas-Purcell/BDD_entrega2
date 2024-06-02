from restaurant import restaurant
from plato import plato
from comuna import comuna
from empresa import empresa 
from despachador import despachador
from usuario import usuario
from direccion import direccion
from platorestaurant import platoRestaurant
from pedido import pedido
from suscripcion import suscripcion
from despachadorempresa import despachadorEmpresa
from contenidopedido import contenidoPedido
from direccionusuario import direccionUsuario
from convenioempresarestaurant import convenioEmpresaRestaurant
from despacho import despacho
from serviciodespacho import servicioDespacho

def main():
    error_text = []
    error_text.append(restaurant())
    error_text.append(plato())
    error_text.append(comuna())
    error_text.append(empresa())
    error_text.append(despachador())
    error_text.append(usuario())
    error_text.append(direccion())
    error_text.append(platoRestaurant())
    error_text.append(pedido())
    error_text.append(suscripcion())
    error_text.append(despachadorEmpresa())
    error_text.append(contenidoPedido())
    error_text.append(direccionUsuario())
    error_text.append(convenioEmpresaRestaurant())
    error_text.append(despacho())
    error_text.append(servicioDespacho())

    with open('error.txt', 'w') as f:
        for text in error_text:
            for line in text:
                if not ('UniqueViolation' in str(line)) and not ('ForeignKeyViolation' in str(line)):
                    if 'Tabla' in str(line):
                        f.write(str(line) + '\n')
                    else:
                        f.write('\t'.join([str(s) for s in line]) + '\n')
main()

