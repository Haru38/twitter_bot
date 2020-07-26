# -*- coding: utf-8 -*-
import tweepy
import json
import os
import time
import threading

import requests


class Bot():
    def __init__(self,api,Twitter_ID,SCREEN_NAME,lock):
        self.api = api
        self.Twitter_ID = Twitter_ID
        self.SCREEN_NAME = SCREEN_NAME
        self.lock = lock
        self.last_rep = ''

    def auto_tweet(self):
        print("start auto tweet")
        self.lock.acquire()

        text = "ツイートする内容"

        print("get image files")
        #画像ファイルの取得
        auto_path = '画像ファイルのパス'
        auto_file_names = os.listdir(auto_path)
        auto_media_ids = []

        for auto_filename in sorted(auto_file_names)[:len(rlist)]:
            auto_res = self.api.media_upload(auto_path + auto_filename)
            auto_media_ids.append(auto_res.media_id)


        self.api.update_status(status=text, media_ids=auto_media_ids)
        self.lock.release()
        print("end auto tweet")

    def reply(self):

        if self.last_rep == '':
            timeline = self.api.mentions_timeline(count=1)
        else:
            timeline = self.api.mentions_timeline(count=200, since_id=self.last_rep)
        #その時のタイクラインの状況を取ってくる
        if len(timeline) == 0:#一つもなかった場合
            print("reply tweets doesn't exist.")
            return

        self.last_rep = timeline[0].id
        for status in timeline:
            screen_name = status.author.screen_name
            #inpが相手の返信内容
            keywords = status.text.lstrip("@"+self.Twitter_ID).replace('\n','')#本文の余計な部分を削除

            text = "返信内容"

            self.lock.acquire()#api変数

            #画像ファイルの取得
            path = '画像ファイルのパス' #ファイルディレクトリ
            file_names = os.listdir(path)#ファイルをリストで取得
            media_ids = []
            for filename in sorted(file_names)[:len(ret_list)]:
                res = self.api.media_upload(path + filename)
                media_ids.append(res.media_id) #idリストへ追加

            #ツイート
            self.api.update_status(media_ids=media_ids, status=text, in_reply_to_status_id=status.id)
            self.lock.release()
