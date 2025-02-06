from PIL import Image
import os
import re

CharactersDict = {
    "sr_f01":["0101","0102","0201","0202","0301","0302","0401"],
    "sr_f02":["0103","0203","0303"],
    "sr_f03":["0101","0102","0201","0202","0301","0302"],
    "sr_f04":["0103","0203","0303"],
    "sr_f05":["0501","0502"],
    "sr_f06":["0601","0602"],
    "sr_f07":["0603"],
    "sr_f11":["11","12"],
    "sr_f12":["13"],
    "sr_f21":["21","22"]
    }

"""
SummerPocketsCharactersDict = {
    "sk_f01":["01","02"],
    "sk_f02":["03"],
    "sk_f11":["11","12"],
    "um_f01":["01","02","03"],
    "um_f11":["11","12","13"],
    "tm_f01":["01","02","03"],
    "tm_f11":["0111","0112","0113","0211","0212","0213"],
    "tm_f12":["0312"],
    "ts_f01":["01","02"],
    "in_f01":["01","02","03","04"],
    "tn_f01":["01","02","03"],
    "tn_f02":["0104"],
    "tn_f03":["0204","0304","0704"],
    "tn_f04":["0401","0402","0403","0501","0502","0503","0601","0602","0603"],
    "tn_f05":["0404"],
    "tn_f06":["0504","0604"],
    "tn_f07":["01","02","03"],
    "tn_f08":["01","02","03"],
    "tn_f09":["0101","0102","0103","0201","0202","0203","0301","0302","0303","0701","0702","0703"],
    "ky_f01":["01"],
    "ky_f02":["01"],
    "ky_f03":["0102","0202"],
    "ky_f04":["0102","0202"],
    "ky_f05":["0302","0402"],
    "ky_f06":["0302","0402"],
    "ko_f01":["01"],
    "ko_f02":["02"],
    "km_f01":["01"],
    "km_f02":["02"],
    "km_f03":["03"],
    "km_f04":["09"],
    "km_f11":["11","12","13"],
    "ao_f01":["01","02","03"],
    "ao_f02":["04"],
    "ao_f11":["11","12","13","14"],
    "sr_f01":["0101","0102","0201","0202","0301","0302","0401"],
    "sr_f02":["0103","0203","0303"],
    "sr_f03":["0101","0102","0201","0202","0301","0302"],
    "sr_f04":["0103","0203","0303"],
    "sr_f05":["0501","0502"],
    "sr_f06":["0601","0602"],
    "sr_f07":["0603"],
    "sr_f11":["11","12"],
    "sr_f12":["13"],
    "sr_f21":["21","22"],
    "sc_f01":["01","02","03"],
    "sj_f01":["01","02"],
    "sj_f02":["01","02"],
    "ru_f01":["01","02","03"],
    "ru_f02":["01","02","03"],
    "sz_f01":["01","03"],
    "sz_f02":["02"],
    "sz_f11":["11","12","13"],
    "mk_f01":["01","02"],
    "mk_f11":["11","12","13"],
    "mk_f14":["14","15"]
    }
"""

partImageFolder = ".\\unpackgbo\\"
g00Folder = ".\\org\\"
outFolder = ".\\out\\"

def search(pattern,folder):
    arr = os.listdir(folder)
    tmp = []
    for f in arr:
        if re.match(pattern, f):
            tmp.append(f)
        """if target in f:
            tmp.append(f)"""
    return tmp

def getOffset(partimage,baseplate):
    with open(partimage,"rb") as f:
        f.seek(25)
        datax1 = f.read(2)
        f.read(2)
        datay1 = f.read(2)
        f.close()
    with open(baseplate,"rb") as f:
        f.seek(25)
        datax2 = f.read(2)
        f.read(2)
        datay2 = f.read(2)
        f.close()
    datax1s = int.from_bytes(datax1,"little")
    datay1s = int.from_bytes(datay1,"little")
    datax2s = int.from_bytes(datax2,"little")
    datay2s = int.from_bytes(datay2,"little")
    #print(datax1s,datay1s,datax2s,datay2s)
    x = abs(datax1s-datax2s)
    y = abs(datay1s-datay2s)
    return x,y

def mergeImage(partimage,baseplate,offsetList,outimg):
    backimg = Image.open(baseplate)
    faceimg = Image.open(partimage)
    backimg.paste(faceimg, offsetList, mask = faceimg)
    backimg.save(outimg)

def main():
    mode1 = input("input to choose far(1), normal(2), close(3) or all(a): ")
    mode2 = input("input to choose longer(y), not(n) or both(a): ")

    def getG00Path(pngName):
        return g00Folder + pngName.split(".")[0] + ".g00"
    def getOutName(part,base,num):
        name = part.split(".")[0] + "_" + base.replace("bs" + num + "_","")
        print("processed",part,base)
        return name

    def mainlengthed(num,char0,char0List,char1,prefix):
        char1List = search(prefix + "bs" + num + "_" + char0.split("_")[0] + ".*" + char1 + "01.png", partImageFolder)
        for tar1 in char1List:
            for tar0 in char0List:
                #print(tar0,tar1)
                offsets = getOffset(getG00Path(tar0),getG00Path(tar1))
                mergeImage(partImageFolder+tar0,partImageFolder+tar1,offsets,outFolder+getOutName(tar0,tar1,num))

    def mainDistanced(num):
        for char0 in CharactersDict:
            char0List = search("bs" + num + "_" + char0, partImageFolder)
            for char1 in CharactersDict[char0]:
                if mode2 == "y":
                    mainlengthed(num,char0,char0List,char1,"f_")
                elif mode2 == "n":
                    mainlengthed(num,char0,char0List,char1,"")
                elif mode2 == "a":
                    for p in ["","f_"]:
                        mainlengthed(num,char0,char0List,char1,p)
                else:
                    print("illegal mode2")

    if mode1 == "a":
        for i in range(1,4):
            mainDistanced(str(i))
    elif mode1 in ['1','2','3']:
        mainDistanced(mode1)
    else:
        print("illegal mode1")

main()