## # LIBRARIES # ##
import re
import json
import requests

version = 0.2

## FUNCTIONS ##

def parse_args(): # для командной строки (парсер командной строки)
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--domain', type=str, required=True, help="Target domain.")
	parser.add_argument('-o', '--output', type=str, help="Output file.")
	return parser.parse_args()

def banner(): # для передачи параметра из формы в переменную нужно сделать : target = forms.cleaned_data['target'] ? 
	global version
	b = '''
          ____ _____ _____ ____  
         / ___|_   _|  ___|  _ \ 
        | |     | | | |_  | |_) |
        | |___  | | |  _| |  _ < 
         \____| |_| |_|   |_| \_\\
	
     Version {v} - Hey don't miss AXFR!
    Made by Sheila A. Berta (UnaPibaGeek)
	'''.format(v=version)
	print(b)
	
def clear_url(target):
	return re.sub('.*www\.','',target,1).split('/')[0].strip() # target передает домен 

def save_subdomains(subdomain,output_file):
	with open(output_file,"a") as f:
		f.write(subdomain + '\n')
		f.close()

def main():
	work_done = 
	#banner()
	args = parse_args()

	subdomains = []
	target = clear_url(args.domain)
	output = args.output

	req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

	if req.status_code != 200:
		print("[X] Information not available!") 
		exit(1)

	json_data = json.loads('[{}]'.format(req.text.replace('}{', '},{')))

	for (key,value) in enumerate(json_data):
		subdomains.append(value['name_value'])

	
	print("\n[!] ---- TARGET: {d} ---- [!] \n".format(d=target))

	subdomains = sorted(set(subdomains))

	for subdomain in subdomains:
		print("[-]  {s}".format(s=subdomain))
		if output is not None:
			save_subdomains(subdomain,output)

	print("\n\n[!]  Done. Have a nice day! ;).")


main()
