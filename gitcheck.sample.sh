#!/bin/bash
homelocation=""
gitlocation=$homelocation""         #版本管理所在的目录
loglocation=$homelocation""         #输出日志的目录
untrack=$loglocation"/add.log"                 
modified=$loglocation"/mod.log"
deleted=$loglocation"/del.log"
fileType="."  						#要监控的文件类型
cd  $gitlocation
git ls-files  -m|grep $fileType > $modified
git ls-files  -d|grep $fileType > $deleted
git ls-files --exclude-standard --others |grep $fileType > $untrack
cd $loglocation
python pycheck.py
