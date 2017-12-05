#!/usr/bin/env php
<?php

/* An example PHP script to show how to manage paramters and responses on
 * a modern version of PHP. Tested on PHP 7
 */

$auth = "token";

$user = "alec";

function do_call($request) {
  
  $url = "http://localhost:9191/rpc/api/xmlrpc";
  $header[] = "Content-type: text/xml";
  $header[] = "Content-length: ".strlen($request);
  
  $ch = curl_init();   
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($ch, CURLOPT_TIMEOUT, 1);
  curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
  curl_setopt($ch, CURLOPT_POSTFIELDS, $request);
  
  $data = curl_exec($ch);       
  if (curl_errno($ch)) {
    print curl_error($ch);
  } else {
    curl_close($ch);
    return $data;
  }
}

$request = xmlrpc_encode_request("api.setUserProperties",
                  array($auth,
                        $user,
                        array(
                          array( "primary-card-number", "8888"),
                          array("secondary-card-number", "9999"))));

$r = do_call($request);

$response = xmlrpc_decode($r);

if ($response && is_array($response) && xmlrpc_is_fault($response)) {
    trigger_error("xmlrpc: $response[faultString] ($response[faultCode])");
} else {
  print_r($response);
}

?>

