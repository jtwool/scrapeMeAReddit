# scrapeMeAReddit v1.0
# JT Wolohan
# jwolohan@indiana.edu
# Dept. Information and Library Science, Indiana University
# Center for Computer Mediated Communication
# (c) 2018 - GNU LESSER GENERAL PUBLIC LICENSE
import requests, requests.auth
from requests import get
import json, re, functools, os
from datetime import datetime,timezone,timedelta
from time import sleep

def getReddit(url,params=None,**kwargs):
  sleep(1.05)
  return get(url,params=None,**kwargs)

def time2POSIX(timestr):
  mytime = datetime.strptime(timestr,"%m/%d/%Y").replace(tzinfo=timezone.utc)
  posix = (mytime - datetime(1970, 1, 1, tzinfo=timezone.utc))
  return posix.total_seconds()

def authenticate_crawler(creds):
  client_auth = requests.auth.HTTPBasicAuth(creds['client-id'],
                                            creds['client-secret'])
  post_data = {"grant_type": "password",
               "username": creds['username'],
               "password": creds['password']}
  headers = {"User-Agent": creds['user-agent']}
  response = requests.post("https://www.reddit.com/api/v1/access_token",
                           auth=client_auth,
                           data=post_data,
                           headers=headers)
  tkn = response.json()['access_token']
  headers['Authorization'] = "bearer "+tkn
  return headers

def genUserPath(u,after=None,info=False):
  p1 = "http://oauth.reddit.com/user/"
  p2 = ".json?limit=100"
  if after not in ['',None]:
    p2+="&after={}".format(after)
  elif info:
    p2 = "/about.json"
  return(p1+u+p2)

def check_ratelimit(x):
  remain = int(float(x.headers.get('x-ratelimit-remaining',0)))
  reset = int(float(x.headers.get('x-ratelimit-reset',300)))
  if remain <= 10:
    sleep(301)
    return 1
  else:
    return 0

def _safeJSONloads(s:str):
  try:
    return json.loads(s)
  except:
    return {}

def writeUser(fn,u,ps):
  with open(f"./{fn}/{u}.json","w") as f:
    f.write(json.dumps(ps))
  return None

def get_user_text(headers,user):
  rs = 0
  try:
    #Get account created date and karma
    abturl = genUserPath(user,info=True)
    x = getReddit(abturl,headers=headers)
    check_ratelimit(x)
    j = _safeJSONloads(x.text)
    r = []
    url = genUserPath(user)
    x = getReddit(url,headers=headers)
    if check_ratelimit(x): 
      headers = myAuthenticate()
    j = _safeJSONloads(x.text)
    rs += 1
    AFTER = j.get('data',{}).get('after','')
    children = j.get('data',{}).get('children',[])
    r = r + [child for child in children]
    while AFTER not in [None,'']:
      url = genUserPath(user,after=AFTER)
      x = getReddit(url,headers=headers)
      rs += 1
      if check_ratelimit(x): 
        headers = myAuthenticate()
      j = _safeJSONloads(x.text)
      AFTER = j.get('data',{}).get('after','')
      children = j.get('data',{}).get('children',[])
      r = r + [child for child in children]
    return r
  except: return []

def getUsers(creds,user_file):
  # Make directory to store user files  
  uf = re.sub("\.[a-z]{3}","",user_file.split("/")[-1])
  filename = str(f"RedditUsers{uf}")
  try:
    os.mkdir(f"./{filename}")
  except FileExistsError: pass
  # Create authentication function
  myAuthenticate = functools.partial(authenticate_crawler,creds=creds)
  HEAD = myAuthenticate()
  with open(user_file,'r') as f:
    for i,u in enumerate(f):
      if i%25 == 0:
        HEAD = myAuthenticate()
      u = u.strip()
      posts = get_user_text(HEAD,u)
      writeUser(filename,u,posts)

def genSubPath(sub,start,stop):
  a = str(f"http://oauth.reddit.com/r/{sub}/search?sort=new&q=timestamp%3A{stop}")
  z= str(f"{start}&restrict_sr=on&syntax=cloudsearch&limit=100")
  return str(f"{a}..{z}")

def requestComments(permalink,headers):
  url = "http://oauth.reddit.com/"+permalink
  x = getReddit(url,headers=headers)
  return json.loads(x.text)

def getPosts(headers,subreddit,start,end,wp,creds):
  myAuthenticate = functools.partial(authenticate_crawler,creds)
  start_time = int(start)
  end_time = int(end)
  while end_time > end-1:
    afters = []
    after = None
    end_time = start_time-(20000)
    more_posts = True
    while more_posts:
      url = genSubPath(subreddit,start_time,end_time)
      if after: url = url+"&after="+after
      x = getReddit(url,headers=headers)
      if check_ratelimit(x):
        headers = myAuthenticate()
      j = json.loads(x.text)
      after = j['data']['after']
      if after in afters: break
      else: afters.append(after)
      if len(j['data']['children']) == 0: 
        more_posts = False
      else:
        for post in j['data']['children']:
          if check_ratelimit(x):
            headers = myAuthenticate()
          permalink = post['data']['permalink']
          with open(f"{wp}/{post['data']['name']}.json",'w') as f:
            f.write(json.dumps(requestComments(permalink,headers)))
    start_time = end_time

def getSubreddits(creds,subs_file,start,end):
  # Make directory to store user files  
  sf = re.sub("\.[a-z]{3}","",subs_file.split("/")[-1])
  filename = str(f"Subreddits-{sf}")
  try:
    os.mkdir(f"./{filename}")
  except FileExistsError: pass
  # Create authentication function
  myAuthenticate = functools.partial(authenticate_crawler,creds=creds)
  HEAD = myAuthenticate()
  with open(subs_file,'r') as f:
    for subreddit in f:
      subreddit = subreddit.strip()
      wp = str(f"./{filename}/{subreddit}")
      try:
        os.mkdir(wp)
      except FileExistsError: pass
      getPosts(HEAD,subreddit,time2POSIX(start),time2POSIX(end),wp,creds)
      
if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("-c","--credentials",type=str,help="path to account credentials")
  parser.add_argument("-s","--start",type=str,help="start date MM/DD/YYYY format")
  parser.add_argument("-e","--end",type=str,help="end date in MM/DD/YYYY format")
  parser.add_argument("--subs",type=str,help="path to file cointaining list of subreddits")
  parser.add_argument("--users",type=str,help="path to file cointaining list of subreddits")

  args = parser.parse_args()

  with open(args.credentials) as f:
    creds = json.load(f)
  if not args.start: args.start = datetime.now().strftime("%m/%d/%Y")
  if not args.end:
    rn = datetime.now()
    args.end = (rn-timedelta(days=7)).strftime("%m/%d/%Y")
  if args.subs:
    print(f"Fetching links and comments from subs in {args.subs} between {args.start} to {args.end}")
    getSubreddits(creds,subs_file=args.subs,start=args.start,end=args.end)
  elif args.users:
    print(f"Fetching links and comments by users from {args.users}")
    getUsers(creds,user_file=args.users)
