import json
import yaml
from yaml.loader import UnsafeLoader


class fixer():
    """класс починки аватаров и анимаций"""
    def __init__(self, body_mesh_path:str,vrcsdk_ids_path:str) -> None:
        self.body_keys:dict
        self.vrcsdk_ids:dict
        self.load_data(body_mesh_path,vrcsdk_ids_path)
        pass
    
    def load_data(self,body_mesh_path,vrcsdk_ids_path):
        with open(vrcsdk_ids_path, "r") as f:
            self.vrcsdk_ids=json.load(f)
        with open(body_mesh_path, "r") as f:
            bodyL=f.readlines()
        bodyy="".join(bodyL[i][4::] for i in range(len(bodyL))).split("fullWeights", 1)[0].split("channels",1)[1]
        bodyy="channels"+bodyy
        #print(bodyy)
        j=yaml.load(bodyy,Loader=UnsafeLoader)
        bs_dict={}
        for g in j["channels"]:
            bs_dict[g["nameHash"]]=g["name"]
        self.body_keys=bs_dict
        


    def clsfix_part(self, k:dict):
        try:
            da=k["MonoBehaviour"]
            if "lipSync" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["descriptor"]
            if "blueprintId" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["pipeline"]
            if "pull" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["physbone"]
            if "insideBounds" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["physbonec"]
            if "allowSelf" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["crecv"]
            if "allowSelf" not in da.keys() and "collisionTags" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["csnder"]
            if "disableStationExit" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["vrcstation"]
            if "parameters" in da.keys() and da["m_Name"] != None:
                da["m_Script"]=self.vrcsdk_ids["expparams"]
            if "controls" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["expmenu"]
            if "goalWeight" in da.keys() and "layer" not in da.keys():
                da["m_Script"]=self.vrcsdk_ids["plc"]
            if "goalWeight" in da.keys() and "layer"  in da.keys():
                da["m_Script"]=self.vrcsdk_ids["alc"]
            if "trackingHead" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["atc"]
            if "enterPoseSpace" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["atps"]
            if "parameters" in da.keys() and "localOnly" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["apd"]
            if "disableLocomotion" in da.keys():
                da["m_Script"]=self.vrcsdk_ids["aloc"]
            k["MonoBehaviour"]=da
            return k
        except KeyError:return k


    def file_fix(self, path):
        res=[]
        firstlines=[]
        with open(path,"r") as f: #разборка
            o=f.readlines()
            beginning=o[0:2]
            k="".join(o[2::]).split("---")
            for _ in range(1, len(k)): 
                k[_]="---"+k[_]
                firstlines.append(k[_].split("\n")[0]+"\n")
            for j in range(len(k)):
                res.append(yaml.load("".join(k[j].split("\n")[1::][i]+"\n" for i in range(len(k[j].split("\n")[1::]))), Loader=UnsafeLoader))
            res=res[1::]

        out="".join(beginning) #сборка
        for k in range(len(res)):
            out+=firstlines[k]
            out+=yaml.dump(self.clsfix_part(res[k]))

        with open(path, "w") as f:
            f.write(out)
    
    def fix_anim(self,path):
        with open(path, "r") as f:
            _=f.readlines()
            animL=_[3::]
            first=_[0:3]

        animy="".join(animL[i] for i in range(len(animL)))
        k=yaml.load(animy,Loader=UnsafeLoader)
        try: 
            for a in reversed(k["AnimationClip"]["m_FloatCurves"]):
                try:
                    a["attribute"]=self.body_keys[int(a["attribute"].split(".")[1])]
                    a["attribute"]="blendShape."+a["attribute"]
                except: pass
        except KeyError: pass
        out=yaml.dump(k)

        #print(first)
        out="".join(first[i]  for i in range(len(first))) + out
        #print(out)
        with open(path, "w") as f:
            f.write(out)