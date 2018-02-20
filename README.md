# scrapeMeAReddit v.1.0
*A simple command line Reddit scraping tool.*
### JT Wolohan
*Center for Computer Mediated Communication*

*Dept. Information and Library Science*

*Indiana University*

*jwolohan@indiana.edu*

### Introduction
scrapeMeAReddit is a simple command line tool for fetching Reddit posts. The tool offers users the ability to quickly download posts from specified subreddits or users. The software is written in Python3 and requires Python3 to run. Please take care to abide by Reddit's API access rules while using this software: https://github.com/reddit-archive/reddit/wiki/API 

To get set up with Reddit-approved application credentials (required to use this tool), visit this page and follow the instructions: https://github.com/reddit-archive/reddit/wiki/OAuth2

### Using the tool
The software is run on the command line. To use the tool, first update the demo\_credentials.json file with your application credentials and an appropriate user agent. You can then run the software in one of two modes: (1) subreddit mode and (2) user mode.
**Subreddit mode**
Subreddit downloads all posts from between to points in time from subreddits specified in an input file. The posts are saved as JSON files.

`python3 scrapeMeAReddit.py -c your_credentials.json --subs your_subreddits.txt`

Be default, the tool will scrape data from the past 7 days, but this can be changed by using `--start` or `-s` and `--end` or `-e`, e.g., we could scrape all the posts from the year 2015 with:

`python3 scrapeMeAReddit.py -c your_credentials.json --subs your_subreddits.txt -s 01/01/2015 -e 12/31/2015`

Note that the dates must be in MM/DD/YYYY format.

Your file containing subreddits should be a plaintext file with one subreddit per line without r/ or /r/ prepended, e.g., AskReddit

**User mode**
User mode, similar to subreddit mdoe, is invoked as follows:

`python3 scrapeMeAReddit.py -c your_credentials.json --users your_users.txt`

Again, your file containing the users whose posts you would like to download should contain one user per file, without u/ or /u/ prepended, e.g., Throwaway27

User mode fetches a users 1000 most-recent posts.

*(c) 2018 - GNU LGPL3.0*

