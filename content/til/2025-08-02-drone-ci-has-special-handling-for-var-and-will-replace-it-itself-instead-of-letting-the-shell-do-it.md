---
authors: ['björn']
date: 2025-08-02T09:37:29.210041+08:00
daily: ['2025-08-02']
lastmod: 2025-08-02T09:37:29.210041+08:00
title: Drone CI handling of ${VAR} vs. $VAR
tags:
  - drone-ci
---
Drone CI has special handling for `${VAR}` and will replace it **itself** instead of letting the shell do it. So if you have `export PATH=${GOPATH}/bin:$PATH` and have `$GOPATH` defined in your global environment key, then it'll become a blank value. But if you do `export PATH=$GOPATH/bin:$PATH` it'll work.
  
This is different from normal shell where `${VAR}` is the same as `$VAR` and it exists to make sure you can concatenate strings without issues, i.e.
  
```shell
VAR=m000
echo "'${VAR}est'"  # => 'm000est'
echo "'$VARest'"    # => ''
```
