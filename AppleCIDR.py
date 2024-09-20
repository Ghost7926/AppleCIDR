import ipaddress
import argparse
import sys

def extract_ips_from_range(ip_range):
    try:
        # Handle 'x.x.x.x-y' format
        if '-' in ip_range:
            start, end = ip_range.split('-')
            start = start.strip()
            end = end.strip()
            
            # If end is not a full IP, complete it using the start IP
            if '.' not in end:
                start_parts = start.split('.')
                end = '.'.join(start_parts[:-1] + [end])
            
            start_ip = ipaddress.ip_address(start)
            end_ip = ipaddress.ip_address(end)
            return [str(ipaddress.ip_address(ip)) for ip in range(int(start_ip), int(end_ip) + 1)]
        
        # Handle CIDR notation
        if '/' in ip_range:
            ip_net = ipaddress.ip_network(ip_range.strip(), strict=False)
            return [str(ip) for ip in ip_net]
        
        # Handle single IP address
        ipaddress.ip_address(ip_range.strip())
        return [ip_range.strip()]
    except ValueError:
        # If it's not a valid IP or range, assume it's a domain name and return as is
        return [ip_range.strip()]

def read_ips_from_file(filename):
    ips = set()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            ips.update(extract_ips_from_range(line))
    return ips

def main(scope_file, output_file, exclusion_file=None):
    scope_ips = read_ips_from_file(scope_file)
    
    if exclusion_file:
        exclusion_ips = read_ips_from_file(exclusion_file)
        scope_ips -= exclusion_ips
    
    with open(output_file, 'w') as f_out:
        for ip in sorted(scope_ips):
            f_out.write(ip + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List out the IP Addresses in a file, with optional exclusions")
    parser.add_argument("scope_file", type=str, help="File containing IP ranges to include")
    parser.add_argument("exclusion_file", nargs='?', type=str, help="Optional file containing IP ranges to exclude")
    args = parser.parse_args()

    scope_file = args.scope_file
    exclusion_file = args.exclusion_file
    output_file = 'listed_ips.txt'

    print('Listing...')
    main(scope_file, output_file, exclusion_file)
    print('Done. Have a good day!')
