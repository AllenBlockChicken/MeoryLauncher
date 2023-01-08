from os.path import exists
from json import loads
from json import dumps
import zipfile

version = "1.8.9"
mcdir = "C:\Users\Allen\AppData\Local\Programs\Minecraft\正版专用\.minecraft"
maxMen = "1024M"
javaw_path = "C:\\Program Files\Java\\jre1.8.0_351\\bin\\javaw.exe"
username = "BlockChicken_"

'''
filename:解压的文件名
path:解压路径
'''


def unpress(filename, path):  # 解压文件
    Zip = zipfile.ZipFile(filename)
    for z in Zip.namelist():
        Zip.extract(z, path)
        Zip.close()


def allMyVersion(version: str, mcdir: str):  #
    if exists(mcdir + "\\versions\\" + version + "\\" + version + ".json"):
        return True
    else:
        return False


'''
    version:游戏版本
    javaw_path:javaw.exe路径
    maxMen:最大内存
    username:玩家名
    mcdir:游戏路径（.minecraft）
'''


def run(mcdir: str, version: str, javaw_path: str, maxMen: str, username: str):  # 启动游戏
    commandLine = str("")
    JVM = str("")
    classpath = str("")
    mc_args = str("")

    if ((not javaw_path == "")
            and (not version == "")
            and (not maxMen == "")
            and (not username == "")
            and (not mcdir == "")):

        if allMyVersion(version=version, ):
            version_json = open(mcdir + "\\versions\\" + version + "\\" + version + ".json")
            dic = loads(version_json.read())
            version_json.close()
            # 文件解压至natives文件夹
            for lib in dic["libraries"]:
                if "classifiers" in lib['downloads']:
                    for native in lib['downloads']:
                        if native == "artifect":
                            dirct_path = mcdir + "\\versions\\" + version + "\\" + version + "natives"  # 解压到的路径
                            filepath = mcdir + "\\libraries\\" + lib["downloads"][native]['path']  # 要解压的artifect库
                            unpress(filepath, dirct_path)

                        elif native == 'classifiers':
                            for n in lib['downloads'][native].values():
                                dirct_path = mcdir + "\\versions\\" + version + "\\" + version + "natives"  # 解压到的路径
                                filepath = mcdir + "\\libraries\\" + n["path"]
                                unpress(filepath, dirct_path)

            JVM = '"' + javaw_path + '" -XX:+UseG1GC -XX:-UseAdaptiveSizePolicy' + \
                  ' -XX:-OmitStackTraceInFastThrow -Dfml.ignoreInvalidMinecraftCertificates=True ' + \
                  '-Dfml.ignorePatchDiscrepancies=True -Dlog4j2.formatMsgNoLookups=true ' + \
                  '-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump ' + \
                  '-Dos.name="Windows 10" -Dos.version=10.0 -Djava.library.path="' + \
                  mcdir + "\\versions\\" + version + "\\" + version + "-natives" + \
                  '" -Dminecraft.launcher.brand=launcher ' + \
                  '-Dminecraft.launcher.version=1.0.0 -cp'
