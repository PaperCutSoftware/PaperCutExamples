# Using the PaperCut MF/NG public web services API to provide a manual top up payment gateway

The XML-RPC public web services API has a method call `api.adjustUserAccountBalance()` which does what is says on the tin. See the [documentation](http://www.papercut.com/products/ng/manual/apdx-tools-web-services.html) for details.


1. Develop a web page integration with a payment service
2. Add a custom URL to the PaperCut user web page, which is used by end users when they want to top up their PaperCut account.
3. When the user clicks on the URL link in the PaperCut user web page to the payment service, the user identification details is passed as part of the URL. This is explained at:

      http://www.papercut.com/products/ng/manual/ch-customization-user-web-pages.html#Additional-Links-in-the-Navigation-Menu

4. The user is re-directed to the custom payment service page via the configured URL. This solution would manage the payment process and, once approved, the solution has the responsibility of calling the local PaperCut XML-RPC service with the user name and credit adjustment `api.adjustUserAccountBalance()`


Note: If the XML-RPC call is coming to PaperCut from across the network it is necessary to whitelist the remote address in
the PaperCut admin interface.
