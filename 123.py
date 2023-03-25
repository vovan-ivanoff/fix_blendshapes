from fix_scripts import fixer
import os

src=r"F:\VRCAS_New7\exported\(rex)_avtr_994bfb62-88ca-4864-a251-78387e6e5a2c\ExportedProject\Assets"
nfixer=fixer(os.path.join(src,"Mesh\Body.asset"), "./vrc_scripts_list.json")


for _ in os.listdir(src+"\\AnimatorController\\"): nfixer.file_fix(src+"\\AnimatorController\\"+_)
for _ in os.listdir(src+"\\MonoBehaviour\\"): nfixer.file_fix(src+"\\MonoBehaviour\\"+_)
for _ in os.listdir(src+"\\AnimationClip\\"): nfixer.fix_anim(src+"\\AnimationClip\\"+_)
for i in os.listdir(src):
    if i.startswith("prefab") and i.endswith(".prefab"):
        nfixer.file_fix(src+"\\"+i)
