---
authors: ['björn']
date: '2025-10-01T12:44:45+02:00'
lastmod: '2025-10-01T12:44:45+02:00'
location: Sweden
title: 'Use --resolve with curl when testing Caddy on localhost'
tags:
  - how-to
  - linux
daily: ['2025-10-01']
series: []
---
Use `curl -k --resolve bjorn.now:443:127.0.0.1 https://bjorn.now` when testing an HTTPS site locally using [Caddy](https://caddyserver.com/), instead of `curl -k -H "Host: bjorn.now" https://localhost`, because Caddy relies on [SNI](https://en.wikipedia.org/wiki/Server_Name_Indication) and refuses the connection if it doesn't know which host you're trying to connect to.

<!--more-->

This seems to be a security decision to avoid leaking which certificates (and therefore sites) it hosts by not providing a default (can't find a source and it's what the search previews give me). Which my old nginx setup did.

The cryptic error message from cURL, which I didn't find anything obvious online about:
```text {class="no-copy-button"}
curl: (35) OpenSSL/3.0.13: error:0A000438:SSL routines::tlsv1 alert internal error
```

And I debugged this together with Claude by enabling debug logging in Caddy (`{ debug }` at the top level in the `Caddyfile`) which gave me this output when I called it using cURL:

```text {class="no-copy-button"}
2025/10/01 10:04:56.330 DEBUG   events  event   {"name": "tls_get_certificate", "id": "7353980b-a85e-4f10-9704-89da7358ef89", "origin": "tls", "data": {"client_hello":{"CipherSuites":[4866,4867,4865,49196,49200,159,52393,52392,52394,49195,49199,158,49188,49192,107,49187,49191,103,49162,49172,57,49161,49171,51,157,156,61,60,53,47,255],"ServerName":"","SupportedCurves":[29,23,30,25,24,256,257,258,259,260],"SupportedPoints":"AAEC","SignatureSchemes":[1027,1283,1539,2055,2056,2057,2058,2059,2052,2053,2054,1025,1281,1537,771,769,770,1026,1282,1538],"SupportedProtos":null,"SupportedVersions":[772,771],"Conn":{}}}}
2025/10/01 10:04:56.330 DEBUG   tls.handshake   no matching certificates and no custom selection logic  {"identifier": "127.0.0.1"}
2025/10/01 10:04:56.331 DEBUG   tls.handshake   all external certificate managers yielded no certificates and no errors {"remote_ip": "127.0.0.1", "remote_port": "42516", "sni": ""}
2025/10/01 10:04:56.331 DEBUG   tls.handshake   no certificate matching TLS ClientHello {"remote_ip": "127.0.0.1", "remote_port": "42516", "server_name": "", "remote": "127.0.0.1:42516", "identifier": "127.0.0.1", "cipher_suites": [4866, 4867, 4865, 49196, 49200, 159, 52393, 52392, 52394, 49195, 49199, 158, 49188, 49192, 107, 49187, 49191, 103, 49162, 49172, 57, 49161, 49171, 51, 157, 156, 61, 60, 53, 47, 255], "cert_cache_fill": 0.0002, "load_if_necessary": true, "obtain_if_necessary": true, "on_demand": false}
2025/10/01 10:04:56.332 DEBUG   http.stdlib     http: TLS handshake error from 127.0.0.1:42516: no certificate available for '127.0.0.1'
```

The culprit was the `"ServerName":""`, and I'm guessing also `"sni": ""`, so if you need to validate and see that as well then that's likely the problem. 🙂

---

This jogs my memory, back in the olden times, we would need a unique IP address for each HTTPS site because we couldn't multi-host, and SNI solved that problem. 

Importantly, SNI _doesn't_ encrypt the host name and it's still sent in plaintext to the server.
