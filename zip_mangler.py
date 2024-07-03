import re 
from os.path import abspath, exists
import argparse

def break_zip_signature(file_path: str, replacement_pattern: str):
	file_path = abspath(file_path)
	pattern_to_match_bytes = b'PK\x03\x04'
	replacement_pattern_bytes = replacement_pattern.encode('utf-8')

	with open(file_path, 'rb') as r:
		new_string, number_of_subs_made = re.subn(pattern=pattern_to_match_bytes, repl=replacement_pattern_bytes, string=r.read(), count=0)
	

	if number_of_subs_made < 1:
		raise Exception("Couldn't find anything to replace")
	
	return new_string

def repair_zip(file_path: str, replacement_pattern: str):
	file_path = abspath(file_path)
	pattern_to_match_bytes = replacement_pattern.encode('utf-8')
	replacement_pattern_bytes = b'PK\x03\x04'

	with open(file_path, 'rb') as r:
		new_string, number_of_subs_made = re.subn(pattern_to_match_bytes, repl=replacement_pattern_bytes, string=r.read(), count=0)
	
	if number_of_subs_made < 1:
		raise Exception("Couldn't find anything to replace")
	return new_string

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s','--source', type=str)
	parser.add_argument('-d','--destination', type=str)
	parser.add_argument('-r','--replacement', type=str)
	parser.add_argument('-m','--mode', type=str)

	args = parser.parse_args()

	if not exists(args.source):
		raise Exception("source file doesn't exist")
	if args.mode == "repair":
		repaired = repair_zip(args.source, args.replacement)
		destination = abspath(args.destination)
		with open(destination, 'wb') as w:
			w.write(repaired)
	elif args.mode == "corrupt":
		corrupted = break_zip_signature(args.source, args.replacement)
		destination = abspath(args.destination)
		with open(destination, 'wb') as w:
			w.write(corrupted)

if __name__ == "__main__":
	main()
"""
corrupt

python ./zip_mangler.py -s ./doc.zip -d ./doc.corrupted.zip -r '\0x35\0x4b\0x03\0x05' -m corrupt

repair

python ./zip_mangler.py -s doc.corrupted.zip -d doc.repaired.zip -r '\0x35\0x4b\0x03\0x05' -m repair
"""
