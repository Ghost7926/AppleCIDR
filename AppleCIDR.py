import ipaddress
import argparse

def extract_ips_from_range(item):
    item = item.replace(" ", "")  # Remove spaces
    item = item.strip()
    try:
        if '-' in item: # incase client list ip range as x.x.x.x-x
            base_ip, range_part = item.split('-')
            start_ip = ipaddress.IPv4Address(base_ip.strip())
            end_ip = ipaddress.IPv4Address(base_ip.split('.')[0] + '.' + base_ip.split('.')[1] + '.' + base_ip.split('.')[2] + '.' + range_part.strip())

            current_ip = start_ip
            while current_ip <= end_ip:
                yield str(current_ip)
                current_ip += 1
        elif '/' in item: # for CIDR notation ranges
            ip_net = ipaddress.ip_network(item, strict=False)
            for ip in ip_net.hosts():
                yield str(ip)
        else: # for domains
            ip = ipaddress.ip_address(item)
            yield str(ip)
    except ValueError:
        yield item

def read_existing_items(output_file):
    existing_items = set()
    try:
        with open(output_file, 'r') as f:
            for line in f:
                item = line.strip()
                existing_items.add(item)
    except FileNotFoundError:
        pass
    return existing_items

def main(input_file, output_file):
    existing_items = read_existing_items(output_file)

    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'a') as f_out:
        for line in lines:
            items = extract_ips_from_range(line)
            for item in items:
                if item not in existing_items:
                    f_out.write(item + '\n')
                    existing_items.add(item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List out the IP Addresses in a file")
    parser.add_argument("filename", type=str, help="IP range file")
    args = parser.parse_args()

    input_file = args.filename
    output_file = 'listed_scope.txt'
    
    print('Listing...')
    main(input_file, output_file)
    print('Done. Have a good day!')
