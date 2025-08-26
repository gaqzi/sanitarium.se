---
authors: ['björn']
date: '{{ .Date }}'
lastmod: '{{ .Date }}'
draft: true
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
tags: []
daily: ['{{ (time .Date).Format "2006-01-02" }}']
---
