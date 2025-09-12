---
authors: ['björn']
date: '2025-09-12T10:06:50+02:00'
lastmod: '2025-09-12T10:06:50+02:00'
location: Sweden
draft: true
title: '2025 09 12 Unique Ids When Testing'
subtitle: ''
tags: []
daily: ['2025-09-12']
series: []
---

for doing random for tests I like setting it up like:

* Create a start timestamp that is "your epoch", usually the time you write the unique ID library and save it as a constant (i.e. `myEpoch := time.Date(2025, 9, 12, 9, 31, 0, 0, time.UTC)`
* When creating a new id then do: `id := time.Now().Since(myEpoch).Nanoseconds()`
* If you want to shorten the ID then convert it to base36: `strconv.FormatInt(id, 36)`

By creating our own epoch we create a shorter id since we're not taking nanoseconds since the 70s, and then if we use letters as well as numbers in the id we can further shorten it since base36 is the whole english alphabet+numbers so the length gets severely cut :smile:

And by using nanosecond precision you shouldn't have a problem of collisions :slightly_smiling_face:

For those cases where you can only use numbers, hope it's int64 then and then just rely on custom epoch + nanoseconds :slightly_smiling_face:

Very much inspired to use base36 from https://www.youtube.com/watch?v=gocwRvLhDf8 :smile:

Aand why base36 instead of base64 if that's what YouTube uses? Because [Go's FormatInt](https://pkg.go.dev/strconv@go1.25.0#FormatInt) only supports 36 out of the box :slightly_smiling_face: