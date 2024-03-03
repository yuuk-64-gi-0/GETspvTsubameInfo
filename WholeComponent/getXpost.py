import os
import sys
import json
import tweepy
import time
os.chdir(os.path.dirname(__file__))

RootSettingFile = "RootSettings.json"
RootSettings : dict[str,str] = {}

def get1LineTextFile(filepath : os.PathLike) -> str:
    with open(filepath,"r",encoding='utf-8') as fr:
        keyval = fr.read()
    return keyval

def getJsonFile(filepath : os.PathLike):
    return json.loads(get1LineTextFile(filepath))

def getRootSettings():
    global RootSettings
    RootSettings = getJsonFile(RootSettingFile)

def genXclient(Settings : dict[str,str]):
    XBearerToken = get1LineTextFile(Settings["XBearerTokenFile"])
    XApiKey = get1LineTextFile(Settings["XApiKeyFile"])
    XApiSecretKey = get1LineTextFile(Settings["XApiSecretKeyFile"])
    XAccessToken = get1LineTextFile(Settings["XAccessTokenFile"])
    XAccessTokenSecret = get1LineTextFile(Settings["XApiSecretKeyFile"])
    X_client = tweepy.Client(
        bearer_token=XBearerToken,
        consumer_key=XApiKey,
        consumer_secret=XApiSecretKey,
        access_token=XAccessToken,
        access_token_secret=XAccessTokenSecret,
        wait_on_rate_limit=True)
    return X_client

def getXaccountID(username : str):
    global RootSettings
    IDcachefile = RootSettings["XIdCacheFile"]
    if not(os.path.isfile(IDcachefile)):
        with open(IDcachefile,"w") as ifw:
            ifw.write("username:ID")
    while not(os.access(IDcachefile,os.R_OK)):
        time.sleep(1)
    with open(IDcachefile,"r",encoding='utf-8') as fr:
        IDdict = {line.split(":")[0]:line.split(":")[1] for line in fr.read().splitlines()}
    if username in IDdict.keys():
        return IDdict[username]
    else:
        X_client = genXclient(RootSettings)
        resid = dict(X_client.get_user(username=username)[0])["id"]
        IDdict[username] = resid
        while not(os.access(IDcachefile,os.W_OK)):
            time.sleep(1)
        with open(IDcachefile,"a",encoding='utf-8') as fa:
            fa.write("\n%s:%s" % (username,resid))
        return resid

def getTargetPost(username : str):
    global RootSettings
    user_id = getXaccountID(username)
    X_client = genXclient(RootSettings)
    responses = X_client.get_users_tweets(id=user_id, max_results=100)
    outdata = {}
    for response in responses:
        tweet_dict = dict(response)
        outdata[tweet_dict["id"]] = tweet_dict
    return outdata


if __name__ == "__main__":
    getRootSettings()
    username = RootSettings["XUserId"]
    res = getTargetPost(username)
    with open("testout.json","w",encoding='utf-8') as fw:
        json.dump(res,fw,ensure_ascii=False,indent=4)
