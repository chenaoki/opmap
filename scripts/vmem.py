# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from opmap.opmap import VmemMap, PhaseMap, PhaseVarianceMap
import json

f = open('vmem_sample.json', 'r')
data = json.load(f)
vmem_params = data["Vmem"]["Basic"]
option_params = data["Vmem"]["Option"]
wave_params = data["Wave_Display"]

def QandA(question):
    while True:
        print(question)
        answer = raw_input()
        assert answer != 'q'
        if answer == 'y' or answer == 'n':
            break
        else:
            print(u'yまたはnを入力してください。')
    return answer

print(u'qを押すとプログラムが終了します。')


vmem = VmemMap(**vmem_params)
if option_params["smooth_size"] > 0:
    vmem.smooth(size=option_params["smooth_size"])
vmem.setDiffRange(option_params["diff_min"])
vmem.showMovie()
plt.close()

question = u'この画像を保存しますか？(yまたはnを入力してください。)'
save_fig = QandA(question)
if save_fig == 'y':
    save_path = vmem_params["path"] + "/opmap_results"
    vmem.saveImage(save_path)

question = u'波形を表示しますか？(yまたはnを入力してください。)'
wave_output = QandA(question)
if wave_output == 'y':
    save_path = vmem_params["path"] + "/wave_results"
    print(u'電位波形を確認したい点を選んでください。')
    points = vmem.selectPoints()
    if wave_params["filter_size"] > 0:
        vmem.plot(points, filter_size=wave_params["filter_size"], savepath=save_path)
