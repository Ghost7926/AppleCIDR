import ipaddress
import argparse
import sys

def extract_ips_from_range(ip_range):
    try:
        ip_net = ipaddress.ip_network(ip_range, strict=False)
        return list(map(str, ip_net.hosts()))
    except ValueError:
        return []

def main(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f_out:
        for line in lines:
            line = line.strip()
            ips = extract_ips_from_range(line)
            for ip in ips:
                f_out.write(ip + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List out the IP Addresses in a file")
    parser.add_argument("filename", type=str, help="IP range file")
    args = parser.parse_args()

    if len(args.filename.split()) > 1:
        print("Error: Please provide only one file argument.")
        print("If the file name has spaces, the program will believe it is multiple files.")
        sys.exit(0)


    input_file = args.filename
    output_file = 'listed_ips.txt'
    print('Listing...')
    main(input_file, output_file)
    print('Done. Have a good day!')
