---
authors: ['björn']
date: '{{ .Date }}'
lastmod: '{{ .Date }}'
location: {{ .Site.Params.defaultLocation }}
draft: true
full: false  # set to true if the full thing should be shown in listings
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
tags: []
daily: ['{{ (time .Date).Format "2006-01-02" }}']
series: []
---

<!--more-->
