#!/bin/bash
homelocation="/Users/timsims"
gitlocation=$homelocation"/Sites/shop"        #版本管理所在的目录
loglocation=$homelocation"/github/shop"       #输出日志的目录
untrack=$loglocation"/add.log"                 
modified=$loglocation"/mod.log"
deleted=$loglocation"/del.log"
cd  $gitlocation
git ls-files  -m|grep .php > $modified
git ls-files  -d|grep .php > $deleted
git ls-files --exclude-standard --others |grep .php  > $untrack
