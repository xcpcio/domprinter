from nicegui import ui
from utils.tools import read_config
from utils.layout import add_basic_layout, add_main_content

ui.page_title('Domprinter-CLient')

cfg = read_config(dir="./config.yaml")


@ui.page('/')
def main_page():
    add_basic_layout()
    add_main_content()

    
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Domprinter-Client",
        favicon="./static/favicon.png",
        host=cfg['listen_host'], 
        port=cfg['listen_port'], 
        reload=cfg['auto_reload'],
    )
