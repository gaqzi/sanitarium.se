---

authors: ['björn']
comments: false
date: 2024-02-01 17:00:00 +08:00
slug: how-to-make-docker-pull-resume-layer-downloads
title: "How to make Docker resume downloads" 
subtitle: "…download that final 100KB and not 200MB again"
categories:
- blog
tags:
- docker
- how-to

---


In the Docker Desktop app you can go into `Features in Development` and check
`Use containerd for pulling and storing images`.

Or you can do add the following to Docker's `daemon.json` file:

```javascript
{
  "features": {
    "containerd-snapshotter": true
  }
}
```

This comes from [a comment] in a ticket for [resuming downloads when they 
fail.][2]

[a comment]: https://github.com/docker/for-linux/issues/1187#issuecomment-1457279396
[2]: https://github.com/docker/for-linux/issues/1187
