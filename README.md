# AppleCIDR
Parses a scope file containing IP ranges, CIDR notations, and domains and will output them as a list of individual IP addresses and domains. This helps with compatibility for tools that require IPs in a straightforward format for ingestion rather than ranges. If you have exclusions you need taken out, you can add that file in the input to remove them from the listed scope file. Reference the usages listed below. 

## Usage
```
python3 AppleCIDR.py <scope_file>
```
If you have exclusions
```
python3 AppleCIDR.py <scope_file> <exclusion_file>
```
<img src="https://github.com/Ghost7926/AppleCIDR/assets/93566632/d0717433-867c-4c94-8fbe-5e3f30e7f7c7" alt="pngtree-hot-apple-cider-vector-png-image_6905291" width="200" align="left">
