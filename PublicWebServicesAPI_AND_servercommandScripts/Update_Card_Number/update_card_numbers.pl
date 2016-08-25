#!/usr/bin/env perl
#
## Update Card Numbers from CSV
# Uses RPC::XML - http://search.cpan.org/~rjray/RPC-XML-0.79/lib/RPC/XML.pm
# to support https connections also install LWP::Protocol::https

# Usage: resp_number.pl sample.csv, or reads account details from stdin

use RPC::XML;
use RPC::XML::Client;

use strict;

my $server = "localhost"; my $port="9191";
my $token = "password";
my $url = "http://${server}:${port}/rpc/api/xmlrpc";

my $client = RPC::XML::Client->new($url);

my $updated;

while (<>){
  chomp;
  my ($user, $cardno) = split ",";

  my $resp = $client->send_request('api.setUserProperty', $token, $user,
                'card-number', RPC::XML::string->new($cardno));

  die "$resp\n" unless ref($resp);

  if ($resp->value == 1){
    $updated++
  } else {
    print STDERR "Failed to update $user\n";
  }

}
print "\nFinshed: $updated users have been updated\n";

