import requests
import time
import sys
from metros import metro
import dateToId
import os
def pull_json(end_cursor):
    try:
        URL='https://www.instagram.com/explore/locations/204517928/chicago-illinois/?__a=1&max_id='+end_cursor
        r = requests.get(url = URL) 
        data = r.json() 
        data=data['graphql']['location']['edge_location_to_media']
        return data
    except:
        return None

    
def main(argv):
    n=len(argv)
    if(n<3):
        print('pass 2 dates as input ..... and one location')
        return
    date1=argv[0]
    date2=argv[1]
    location=argv[2]
        
    try:
        maxid1=dateToId.run(date1)
        maxid2=dateToId.run(date2)
    except:
        print("error in date format, make sure no following zeroes example: 2020/7/15")
        return
    if(location not in metro):
        print('Location not available in metros file')
        return 
    
    
    posts=[]
    end_cursor=maxid1
    if(n==4):
        end_cursor=argv[3]
    wrong=0
    ctr=0
    while(end_cursor and wrong<20 and end_cursor>maxid2):
        try:
            data=pull_json(end_cursor)
            wrong=0
        except:
            print('waiting........')
            wrong+=1
            time.sleep(5)
            continue
        try:
            posts.extend(data['edges'])
            wrong=0
        except:
            print('waiting........ couldnt find edges in data make sure end_cursor is correct if passed')
            wrong+=1
            time.sleep(5)
            continue

        end_cursor=data['page_info']['end_cursor']
        with open('cursor.txt', "w") as output:
                    output.write(str(end_cursor))
    #     break
        if(len(posts)>=ctr):
            ctr+=500
            if(ctr>500):
                os.remove(last)
            with open(location+'_'+date1.replace('/','-')+'_'+date2.replace('/','-')+'_'+end_cursor+'.txt', "w") as output:
                    output.write("posts="+str(posts))
            last=location+'_'+date1.replace('/','-')+'_'+date2.replace('/','-')+'_'+end_cursor+'.txt'
            
        print(len(posts),end_cursor)
    
    if(wrong>=30):
        print("Not Exited Succesfully.. couldnt scrape more, scraped"+str(len(posts))+" posts ")
        return
    
    with open(location+'_'+date1.replace('/','-')+'_'+date2.replace('/','-')+'_'+end_cursor+'.txt', "w") as output:
                    output.write("posts="+str(posts))
    
    print("Done.... scraped "+str(len(posts))+" posts ")
    

if __name__=="__main__":
    main(sys.argv[1:])