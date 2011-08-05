#!/bin/bash
homelocation=""
gitlocation=$homelocation""        #版本管理所在的目录
loglocation=$homelocation""       #输出日志的目录
untrack=$loglocation"/add.log"                 
modified=$loglocation"/mod.log"
deleted=$loglocation"/del.log"
ignoreType=".php"
cd  $gitlocation
git ls-files  -m|grep $ignoreType > $modified
git ls-files  -d|grep $ignoreType > $deleted
git ls-files --exclude-standard --others |grep $ignoreType > $untrack
cd $loglocation
python pycheck.py
