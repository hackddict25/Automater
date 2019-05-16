import requests
import os
import time
import sys


#Agruement checker
if len(sys.argv)!=2:
    print('Enter a domain, Ex. python recon.py google.com')
    sys.exit(1)
domain=sys.argv[1]

#File checker
from pathlib import Path
my_file=Path('/root/Documents/recon/'+domain)
if my_file.is_dir():
    print('file exists')
    print('[!]quitting')
    sys.exit()

#aquatone subdomain finder

os.system('aquatone-discover --domain '+domain)
time.sleep(0.3)
os.system('aquatone-takeover --domain '+domain)
time.sleep(0.3)



#sublister subdomain finder
os.system('cd /root/Downloads/Sublist3r && mkdir /root/Documents/recon/'+domain+' && python /root/Downloads/Sublist3r/sublist3r.py -d '+domain+' -o /root/Documents/recon/'+domain+'/'+domain+'.txt')
time.sleep(0.3)


#domain='carta.com'
#subs formatting
f=open('/root/aquatone/'+domain+'/hosts.txt','r')
sep=','
new=''
s=open('/root/Documents/recon/'+domain+'/'+domain+'.txt','a')
f.seek(0)
for line in f:
   
   head=line[:line.find(',')] 
   print(head)
   s.write(head)
   s.write('\n')
   if(line==''):
       break
   

s.close()
f.close()


#sorting of duplicate domains
lines_seen = set()
outfile = open('/root/Documents/recon/'+domain+'/temp.txt','w')
for line in open('/root/Documents/recon/'+domain+'/'+domain+'.txt','r'):
    if line not in lines_seen: #not a duplicate
        outfile.write(line)
        lines_seen.add(line)

    
outfile.close()


# Screenshot 
print('[info] screenshot beginning')
time.sleep(0.2)
os.system('webscreenshot -i /root/Documents/recon/'+domain+'/temp.txt -o /root/Documents/recon/'+domain+'/screenshot')


#subdomain report generate


directory ='/root/Documents/recon/'+domain+'/screenshot'
filecopy="/root/Documents/recon/%s/report.html" %(domain)
 
for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           with open(filecopy,'a+') as c:
                c.write('<h2>'+f+'</h2>') 
                c.write('<img src="')
                c.write(os.path.abspath(os.path.join(dirpath, f)))
                c.write('\" ">')
                c.write("<br><br>")    
                c.write('\n')

	#Domains which dont have screenshot
temp = '/root/Documents/recon/'+domain+'/temp.txt'
with open(filecopy,'a+') as d:
	d.write('<br><br><br><center><h1>OTHER DOMAINS</h1></center>')




temp2 = '/root/Documents/recon/'+domain+'/temp2.txt'
for dirpath,_,filenames in os.walk(directory):
	for f in filenames:
		with open(temp2,'a+') as t:
			f = f.replace("http_","")
			f = f.replace("_80.png","")	
			t.write(f)
			t.write('\n')
	
with open('/root/Documents/recon/'+domain+'/temp.txt','r+') as source:
    lines_src = source.readlines()
with open(temp2,'r') as f:
    lines_f = f.readlines()
destination = open(filecopy,'a+')
for data in lines_src:
    if data not in lines_f:
        destination.write('<h2><a href="https://'+data+'">'+data+'</a></h2><br>')
destination.close()

		
