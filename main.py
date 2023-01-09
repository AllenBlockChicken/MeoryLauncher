from os.path import exists
from json import loads
from json import dumps
import zipfile
from os import system
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

print("Meory Launcher!")
version = input("请输入版本号（例如：1.8.9）：")
mcdir = filedialog.askdirectory(title='选择".minecraft"文件夹')
javaw_path = filedialog.askopenfilename(title='选择"javaw.exe"文件（通常在“C:/Program Files/Java/Java版本/bin/”中')
username = input("请输入用户名：")
maxMen = input("请输入最大内存（例：1024M）：")

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

        if allMyVersion(version=version,mcdir=mcdir ):
            version_json = open(mcdir + "\\versions\\" + version + "\\" + version + ".json")
            dic = loads(version_json.read())
            version_json.close()
            # 文件解压至natives文件夹
            for lib in dic["libraries"]:
                if "classifiers" in lib['downloads']:
                    for native in lib['downloads']:
                        if native == "artifact":
                            dirct_path = mcdir + "\\versions\\" + version + "\\" + version + "natives"  # 解压到的路径
                            filepath = mcdir + "\\libraries\\" + lib["downloads"][native]['path']  # 要解压的artifact库
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

            classpath += '"'

            for lib in dic["libraries"]:
                if not 'classifiers' in lib["downloads"]:
                    normal = mcdir + "\\libraries\\" + lib["downloads"]["artifact"]["path"]  # 普通库路径
                    classpath += normal + ";"  # 将普通库路径追加到-cp后面

            classpath = classpath + mcdir + "\\versions\\" + version + "\\" + version + ".jar" + '"'
            JVM = JVM + " " + classpath + " -Xmx" + maxMen + " -Xmn256m -Dlog4j.formatMsgNoLookups=true"

        mc_args += dic["mainClass"] + " "
        for arg in dic["arguments"]["game"]:
            if isinstance(arg, str):
                mc_args += arg + " "
            elif isinstance(arg, dict):  # 无论是什么，只要是在大括号里括着的，都被python认为是字典类型
                if isinstance(arg["value"], list):
                    for a in arg["value"]:
                        mc_args += a + " "
                elif isinstance(arg["value"], str):
                    mc_args += arg["value"] + " "
        # 将模板替换为具体数值
        mc_args = mc_args.replace("${auth_player_name}", username)  # 玩家名称
        mc_args = mc_args.replace("${version_name}", version)  # 版本名称
        mc_args = mc_args.replace("${game_directory}", mcdir)  # mc路径
        mc_args = mc_args.replace("${assets_root}", mcdir + "\\assets")  # 资源文件路径
        mc_args = mc_args.replace("${assets_index_name}", dic["assetIndex"]["id"])  # 资源索引文件名称
        mc_args = mc_args.replace("${auth_uuid}", "{}")  # 由于没有写微软登录,所以uuid为空的
        mc_args = mc_args.replace("${auth_access_token}", "{}")  # 同上
        mc_args = mc_args.replace("${clientid}", version)  # 客户端id
        mc_args = mc_args.replace("${auth_xuid}", "{}")  # 离线登录,不填
        mc_args = mc_args.replace("${user_type}", "Legacy")  # 用户类型,离线模式是Legacy
        mc_args = mc_args.replace("${version_type}", dic["type"])  # 版本类型
        mc_args = mc_args.replace("${resolution_width}", "1000")  # 窗口宽度
        mc_args = mc_args.replace("${resolution_height}", "800")  # 窗口高度
        mc_args = mc_args.replace("-demo ", "")  # 去掉-demo参数，退出试玩版

        commandLine = JVM + " " + mc_args

        bat = open("pyLauncher.bat","w")
        bat.write(commandLine)
        bat.close()
        system("pyLauncher.bat")


run(mcdir,version,javaw_path,maxMen,username)

