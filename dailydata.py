import datetime, csv

htm1 = """\
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
    <header>
      <h1>片上大橋　風向風速監視システム</h1>
    </header>
    <br/>
    <a href="./windspeed.cgi">前のページへ</a>
    <br/><br/>
    <div class="data-table">
      <table border="1" style="border-collapse: collapse">
        <tr>
          <th>時刻</th>
          <th>風向</th>
          <th>風速[m/s]</th>
        </tr>
"""

htm2 = """\
      </table>
    </div>
    <br/>
    <a href="#">一番上に戻る</a>
    <br/><br/>
    <footer>
      <f1>岡山県備前県民局　東備地域維持補修班</f1>
    </footer>
  </center>
</body>
</html>
"""

fname = datetime.datetime.now().strftime("%Y%m%d")
if datetime.datetime.now().strftime("%H%M") == '0000':
    fname = str(int(fname) - 1)
else:
    pass
fpath = "/var/www/html/wind/data/" + fname + ".csv"
with open(fpath, encoding='shift-jis') as f:
    reader = csv.reader(f)
    datalist = [row for row in reader]

opath = "/var/www/html/wind/dailydata.html"
with open(opath, 'w') as f:
    print(htm1, file=f)

    ri = 3
    while True:
        try:
            print("        <tr>", file=f)
            print("          <td>" + datalist[ri][0] + "</td>", file=f)
            print("          <td>" + datalist[ri][2] + "</td>", file=f)
            print("          <td>" + datalist[ri][1] + "</td>", file=f)
            print("        </tr>", file=f)
            ri += 1
        except Exception:
            break

    print(htm2, file=f)
