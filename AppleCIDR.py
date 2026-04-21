import ipaddress
import argparse
import sys

def extract_ips_from_range(ip_range):

    try:
        if '-' in ip_range:
            start, end = ip_range.split('-')
            start = start.strip()
            end = end.strip()

            if '.' not in end:
                start_parts = start.split('.')
                end = '.'.join(start_parts[:-1] + [end])

            start_ip = ipaddress.ip_address(start)
            end_ip = ipaddress.ip_address(end)
            return [str(ipaddress.ip_address(ip)) for ip in range(int(start_ip), int(end_ip) + 1)]

        if '/' in ip_range:
            ip_net = ipaddress.ip_network(ip_range.strip(), strict=False)
            return [str(ip) for ip in ip_net]

        ipaddress.ip_address(ip_range.strip())
        return [ip_range.strip()]
    except ValueError:
        return [ip_range.strip()]


def read_ips_from_file(filename):
    ips = set()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            ips.update(extract_ips_from_range(line))
    return ips


def split_ips_and_other(ip_set):
    valid_ips = []
    other = []
    for item in ip_set:
        try:
            valid_ips.append(ipaddress.ip_address(item))
        except ValueError:
            other.append(item)
    return valid_ips, other


def list_mode(scope_file, output_file, exclusion_file=None):
    scope_ips = read_ips_from_file(scope_file)

    if exclusion_file:
        exclusion_ips = read_ips_from_file(exclusion_file)
        scope_ips -= exclusion_ips

    valid_ips, other = split_ips_and_other(scope_ips)
    sorted_ips = [str(ip) for ip in sorted(valid_ips)] + sorted(other)

    with open(output_file, 'w') as f_out:
        for ip in sorted_ips:
            f_out.write(ip + '\n')


def range_mode(scope_file, output_file, exclusion_file=None):

    scope_ips = read_ips_from_file(scope_file)
    valid_scope, other_scope = split_ips_and_other(scope_ips)

    scope_networks = [ipaddress.ip_network(ip) for ip in valid_scope]
    collapsed_scope = list(ipaddress.collapse_addresses(scope_networks))

    if exclusion_file:
        exclusion_ips = read_ips_from_file(exclusion_file)
        valid_excl, _ = split_ips_and_other(exclusion_ips)
        exclusion_networks = list(ipaddress.collapse_addresses(
            [ipaddress.ip_network(ip) for ip in valid_excl]
        ))

        for excl_net in exclusion_networks:
            new_scope = []
            for net in collapsed_scope:
                if excl_net == net:
                    continue  
                if excl_net.subnet_of(net):
                    new_scope.extend(net.address_exclude(excl_net))
                elif net.subnet_of(excl_net):
                    continue  
                else:
                    new_scope.append(net)  
            collapsed_scope = list(ipaddress.collapse_addresses(new_scope))

    sorted_networks = sorted(collapsed_scope, key=lambda n: (n.version, int(n.network_address)))

    with open(output_file, 'w') as f_out:
        for net in sorted_networks:
            if net.prefixlen in (32, 128):
                f_out.write(str(net.network_address) + '\n')
            else:
                f_out.write(str(net) + '\n')
        for item in sorted(other_scope):
            f_out.write(item + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert messy IP scope files into tool-digestible output. "
                    "Use 'list' to expand to individual IPs, 'range' to collapse into CIDR blocks."
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Mode of operation')

    list_parser = subparsers.add_parser('list', help='Expand all ranges/CIDRs into individual IPs')
    list_parser.add_argument('scope_file', type=str, help='File containing IP ranges to include')
    list_parser.add_argument('exclusion_file', nargs='?', type=str, help='Optional file containing IPs/ranges to exclude')

    range_parser = subparsers.add_parser('range', help='Collapse IPs/ranges into minimal CIDR blocks')
    range_parser.add_argument('scope_file', type=str, help='File containing IPs/ranges to include')
    range_parser.add_argument('exclusion_file', nargs='?', type=str, help='Optional file containing IPs/ranges to exclude')

    args = parser.parse_args()

    if args.command == 'list':
        output_file = 'listed_ips.txt'
        print('Listing...')
        list_mode(args.scope_file, output_file, args.exclusion_file)
        print(f'Done. Output written to {output_file}. Have a good day!')

    elif args.command == 'range':
        output_file = 'cidr_ranges.txt'
        print('Ranging...')
        range_mode(args.scope_file, output_file, args.exclusion_file)
        print(f'Done. Output written to {output_file}. Have a good day!')
