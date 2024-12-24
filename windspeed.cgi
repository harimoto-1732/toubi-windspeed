#!/usr/bin/perl


use strict;
use warnings;

# debug ######################
my $debug_yama = 0;
sub yamane_debug {
	if ($debug_yama == 1) {
		#日時の取得
		my ($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime();

		#日時の調整
		$mon++;	#月数には1を足す。
		$year = 1900+$year;	#年数には、1900を足す。
		$mon = sprintf("%.2d",$mon);	#2桁表示に統一する。
		$mday = sprintf("%.2d",$mday);
		$hour = sprintf("%.2d",$hour);
		$sec = sprintf("%.2d",$sec);
		$min = sprintf("%.2d",$min);

		#フォーマット指定 例　2003/03/15(土) 20:12:12
		my $today = "$year/$mon/$mday $hour:$min:$sec";
	
		open(DATAFILE, ">>", "yamane_log.txt") or die("Error:$!");
		print DATAFILE $today;
		print DATAFILE $_[0];
		print DATAFILE "\n";
		close(DATAFILE);
	}
}

# コマンド作成データ
my ($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime();
$mon++;	#月数には1を足す。
$mon = sprintf("%.2d",$mon);	#2桁表示に統一する。
$mday = sprintf("%.2d",$mday);
# UTF8 文字コード変換出力ファイル
my $windfile = sprintf("./data/%d%.2d%.2d.csv", 1900+$year, $mon, $mday);
my $dldate = sprintf("%d%.2d%.2d", 1900+$year, $mon, $mday);
my $time = sprintf("%.2d:%.2d", $hour, $min);
my $line;
my $latest_time = substr($time, 0, 4);
my ($n1, $n2, $n3, $n4, $n5, $n6, $n7, $n8, $n9);

=pod
my $ii = 0;
open (IN, "< $windfile") or die "$!";
while ( <IN> ) {
	($n1, $n2, $n3, $n4, $n5, $n6, $n7, $n8, $n9) = split(/,/);
	# 最終ラインまで読む（データ量が少ない為）
}
close IN;
=cut

#=pod
# ファイル存在チェック
yamane_debug("- $windfile -");
if( !(-f $windfile) ) {
	print "\n<!doctype html>\n\n";

	print "<html lang=\"ja\">\n";
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n";
	print "<head><title>片上大橋　風向風速監視システム</title></head>\n";
	print "<body>\n";
	print "<br/>\n";
	print "<p>$windfile ファイルが存在しません。</p>\n";
	print "<p>処理を中止します。</p>\n";
	print "</body>\n";
	print "</html>\n";

	exit;
}
#=cut

open (INN, "< $windfile") or die "$!";
my @arr = <INN>;
close( INN );
foreach my $element (@arr) {
	if (substr($element, 0, 4) eq $latest_time) {
		$line = $element;
		last;
	}
}
if (defined $line) {
	($n1, $n2, $n3, $n4, $n5, $n6, $n7, $n8, $n9) = split(/,/, $line);
} else {
	warn "No matching element.";
}
# 最新測定時間
$latest_time = $n1;
# 風向、風速取得
my $wind_direction = $n3;
my $wind_average = $n2;
#print $windo, "\n";
#print $average, "\n";
# <!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">
my $myhead = <<"HEADD";
content-type: text/html

<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="Content-Style-Type" content="text/css">
<meta name="viewport" content="width=device-width">
<title>片上大橋　風向風速監視システム</title>
</head>
<body bgcolor="#ffffff" text="#000000" link="#0000ff" vlink="#ff00ff" alink="#ff0000">
<center>
HEADD

my $mytaile = <<"TAILE";
</center>
</body>
</html>
TAILE

my $mydisp_1 = <<"DISP_1";
	<div class="inner">
		<div class="gray-box">
		平均風向
		</div>
		<div class="gray-box">
		平均風速
		</div>	
	</div>
DISP_1

my $mydisp_c = <<"DISP_c";
	<div class="camera">
		<br/>
		<a href="http://219.121.50.242:8000"><img width=100% src="../pic/cam.jpg"></a>
	</div>
DISP_c

my $mydisp_2 = <<"DISP_2";
	<div class="button">
		<br/>
		<a href="./dailydata.html" class="btn_01 pad4_10" style="display:inline-block;">日報表示</a><a href="" class="btn_01 pad4_10" style="display:inline-block;">ダウンロード</a>
		<br/><br/>
	</div>
	</TD> 
</TR>
</TABLE>
<footer><f1>岡山県備前県民局　東備地域維持補修班</f1></footer>
DISP_2


# ここから処理
print $myhead;

print "<header>\n";
print "  <h1>片上大橋　風向風速監視システム</h1>\n";
print "</header>\n";

# TABLEを設定
print "<table width=\"250px\" border=\"0\">\n";
#print "<thead><TR><TH ALIGN=center ROWSPAN=1 BGCOLOR=\"#4169e1\"><FONT SIZE=\"+1\"; color=#ffffff>倉敷みなと大橋</FONT></TH></TR></thead>\n";
print "<TR>\n";
print "	<TD ALIGN=center ROWSPAN=1 BGCOLOR=\"#FFFFFF\"><FONT SIZE=\"-1\">\n";
print "		<br/>", "\n";
print "		<div style=\"line-height:90%\"; class=\"right-pos\">\n";
# 日付を設定
my $mydate = sprintf("%d/%.2d/%.2d %s", $year+1900, $mon, $mday, $latest_time);
print "			<p>$mydate　</p>\n";
print "		</div>", "\n";	
print $mydisp_1;
# 風向、風速を設定
print "		<div class=\"inner\">\n";	
print "		<div class=\"blue-box\">\n";	
print "		$wind_direction\n";	
print "		</div>\n";	
print "		<div class=\"blue-box\">\n";	
print "		$wind_average m/s\n";	
print "		</div>\n";	
print "	</div>\n";	
print $mydisp_c;
my $picfile = "../pic/cam.jpg";
my $modiftime = substr(localtime((stat $picfile)[9]), 11, 5);
print "    <p>$modiftime </p>\n";
print $mydisp_2;
print $mytaile;


