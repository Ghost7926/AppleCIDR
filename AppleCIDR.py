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

def main(input_file, output_file):
    unique_ips = set()
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        ips = extract_ips_from_range(line)
        unique_ips.update(ips)
    
    with open(output_file, 'w') as f_out:
        for ip in sorted(unique_ips):
            f_out.write(ip + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List out the IP Addresses in a file")
    parser.add_argument("filename", type=str, help="IP range file")
    args = parser.parse_args()
    
    if len(args.filename.split()) > 1:
        print("Error: Please provide only one file argument.")
        print("If the file name has spaces, enclose it in quotes.")
        sys.exit(1)
    
    input_file = args.filename
    output_file = 'listed_ips.txt'
    print('Listing...')
    main(input_file, output_file)
    print('Done. Have a good day!')
