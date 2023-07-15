from fix_scripts import fixer
import os
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("-s","--src", type=str,help="Assets dir for fixing avatars", required=True)
parser.add_argument("-l","--list", type=str,help="Json list diir for string swapping(default set to wd)",default="./vrc_scripts_list.json")
args = parser.parse_args()

nfixer=fixer(os.path.join(args.src,"Mesh\Body.asset"), args.list)

for _ in os.listdir(args.src+"\\AnimatorController\\"): 
    nfixer.file_fix(args.src+"\\AnimatorController\\"+_)
    print(f"Controller:{_}")
for _ in os.listdir(args.src+"\\MonoBehaviour\\"): 
    nfixer.file_fix(args.src+"\\MonoBehaviour\\"+_)
    print(f"menu:{_}")
for _ in os.listdir(args.src+"\\AnimationClip\\"): 
    nfixer.fix_anim(args.src+"\\AnimationClip\\"+_)
    print(f"Anim:{_}")
for i in os.listdir(args.src):
    if i.startswith("prefab") and i.endswith(".prefab"):
        nfixer.file_fix(args.src+"\\"+i)
