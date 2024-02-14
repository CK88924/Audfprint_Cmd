import subprocess
import os
import sys
import glob




def find_mp3_files(directory):
    """
    遍歷指定目錄及其子目錄下的所有 .mp3 文件。

    參數:
    - directory: 要遍歷的目錄的路徑字符串。

    返回:
    - mp3_files: 找到的 .mp3 文件的完整路徑列表。
    """
    # 確保路徑是绝對路徑
    directory = os.path.abspath(directory)

    # 建立用於查找 .mp3 文件的模式
    pattern = os.path.join(directory, '**', '*.mp3')

    # 使用 glob.glob 遍歷目錄及其所有子目錄下的 .mp3 文件
    # recursive=True 允许搜索所有子目錄
    mp3_files = glob.glob(pattern, recursive=True)

    return mp3_files


def New( audio_file_path:str):
    # 設置 audfprint.py 腳本的路徑
    audfprint_script_path = "audfprint.py"
    
    # 設置數據庫文件的路徑
    database_path = "music.pklz"  
    # 建立命令行指令
    cmd = [
        "python", audfprint_script_path, "new",
        "--dbase", database_path,
        audio_file_path
    ]

    # 使用 subprocess.run() 執行命令
    result = subprocess.run(cmd, capture_output=True, text=True)

    # 打印输出和（如果有的话）
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)


def Add( audio_file_path:str):
    # 設置 audfprint.py 腳本的路徑
    audfprint_script_path = "audfprint.py"
    
    # 設置數據庫文件的路徑
    database_path = "music.pklz"  
    # 建立命令行指令
    cmd = [
        "python", audfprint_script_path, "add",
        "--dbase", database_path,
        audio_file_path
    ]

    # 使用 subprocess.run() 執行命令
    result = subprocess.run(cmd, capture_output=True, text=True)

    # 打印输出和（如果有的话）
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)



def CreateDB( mp3_files:list ):
    if len(mp3_files)  == 1:
        New(mp3_files[0])

    elif len(mp3_files) > 1:
        New(mp3_files[0])
        for file in mp3_files[1:]:
            Add(file)
    else:
        print("請提供至少一首.mp3媒體以建立資料庫")
        sys.exit(1)
        

def Match(query_path: str):
    """
    使用 audfprint 命令行工具匹配一個查詢音頻文件。

    参数:
    - dbase_path: 數據庫文件的路徑。
    - query_path: 查詢音頻文件的路径。
    """
    # audfprint.py 腳本的路徑
    audfprint_script_path = "audfprint.py"
    dbase_path = "music.pklz"

    # 建立命令行命令
    cmd = ["python", audfprint_script_path, "match", "--dbase", dbase_path, query_path]

    # 執行命令
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("匹配结果：")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("匹配过程中出错：")
        print(e.stderr)

def MatchAct(query_files:list):
    if len(query_files) == 0:
        print("請提供至少一首.mp3媒體以做查詢")
        sys.exit(1)

    else:
        for file in query_files:
            Match(file)
    


         

if __name__ == '__main__':
    directory_path = 'tests/data/Music'
    mp3_files = find_mp3_files(directory_path)
    CreateDB(mp3_files)
    directory_path = 'tests/query'
    query_files = find_mp3_files(directory_path)
    MatchAct(query_files)
    
    
