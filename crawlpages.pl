#!/usr/bin/perl
use strict;
use LWP;
use URI::Escape;

sub save_file {
    my ($filename, $file_data) = @_;
    open OUT_FILE, ">$filename";
    print OUT_FILE $file_data;
    close OUT_FILE
}

sub dump_page {
    my ($page_prefix, $page_no) = @_;
	my $filename = sprintf(".\\data\\bible\\%s%d.txt", $page_prefix, $page_no);
	if(-e $filename) {
		return;
	}
	my $fmt_ops="&include-first-verse-numbers=false&include-verse-numbers=false&include-footnotes=false&include-passage-references=false&include-headings=false&include-subheadings=false&include-passage-horizontal-lines=false&include-heading-horizontal-lines=false&include-short-copyright=false";
	my $req_url = sprintf("http://www.esvapi.org/v2/rest/passageQuery?key=IP&passage=%s+%d&output-format=plain-text%s",
		$page_prefix,
		$page_no,
		$fmt_ops);
    my $req  = HTTP::Request->new(GET => $req_url);
    my $ua = LWP::UserAgent->new;
    my $res = $ua->request($req);

    if($res->code == 200) {
		printf("Save page to %s.\n", $filename);
        save_file($filename, $res->content);
    }
    else {
        printf("Bad request for page %s %d.\n", $page_prefix, $page_no);
    }
}

sub dump_pages {
    my ($prefix, $max_number) = @_;
	for(my $i = 1; $i <= $max_number; $i++) {
		dump_page($prefix, $i);
	}
}

my @pages_table = (
	["Genesis", 50],
    ["Exodus", 40],
    ["Leviticus", 27],
    ["Numbers", 36],
    ["Deuteronomy", 34],
    ["Joshua", 24],
    ["Judges", 21],
    ["Ruth", 4],
    ["1 Samuel", 31],
    ["2 Samuel", 24],
    ["1 Kings", 22],
    ["2 Kings", 25],
    ["1 Chronicles", 29],
    ["2 Chronicles", 36],
    ["Ezra", 10],
    ["Nehemiah", 13],
    ["Esther", 10],
    ["Job", 42],
    ["Psalms", 150],
    ["Proverbs", 31],
    ["Ecclesiastes", 12],
    ["Song of Solomon", 8],
    ["Isaiah", 66],
    ["Jeremiah", 52],
    ["Lamentations", 5],
    ["Ezekiel", 48],
	["Daniel", 12],
	["Hosea", 14],
	["Joel", 3],
	["Amos", 9],
	["Obadiah", 1],
	["Jonah", 4],
	["Micah", 7],
	["Nahum", 3],
	["Habakkuk", 3],
	["Zephaniah", 3],
	["Haggai", 2],
	["Zechariah", 14],
	["Malachi", 4],
	["Matthew", 28],
	["Mark", 16],
	["Luke", 24],
	["John", 21],
	["Acts", 28],
	["Romans", 16],
	["1 Corinthians", 16],
	["2 Corinthians", 1.],
	["Galatians", 6],
	["Ephesians", 6],
	["Philippians", 4],
	["Colossians", 4],
	["1 Thessalonians", 5],
	["2 Thessalonians", 3],
	["1 Timothy", 6],
	["2 Timothy", 4],
	["Titus", 3],
	["Philemon", 1],
	["Hebrews", 13],
	["James", 5],
	["1 Peter", 5],
	["2 Peter", 3],
	["1 John", 5],
	["2 John", 1],
	["3 John", 1],
	["Jude", 1],
	["Revelation", 22]);

sub main {
	foreach my $dump_record(@pages_table) {
		dump_pages($dump_record->[0], $dump_record->[1]);
	}
}

main();
