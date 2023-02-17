import requests, json, os, urllib.request, shutil
from jinja2 import Environment, FileSystemLoader

k = ''
with open('/home/agray/apod-k', 'r') as file_to_read:       #API KEY in link with "count=3" to print 3 random APODs in json file
    json_data = json.load(file_to_read)
    k = json_data["API_KEY"]

# get data of the 3 APODs
r = requests.get(k)                         #  "https://api.nasa.gov/planetary/apod?api_key=XXXXXXXXX&count=3",
data = json.loads(r.text)
#hehehe
# Print APOD data into json list
with open('/home/agray/comp_421_22s_agray/PROJ02/builds/apods.json', 'w') as f:
    # Display the values of "img"
    print('[\n\t', end="", file=f)
    for img in data:
        for title in img:                                 # get title  
            print('{\n\t\t"title": "', end="", file=f)      #print json data to file
            print(img['title'], '",', file=f)
            break                                           #end to print once
        for date in img:                               
            print('\t\t"date": "', end="", file=f)                 
            print(img['date'],'",', file=f)                    
            break                                           
        for explanation in img:                                 
            print('\t\t"explanation": "', end="", file=f)
            print(img['explanation'],'",', file=f)
            break
        for hdurl in img:                                # get image name of APOD file from website link
            print('\t\t"name": "', end="", file=f)
            print(img["date"]+"_"+img["title"].replace(" ","_").replace(":","_")+".jpg",'"\n\t},\n\t', end="", file=f)
            break
        
        title = img["date"]+"_"+img["title"].replace(" ","_").replace(":","_")+".jpg"   # Title of new image directory     
        image_dir = "/home/agray/comp_421_22s_agray/PROJ02/builds/img"                   # Path of the image directory
        urllib.request.urlretrieve(img['hdurl'], os.path.join(image_dir,title))         # Downloading and renaming the image file
      
    # Necessary to print json file without extra comma after last 'image name' 
    print('{\n\t\t "date": "<div style=', end="", file=f)
    print("'display:inline-block; border: 1px solid #CCC; border-radius: 6px; -webkit-border-radius: 6px; -o-border-radius: 6px; position: relative; overflow: hidden; width: 310px; height: 450px;'><iframe src='https://spotthestation.nasa.gov/widget/widget.cfm?country=United_States&region=California&city=Camarillo' width='310' height='450' frameborder='0' ></iframe></div>", end="", file=f)
    print('"}\n]', end="", file=f)

with open("/home/agray/comp_421_22s_agray/PROJ02/builds/apods.json", "r") as d:
    apods = json.load(d)
    
print(apods)

fileLoader = FileSystemLoader("/home/agray/comp_421_22s_agray/PROJ02/templates")
env = Environment(loader=fileLoader)

rendered = env.get_template("newsletter.html.j2").render(apods=apods, title="Random APOD Gallery", src="../img/")

fileName="newsletter.html"

with open(f"/home/agray/comp_421_22s_agray/PROJ02/builds/{fileName}", "w") as f:
    f.write(rendered)