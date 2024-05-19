import ipaddress
from termcolor import colored

def print_colored_binary(binary_str, network_class):
    colored_str = ""
    for i, bit in enumerate(binary_str):
        if i != 0 and i % 8 == 0:
            colored_str += '.'
        if network_class == "Clase A" and i >= 8 and bit == '1':
            colored_str += colored(bit, 'light_red', attrs=['bold'])
        elif network_class == "Clase B" and i >= 16 and bit == '1':
            colored_str += colored(bit, 'light_red', attrs=['bold'])
        elif network_class == "Clase C" and i >= 24 and bit == '1':
            colored_str += colored(bit, 'light_red', attrs=['bold'])
        elif bit == '1':
            colored_str += colored(bit, 'cyan', attrs=['bold'])
        else:
            colored_str += colored(bit, 'light_yellow', attrs=['bold'])
    return colored_str

def calculate_network_details(ip, subnet_mask):
    # Convertir la dirección IP y la máscara de subred a objetos ipaddress.IPv4Network
    network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)

    # Obtener los detalles de la red
    network_bits = network.prefixlen
    subnet_binary = network.netmask.packed
    network_class = get_network_class(network.network_address)
    network_address = network.network_address
    router_address = network.network_address + 1
    broadcast_address = network.broadcast_address
    first_ip = network.network_address + 1
    last_ip = network.broadcast_address - 1
    num_hosts = network.num_addresses - 2

    # Determinar si cada parte de la máscara de subred pertenece a red o host
    net_or_host_parts = []
    if network_class == "Clase A":
        net_or_host_parts = ["Network", "Host", "Host", "Host"]
    elif network_class == "Clase B":
        net_or_host_parts = ["Network", "Network", "Host", "Host"]
    elif network_class == "Clase C":
        net_or_host_parts = ["Network", "Network", "Network", "Host"]

    # Convertir la máscara de subred en una lista de enteros
    subnet_binary_list = [int(bit) for bit in ''.join(format(byte, '08b') for byte in subnet_binary)]

    # Calcular el número de subredes
    num_subnets = 0
    if network_class == "Clase A":
        num_subnets = subnet_binary_list[8:].count(1)
        num_host_bits = subnet_binary_list[8:].count(0)
    elif network_class == "Clase B":
        num_subnets = subnet_binary_list[16:].count(1)
        num_host_bits = subnet_binary_list[16:].count(0)
    elif network_class == "Clase C":
        num_subnets = subnet_binary_list[24:].count(1)
        num_host_bits = subnet_binary_list[24:].count(0)

    # Calcular las direcciones de las redes
    network_addresses = []
    if network_class == "Clase A":
        network_addresses.append(ipaddress.IPv4Address(str(network.network_address).split('.')[0] + ".0.0.0"))
        for _ in range((2 ** num_subnets) - 1):
            network_addresses.append(network_addresses[-1] + (2 ** (8 - num_subnets)))
    elif network_class == "Clase B":
        network_addresses.append(ipaddress.IPv4Address(str(network.network_address).split('.')[0] + "." + str(network.network_address).split('.')[1] + ".0.0"))
        for _ in range((2 ** num_subnets) - 1):
            network_addresses.append(network_addresses[-1] + (2 ** (16 - num_subnets)))
    elif network_class == "Clase C":
        network_addresses.append(ipaddress.IPv4Address(str(network.network_address).split('.')[0] + "." + str(network.network_address).split('.')[1] + "." + str(network.network_address).split('.')[2] + ".0"))
        for _ in range((2 ** num_subnets) - 1):
            network_addresses.append(network_addresses[-1] + (2 ** (24 - num_subnets)))

    return {
        "\nMáscara de red en octeto": network.netmask,
        "Máscara de red en bits": network_bits,
        "\nMáscara de subred en binario": print_colored_binary(''.join(format(byte, '08b') for byte in subnet_binary), network_class),
        "Partes de la máscara de subred": print_colored_parts(net_or_host_parts),
        "\nClase de la red": network_class,
        "\nDirección de Red": str(network_address),
        "Dirección del Router": str(router_address),
        "Dirección de Broadcast": str(broadcast_address),
        "\nPrimera dirección IP": str(first_ip),
        "Última dirección IP": str(last_ip),
        "\nNúmero de Subredes": f"2^{num_subnets} = {2 ** num_subnets}",
        "Número de Hosts": f"(2^{num_host_bits}) - 2 = {num_hosts}",
        "Incremento ÷ Redes": f"8 - {num_subnets} = {8-num_subnets}  ➜   2 ^ {8-num_subnets} = {2 ** (8-num_subnets)}", 
        "\nRedes": [str(addr) for addr in network_addresses]
    }

def get_network_class(ip_address):
    first_octet = ip_address.packed[0]
    if first_octet < 128:
        return "Clase A"
    elif first_octet < 192:
        return "Clase B"
    elif first_octet < 224:
        return "Clase C"
    elif first_octet < 240:
        return "Clase D (Multicast)"
    else:
        return "Clase E"

def get_subnet_mask(mask_input):
    # Verificar si la entrada es una longitud de prefijo
    if mask_input.isdigit():
        prefix_length = int(mask_input)
        if prefix_length >= 0 and prefix_length <= 32:
            return str(ipaddress.IPv4Network(f"0.0.0.0/{prefix_length}", strict=False).netmask)
    # Si no es una longitud de prefijo válida, asumir que es una máscara en formato de octetos
    try:
        ipaddress.IPv4Address(mask_input)
        return mask_input
    except ValueError:
        return None

def print_colored_parts(parts_list):
    colored_parts = []
    for part in parts_list:
        if part == "Network":
            colored_parts.append(colored(part, 'cyan', attrs=['bold']))
        else:
            colored_parts.append(colored(part, 'light_yellow', attrs=['bold']))
    return colored_parts

if __name__ == "__main__":
    while True:
        ip = input("\nDirección IP: ")
        subnet_mask_input = input("Máscara de Subred (puede ser en formato de octetos o longitud de prefijo): ")

        subnet_mask = get_subnet_mask(subnet_mask_input)

        if subnet_mask is not None:
            try:
                ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
                # Si se llega a esta línea, la dirección IP y la máscara son válidas
                break
            except ValueError:
                print("Dirección IP o máscara de subred no válida. Inténtalo de nuevo.")
        else:
            print("Formato de máscara de subred no válido. Inténtalo de nuevo.")

    details = calculate_network_details(ip, subnet_mask)
    
    for key, value in details.items():
        if key == "Partes de la máscara de subred":
            parts = '.'.join(value)
            print(f"{key}: {parts}")
        elif key == "Máscara de subred en binario":
            print(f"{key}: {value}")
        elif key == "Redes":
            print(f"{key}:\n")
            for addr in value:
                print(addr)
            print()
        else:
            print(f"{key}: {value}")
