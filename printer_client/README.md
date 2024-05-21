# domprinter/printer_client

## Usage

如果是在Windows环境下，请使用printer4win.py。并按照在文件开头找到以下内容进行配置。该Windows下的方案使用SumatraPDF作为pdf打印的方法，请先下载SumatraPDF的可执行文件。
```python
CONFIG = {
    "HEADERS": {'content-type': 'application/json'},
    "BASE_URL": "",# 更改为你的打印服务器的实际路径，例如http://admin:admin@127.0.0.1:8080/print-task
    "SUMATRA_PATH": "",  # 更改为SumatraPDF的实际路径，例如D:\SumatraPDF.exe
    "PRINTER_NAME": "" # 更改为你想使用的打印机名称，例如HP LaserJet Professional
}
```

如果是在Linux环境下，可以直接使用main.py启动。

### Windows
```bash
git clone https://github.com/Dup4/domprinter.git

cd domprinter/printer_client

pip3 install -U -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

python printer4win.py
```

### Linux
```bash
git clone https://github.com/Dup4/domprinter.git

cd domprinter/printer_client

pip3 install -U -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

BASE_URL="your-base-url" python3 main.py
```

