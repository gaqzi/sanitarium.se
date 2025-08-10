---
authors: ['björn']
date: '{{ .Date }}'
lastmod: '{{ .Date }}'
draft: true
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
subtitle: ''
tags: []
daily: ['{{ .Date.Format "2006-01-02" }}']
---
