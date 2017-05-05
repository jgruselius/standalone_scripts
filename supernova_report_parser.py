import sys
import re
import json
import csv
import fileinput
import argparse

def parse_and_print(files, print_csv=False):
	samples = {}
	p = re.compile(r"\[(P\d{3,}_\d{3,})\]")
	for line in fileinput.input(files=files):
		m = p.search(line)
		if m:
			s = m.group(1)
		else:
			l = line.split("=")
			if len(l) > 2:
				d = [x.strip(" -") for x in l]
				samples.setdefault(s, {})[d[1]] = d[0]
	if print_csv:
		# Convert to list:
		slist = []
		for k,v in samples.items():
			x = {"SAMPLE": k}
			x.update(v)
			slist.append(x)
		# Build header from all unique labels:
		header = set()
		for s in slist:
			header.update(s.keys())
		writer = csv.DictWriter(sys.stdout,fieldnames=list(header))
		writer.writeheader()
		for s in slist:
			writer.writerow(s)
	else:
		print(json.dumps(samples))

def main(args):
	parse_and_print(args.files, args.csv)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Parse Supernova reports and print numbers in JSON or CSV")
	parser.add_argument('--csv', action="store_true", default=False,
		help='Output in CSV format, default is JSON')
	parser.add_argument('files', metavar='FILE', nargs='*',
		help='Files to parse, if empty or "-" stdin is used')
	args = parser.parse_args()
	main(args)