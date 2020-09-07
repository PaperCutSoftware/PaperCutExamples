# Install a New Web Auth Token

When using the web services API all calls need to provide a security token.

This token needs to be configured in PaperCut via the advanced config key

```
auth.webservices.auth-token
```

The key can be configured using the `server-command` utility.

This Go program is designed to be compiled and shipped with a third party
integration so that a new security token can be installed ay config
time.

NOTE: This program must be run on the PaperCut MF/NG server under the PaperCut or admin/root account

It should work on Windows, MacOS and Linux. But you should test thoroughly
