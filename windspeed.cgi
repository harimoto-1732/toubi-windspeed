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
<style>
.right-pos {
	background-color: #ffffff;
}
p {
  text-align: right;
}
.pad4_10	{ padding: 4px 10px; }
.btn_01 { text-align: center; text-decoration: none; 
	color:  #000;	/* 文字色 */
	-webkit-border-radius: 3px; -moz-border-radius: 3px;
	text-shadow: 0 -1px 1px #FFF, -1px 0 1px #FFF, 1px 0 1px #aaa;
	-webkit-box-shadow: 1px 1px 2px #E7E7E7; -moz-box-shadow: 1px 1px 2px #E7E7E7;
	background: -moz-linear-gradient(top, #fff, #F1F1F1 1%, #F1F1F1 50%, #000000 99%, #ccc); 
	background: -webkit-gradient(linear, left top, left bottom, from(#fff), color-stop(0.01, #F1F1F9), color-stop(0.5, #F1F1F1), color-stop(0.99, #DFDFDF),to(#ccc));
	border: 1px solid; border-color: #ccc #999 #999 #ccc;
	font-size: 100%; }
.inner {
	padding: 1;
	display: flex;
	justify-content: space-evenly;
}
.gray-box{
	width:140px;
	height:30px;
	color:  #fff;               /* 文字色 */
	background:#808080;
	border-radius:  2px;        /* 角丸指定 */
	font-size: 14px;
	font-weight: bold;
	text-align:center;
	height:30px;
	line-height:30px;
}
.blue-box{
	width:140px;
	height:30px;
	color:  #fff;               /* 文字色 */
	background:#4169e1;
	border-radius:  2px;        /* 角丸指定 */
	font-size: 14px;
	font-weight: bold;
	text-align:center;
	height:30px;
	line-height:30px;
}

header {
width: 292px;
padding: 10px;
background: #4169e1;
color: #FFF;
}
h1 {
font-weight: bold;
font-size: 100%;
}

footer {
width: 292px;
padding: 10px;
background: #4169e1;
color: #FFF;
}
f1 {
font-weight: bold;
font-size: 80%;
}
</style>

</head>
<br/>
<body bgcolor="#ffffff" text="#000000" link="#0000ff" vlink="#ff00ff" alink="#ff0000">
<center>

<br/>
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

my $mydisp_2 = <<"DISP_2";
	</div>
		<br/><br/>
		過去データ
		<br/><br/>
		<a href="./dailylist.html" class="btn_01 pad4_10">　日報表示　</a>
		<br/><br/>
		<a href="./fileselect.html" class="btn_01 pad4_10">ダウンロード</a>
		<br/><br/><br/>
	</TD> 
</TR>
</TABLE>
<footer><f1>岡山県備前県民局　東備地域維持補修班</f1></footer>
DISP_2


# ここから処理
print $myhead;

print "<header><h1>片上大橋　風向風速監視システム</h1></header>\n";

# TABLEを設定
print "<TABLE WIDTH=312 BORDER=1 CELLSPACING=0 CELLPADDING=4>\n";
#print "<thead><TR><TH ALIGN=center ROWSPAN=1 BGCOLOR=\"#4169e1\"><FONT SIZE=\"+1\"; color=#ffffff>倉敷みなと大橋</FONT></TH></TR></thead>\n";
print "<TR>\n";
print "	<TD ALIGN=center ROWSPAN=1 BGCOLOR=\"#FFFFFF\"><FONT SIZE=\"-1\">\n";
print "		<br/><br/>", "\n";
print "		最新データ", "\n";
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
	
print $mydisp_2;
print $mytaile;


