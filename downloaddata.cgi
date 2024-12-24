#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use File::Spec;
use Archive::Zip qw(:ERROR_CODES :CONSTANTS);
use Encode;
use POSIX qw(strftime);

my $cgi = CGI->new;

# エラーの場合
my $err = <<"ERR";
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>片上大橋　風向風速監視システム</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <center>
    <br><p>ファイルが存在しません<br><br>選択した期間が間違っている可能性があります</p><br><br>
    <a href="./downloaddata.html" class="btn_01 pad4_10">前のページへ</a><br><br>
    <a href="./windspeed.cgi" class="btn_01 pad4_10">トップページ</a>
  </center>
</body>
</html>
ERR

# ディレクトリを指定
my $dir1 = '/var/www/html/wind/data';
my $dir2 = '/var/www/html/wind/pic';

# htmlから受け取った値を変数へ
my $selected_dir = $cgi->param('directory') eq 'dir1' ? $dir1 : $dir2;
my $date_start = $cgi->param('date-start');
my $date_end = $cgi->param('date-end');

# 日付フォーマットを変換
$date_start =~ s/-//g;
$date_end =~ s/-//g;

# ファイルを選択
opendir(my $dh, $selected_dir) or die "cannot open $selected_dir: $!";
my @files = readdir($dh);
closedir($dh);

# ファイルをzipファイルに追加
my $zip = Archive::Zip->new();
my $file_count = 0;

for my $file (@files) {
    next if $file =~ m/^\./;

    my $filepath = File::Spec->catfile($selected_dir, $file);
    if ($selected_dir eq $dir1) {
        # csv
        if ($file =~ /^(\d{8})\.csv$/) {
            my $file_date = $1;
            if ($file_date ge $date_start && $file_date le $date_end) {
                $zip->addFile($filepath, $file);
                $file_count++;
            }
        }
    } else {
        # jpg
        if ($file =~ /^(\d{12})\.jpg$/) {
            my $file_date = $1;
            if ($file_date ge $date_start && $file_date le $date_end) {
                $zip->addFile($filepath, $file);
                $file_count++;
            }
        }
    }
}

# zipファイルの内容確認
if ($file_count == 0) {
    print $cgi->header(-type => 'text/html', -charset => 'UTF-8');
    print $err;
} else {
    print $cgi->header(-type => 'application/octet-stream', -attachment => 'download.zip');
    unless ($zip->writeToFileHandle(\*STDOUT) == AZ_OK) {
        die 'Failed to create zip file';
    }
}
