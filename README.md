# Calculadora de Detalles de Red

Este script calcula y muestra varios detalles sobre una red IPv4 basada en una dirección IP y una máscara de subred proporcionadas por el usuario. El usuario puede ingresar la máscara de subred en formato de octetos (por ejemplo, `255.255.255.0`) o como longitud de prefijo (por ejemplo, `24`).

## Funcionalidades

- **Validación de Entrada**: Verifica que la dirección IP y la máscara de subred sean válidas antes de proceder con los cálculos.
- **Determinación de Clase de Red**: Identifica si la red es de Clase A, B, C, D o E.
- **Cálculo de Direcciones de Red**:
  - Dirección de red
  - Dirección del router (primera dirección IP utilizable)
  - Dirección de broadcast
  - Primera y última dirección IP utilizable
  - Número de subredes
  - Número de hosts por subred
  - Incremento de subredes
- **Visualización en Binario**: Muestra la máscara de subred en formato binario con colores para distinguir entre partes de red y partes de host.
- **Listado de Redes**: Lista todas las direcciones de red posibles dentro del rango de subredes calculadas.

## Uso

El script solicitará al usuario que ingrese una dirección IP y una máscara de subred. Continuará solicitando hasta que se proporcionen valores válidos.


## Requisitos

- Python 3.x
- Biblioteca `ipaddress`
- Biblioteca `termcolor`

## Instalación de Dependencias

Instala la biblioteca `termcolor` utilizando pip:

```bash
pip install termcolor
```
## Ejecución
Para ejecutar el script, usa el siguiente comando:

```bash
python nombre_del_script.py
```

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio importante antes de enviar una propuesta.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

