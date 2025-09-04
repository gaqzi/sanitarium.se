---
authors: ['björn']
date: 2025-08-02T09:37:29.210041+08:00
lastmod: 2025-08-15T15:24:00.000000+08:00
location: Singapore
daily: ['2025-08-02']
title: Drone CI handling of ${VAR} vs. $VAR
tags:
  - drone-ci
---
Drone CI has special handling for `${VAR}` and will replace it **itself** instead of letting the shell do it. So if you have `export PATH=${GOPATH}/bin:$PATH` and have `$GOPATH` defined in your global environment key, then it'll become a blank value. But if you do `export PATH=$GOPATH/bin:$PATH` it'll work. You [can escape by adding an extra dollar sign](https://laszlo.cloud/drone-environment-variables-three-tips#when-variables-resolve-to-empty-string), i.e. `$${VAR}` will be evaluated by the shell.

This is different from normal shell where `${VAR}` is the same as `$VAR` and it exists to make sure you can concatenate strings without issues, i.e.

```shell
VAR=m000
echo "'${VAR}est'"  # => 'm000est'
echo "'$VARest'"    # => ''
```
