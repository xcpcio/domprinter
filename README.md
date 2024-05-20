<img align="right" width="96" src="./assets/go_logo.png">

# DOMPrinter

[![Test](https://github.com/xcpcio/domprinter/actions/workflows/test.yml/badge.svg)](https://github.com/xcpcio/domprinter/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/xcpcio/domprinter/branch/main/graph/badge.svg?token=5Q80B98LPI)](https://codecov.io/gh/xcpcio/domprinter)
[![Go Report Card](https://goreportcard.com/badge/github.com/xcpcio/domprinter)](https://goreportcard.com/report/github.com/xcpcio/domprinter)
[![GitHub go.mod Go version](https://img.shields.io/github/go-mod/go-version/xcpcio/domprinter)](https://github.com/xcpcio/domprinter/blob/main/go.mod)
[![Github release](https://img.shields.io/github/release/xcpcio/domprinter.svg)](https://github.com/xcpcio/domprinter/releases)
[![platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://github.com/xcpcio/domprinter/releases)
[![License][license-image-mit]][license-link-mit]

* [中文版](./README.cn.md)

## Usage

### Server

首先需要在 Database 里面创建一张表：[建表语句 SQL](./biz/model/sql/print_task.sql)，DB 你可以复用 DOMjudge 的那个 Database，也可以自己再建一个新的 Database

然后通过 Docker 启动 DOMPrinter 服务，可以参考以下脚本启动容器：

```bash
IMAGE="dup4/domprinter:0.0.26"

docker run \
    -d \
    --restart=always \
    --name="${your container name}" \
    -e TZ=Asia/Shanghai \
    -e MYSQL_HOSTNAME="${your db host name}" \
    -e MYSQL_PORT="${your db port}" \
    -e MYSQL_USERNAME="${your db username}" \
    -e MYSQL_PASSWORD="${your db password}" \
    -e MYSQL_SCHEMA="${your db database name}" \
    -e AUTH_USERNAME="${auth username, used for printer client}" \
    -e AUTH_PASSWORD="${auth password}" \
    -p 80:8888 \ # You can change the mapped ports as needed
    "${IMAGE}"
```

然后 DOMPrinter 的服务端就搞定了

### Client

然后需要在能够控制打印机的机器上，安装并启动 [printer_client](./printer_client/README.md)

如果是在Windows环境下，请使用printer4win.py。并按照在文件开头找到以下内容进行配置。该Windows下的方案使用SumatraPDF作为pdf打印的方法，请先下载SumatraPDF的可执行文件。
如果是在Linux环境下，可以直接参考[printer_client](./printer_client/README.md)中的方法使用main.py启动。

```python
CONFIG = {
    "HEADERS": {'content-type': 'application/json'},
    "BASE_URL": "",# 更改为你的打印服务器的实际路径，例如http://admin:admin@127.0.0.1:8080/print-task
    "SUMATRA_PATH": "",  # 更改为SumatraPDF的实际路径，例如D:\SumatraPDF.exe
    "PRINTER_NAME": "" # 更改为你想使用的打印机名称，例如HP LaserJet Professional
}
```

### Handle Script

然后需要将 DOMjudge 和 DOMPrinter 串起来

![alt text](./assets/tutorial_image.png)

你需要在上图所示的这个位置，填入一行命令

```bash
/on_print.sh [file] [original] [language] [username] [teamname] [teamid] [location] 2>&1
```

可以参考这一行命令，`on_print.sh` 的内容在[这里](./cmd/handle_print_cmd/exec.sh)，你需要把这个脚本复制到指定位置，比如按上面的命令，那就需要复制到 `/on_print.sh` 这个位置

友情提醒：不要在这一行命令中填入任何敏感信息，因为这个配置可以被一个公共的 API （`/domjudge/api/v4/config`）拿到，如果有选手（比如 2024 浙江省赛位于 2-B26 的某位选手）对 DOMjudge 特别熟悉，那么这场比赛可能就危险了

错误示范：

```bash
AUTH_USERNAME=domprinter AUTH_PASSWORD=domprinter DOMPRINTER_HOSTNAME=domprinter /on_print.sh [file] [original] [language] [username] [teamname] [teamid] [location] 2>&1
```

不要将 DOMPrinter Server 相关信息通过这种方式传入脚本，不然选手能够通过 DOMjudge API 拿到这些信息，并且可能能够直接连入 DOMPrinter Server 拿到别的队伍的打印代码

## Sponsors

<p align="center">
  <a href="https://github.com/sponsors/Dup4">
    <img src='https://sponsor.dup4.com' alt="Logos from Sponsors" />
  </a>
</p>

## License

[MIT](./LICENSE) License © 2020 - PRESENT [XCPCIO][xcpcio]

[xcpcio]: https://github.com/xcpcio
[license-image-mit]: https://img.shields.io/badge/license-MIT-blue.svg?labelColor=333333
[license-link-mit]: https://mit-license.org/
