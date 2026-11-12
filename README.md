# heartrate

Polar H10とBluetooth Low Energy（BLE）で通信し、心拍データを取得するためのプロジェクトです。

## 環境構築

Python 3がインストールされていることを確認します。

```bash
python3 --version
```

プロジェクトのディレクトリへ移動し、仮想環境を作成します。

```bash
cd /Users/motojisaki/heartrate
python3 -m venv .venv
```

仮想環境を有効化します。

### macOS / Linux

```bash
source .venv/bin/activate
```

作業を終了するときは、次のコマンドで仮想環境を無効化できます。

```bash
deactivate
```

## Polar H10のアドレスを調べる

`findAddress.py`は、周辺にあるBLEデバイスを10秒間探索し、見つかったデバイスの名前とアドレスを表示するスクリプトです。

Polar H10を装着してBluetooth通信が可能な状態にしてから、次のコマンドを実行します。

```bash
python3 findAddress.py
```

実行結果の例：

```text
名前: Polar H10 XXXXXXXX
アドレス: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
--------------------
```

表示された一覧から、名前に`Polar H10`を含むデバイスを探します。表示されたアドレスは、Polar H10へ接続して心拍データを取得するプログラムで使用します。

デバイスが1台も見つからなかった場合は、`見つかりませんでした`と表示されます。その場合は、Polar H10を装着していること、パソコンのBluetoothが有効になっていること、ほかのアプリがPolar H10へ接続していないことを確認してください。

> `findAddress.py`はデバイスを探索するためのスクリプトであり、このスクリプト単体では心拍データを取得しません。

## 心拍データを取得する

`notify.py`は、Polar H10へ接続して心拍数とRR間隔を60秒間取得するスクリプトです。取得したデータはCSVファイルへ保存され、計測終了後に心拍数のグラフが表示されます。

グラフ表示に使用する`matplotlib`をインストールします。

```bash
python -m pip install matplotlib
```

### 接続するデバイス名の設定

`notify.py`の`find_device()`には、接続先のデバイス名が指定されています。

```python
device = await BleakScanner.find_device_by_name(
    "Polar H10 01080F31"
)
```

`findAddress.py`で確認した自分のPolar H10の名前に書き換えてください。デバイス名が一致しない場合は、`Device not found`と表示されます。

### 実行方法

Polar H10を装着し、次のコマンドを実行します。

```bash
python notify.py
```

接続に成功すると、ターミナルへ心拍数とRR間隔が表示されます。

```text
Connected to Polar H10 01080F31
Heart rate: 72
RR interval: 830.078125 ms
```

### 処理の流れ

1. `find_device()`が、指定された名前のPolar H10を探索します。
2. `get_heart_rate()`がPolar H10へ接続します。
3. Heart Rate MeasurementのUUID `2A37`に対する通知を開始します。
4. 通知を受信するたびに`print_heart_rate()`がデータを解析します。
5. 心拍数、RR間隔、受信時刻を`heart_rate_data`へ追加します。
6. 60秒後に通知を停止し、データをCSVへ保存してグラフを表示します。

### 受信データの解析

`print_heart_rate()`は、受信データの先頭にあるフラグを確認し、データ形式に応じて次の値を読み取ります。

- 心拍数：8ビット形式または16ビット形式の値を読み取ります。
- 消費エネルギー：データに含まれている場合は2バイト分を読み飛ばします。
- RR間隔：値を読み取り、`1/1024秒`単位からミリ秒へ変換します。
- 受信時刻：`time.time()`で取得したUNIX時刻を記録します。

RR間隔は、連続する心拍同士の時間間隔です。値は次の式でミリ秒へ変換されます。

```text
RR間隔（ミリ秒）= 受信値 × 1000 ÷ 1024
```

### 出力

計測終了後、`save_to_csv()`によって次のファイルへデータが保存されます。

- `csv/heart_rate.csv`：受信時刻、心拍数、RR間隔
- `csv/rr_intervals.csv`：RR間隔を1件ずつ分けたデータ

その後、`plot_heart_rate()`によって、計測開始からの経過時間を横軸、心拍数を縦軸としたグラフが表示されます。
