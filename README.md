<h1>AppleCIDR <img src="https://github.com/Ghost7926/AppleCIDR/assets/93566632/d0717433-867c-4c94-8fbe-5e3f30e7f7c7" alt="" width="40"> </h1>

Parses a scope file containing IP ranges, CIDR notations, and domains and will output them as a list of individual IP addresses and domains, or collapse them into the minimal set of CIDR blocks. This helps with compatibility for tools that require IPs in a straightforward format for ingestion rather than ranges, or when given odd starting and ending IP addresses. If you have exclusions you need taken out, you can add that file as an additional argument to remove them from the scope.

## Modes

- **`list`** — Expands all ranges and CIDRs into individual IP addresses. Output: `listed_ips.txt`
- **`range`** — Collapses individual IPs and ranges into the smallest set of CIDR blocks. Output: `cidr_ranges.txt`

## Usage

```
python3 AppleCIDR.py [list|range] <scope_file>
```

With exclusions:

```
python3 AppleCIDR.py [list|range] <scope_file> <exclusion_file>
```

## Supported Input Formats

The scope and exclusion files can contain any mix of the following, one entry per line:

| Format | Example |
| --- | --- |
| Single IP | `10.10.10.5` |
| CIDR notation | `10.10.10.0/24` |
| Full range | `10.10.10.0-10.10.100.255` |
| Shorthand range | `10.10.10.1-50` (end uses start's first three octets) |
| Domain | `example.com` (passed through unchanged) |

Blank lines and lines starting with `#` are ignored.

## Examples

Expand a messy scope file into individual IPs, minus exclusions:

```
python3 AppleCIDR.py list scope.txt exclude.txt
```

Take a raw list of individual IPs and collapse it into CIDR blocks for tools like nmap or netexec:

```
python3 AppleCIDR.py range scope.txt
```
