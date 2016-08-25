# Update Card Numbers from CSV
# Uses RPC::XML - http://search.cpan.org/~rjray/RPC-XML-0.79/lib/RPC/XML.pm
# Usage: update_card_number.pl sample.csv

use RPC::XML;
use RPC::XML::Client;

$server = "papercut";
$token = "this_is_my_token";
$url = "http://" . $server . ":9191/rpc/api/xmlrpc";


my $input = $ARGV[0] or die "No input file was found \n";
open( my $data, '<', $input ) or die "Failed to open '$input' \n";

$client = RPC::XML::Client->new($url);

while (my $line = <$data>){
	chomp $line;
	my @records = split ",", $line;
	
	$update_card = $client->send_request( 'api.setUserProperty', $token, $records[0], 'card-number', RPC::XML::string->new($records[1]));

	if ($update_card->value == 1){
		print $records[0] . " has been updated\n";
	} else {
		print "Failed to update " . $records[0] . "\n";
	}

}

print "Finished \n";