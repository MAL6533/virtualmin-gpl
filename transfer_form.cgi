#!/usr/local/bin/perl
# Display server transfer form

require './virtual-server-lib.pl';
&ReadParse();
$d = &get_domain($in{'dom'});
&can_transfer_domain($d) || &error($text{'transfer_ecannot'});
&ui_print_header(&domain_in($d), $text{'transfer_title'}, "", "transfer");

print &ui_form_start("transfer.cgi");
print &ui_hidden("dom", $d->{'id'}),"\n";
print &ui_table_start($text{'transfer_header'}, undef, 2);

# Domain being transferred
my @subs = ( &get_domain_by("parent", $d->{'id'}),
	     &get_domain_by("alias", $d->{'id'}) );
print &ui_table_row($text{'transfer_dom'},
	"<tt>".&show_domain_name($d)."</tt>".
	(@subs ? " ($text{'transfer_subs'})" : ""));

# Destination system
my @hosts = &get_transfer_hosts();
my $hfield = &ui_textbox("host", undef, 40, 0, undef, "autocomplete=off")." ".
	     &ui_checkbox("savehost", 1, $text{'transfer_savehost'}, 0);
if (@hosts) {
	print &ui_table_row($text{'transfer_host'},
		&ui_radio_table("host_mode", 1,
		    [ [ 1, $text{'transfer_host1'},
			&ui_select("oldhost", $hosts[0]->[0],
				   [ (map { $_->[0] } @hosts) ]) ],
		      [ 0, $text{'transfer_host0'},
			$hfield ] ]));
	}
else {
	# No saved hosts yet
	print &ui_table_row($text{'transfer_host'}, $hfield);
	}

# Root password
print &ui_table_row($text{'transfer_pass'},
	&ui_password("hostpass", undef, 20)." ".
	$text{'transfer_passdef'});

# Delete from source
print &ui_table_row($text{'transfer_delete'},
	&ui_radio("delete", 0, [ [ 2, $text{'transfer_delete2'} ],
				 [ 1, $text{'transfer_delete1'} ],
				 [ 0, $text{'transfer_delete0'} ] ]));

# Over-write when restoring?
print &ui_table_row($text{'transfer_overwrite'},
	&ui_yesno_radio("overwrite", 0));

print &ui_table_end();
print &ui_form_end([ [ undef, $text{'transfer_ok'} ] ]);

&ui_print_footer(&domain_footer_link($d),
		 "", $text{'index_return'});
