# experimentの使い方

## パラメータ一覧
### basic
- path : rawデータが入っているディレクトリ。コピーして貼り付けるときは、"\" を "/" に変更
- cam_type : カメラのタイプ。選択できるカメラタイプは以下
	- max (8bitのmaxカメラ)
	- max10 (10bitのmaxカメラ)
	- sa4
	- mini
- image_width : 画像の幅
- image_height : 画像の高さ
- frame_start : 開始フレーム
- frame_end : 終了フレーム

### option
- smooth_size : 空間フィルタ(ガウシアン)のサイズ (ex. 0,2,4...etc)
- diff_min : 膜電位マップのROIの要求変化幅 (ex. 0,10,30...etc)
- interval : 動画作成時のフレームスキップ間隔　(ex. 2,5,10...etc)
- save_image : 膜電位マップの静止画を保存　(0:保存しない, 1:保存)
- plot : 点を選択し、膜電位波形を保存 (0:保存しない, 1:保存)

## 実行手順
1. experimentフォルダの中にあるparam.jsonを書き換え、保存 (Ctrl+S)
2. experinment.pyをダブルクリック
3. plotを選択した場合、グレースケールで表示されたカメラ画像から膜電位を確認したい点を選択し、Escキーを押して終了
4. パラメータで指定したpathの中に作成されたresultフォルダを確認


## 処理結果
- imgフォルダ (膜電位マップの画像)
- selectPoints.png (選択した点の画像)
- plot.png (選択した点の膜電位波形)
- vmem.mp4 (膜電位マップの動画)

## パラメータ一例

```
{
	"basic" : {
	    "path" : "C:/Users/MassieY/Documents/C001S0002",
	    "cam_type" : "sa4",
	    "image_width" : 256,
	    "image_height" : 256,
	    "frame_start" : 0,
	    "frame_end" : 2000
	},
	"option" : {
	    "smooth_size": 0,
	    "diff_min" : 0,
	    "interval" : 10,
	    "save_image" : 0,
	    "plot" : 0
	}
}
```