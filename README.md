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
