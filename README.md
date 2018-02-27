# scrapeMeAReddit v.1.0
*A simple command line Reddit scraping tool.*
### JT Wolohan
**Dept. Information and Library Science, Indiana University**

**jwolohan@indiana.edu**

### Introduction
scrapeMeAReddit is a simple command line tool for fetching Reddit posts. The tool offers users the ability to quickly download posts from specified subreddits or users. The software is written in Python3 and requires Python3 to run. Please take care to abide by Reddit's API access rules while using this software: https://github.com/reddit-archive/reddit/wiki/API

To get set up with Reddit-approved application credentials (required to use this tool), visit this page and follow the instructions: https://github.com/reddit-archive/reddit/wiki/OAuth2

### Installation
1. Clone this repository
  > `git clone https://github.com/jtwool/scrapeMeAReddit`
2. Create your credentials file (e.g., my_creds.json)
3. Create your target file (e.g., my_subs.txt)
4. Run the script with Python3
  > `python3 scrapeMeAReddit -c my_creds.json --subs my_subs.txt`
5. $$$

### Using the tool
The software is run on the command line. To use the tool, first update the demo\_credentials.json file with your application credentials and an appropriate user agent. You can then run the software in one of two modes: (1) subreddit mode and (2) user mode.

**Subreddit mode**

Subreddit downloads all posts from between to points in time from subreddits specified in an input file. The posts are saved as JSON files.

    python3 scrapeMeAReddit.py -c your_credentials.json --subs your_subreddits.txt

Be default, the tool will scrape data from the past 7 days, but this can be changed by using `--start` or `-s` and `--end` or `-e`, e.g., we could scrape all the posts from the year 2015 with:

    python3 scrapeMeAReddit.py -c your_credentials.json --subs your_subreddits.txt -s 12/31/2015 -e 01/01/2015

Note that the dates must be in MM/DD/YYYY format and the scrapeMeAReddit scrapes *backwards* in time. Your end date should be before your start date.

Your file containing subreddits should be a plaintext file with one subreddit per line without r/ or /r/ prepended, e.g.:

    -- file: your_subreddits.txt
    AskReddit
    IAmA
    funny
    gifs

**User mode**

User mode, similar to subreddit mdoe, is invoked as follows:

    python3 scrapeMeAReddit.py -c your_credentials.json --users your_users.txt

Again, your file containing the users whose posts you would like to download should contain one user per file, without u/ or /u/ prepended, e.g.:

    -- file: your_users.txt
    Spartacus
    TheRealSlimShady
    TheBatman
    Throwaway27

User mode fetches each users 1000 most-recent posts.

**Output**

Data retrieved will be saved to subdirectories created in the directory from which scrapeMeAReddit is run. Those subdirectories will be named after the file passed to the --users or your --subreddits option. For example, if your users file is called `funny_users.txt` the data will be saved at `./funny_users/`. Subreddit data will be saved in subdirectories of that directory. For example, a file named `your_subreddits.txt` containing the subreddits IAmA and funny would save data to `./your_subreddits/IAmA/` and `./your_subreddits/funny/`. The data retrieved will be .json objects and each file will either be named its reddit name (for post retrieved from subreddits) or the name of the user represented (for users).

*(c) JT Wolohan 2018 - GNU LGPL3.0*
