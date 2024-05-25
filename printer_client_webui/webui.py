from nicegui import ui
from multiprocessing import Queue
from utils.tools import read_config
from utils.layout import add_basic_layout, add_main_content

from handler import TaskProcessor

ui.page_title('Domprinter-CLient')

cfg = read_config(dir="./config.yaml")

task_queue = None


task_done_list = list()
widget_list = None
handler_init_status = False

def update_label():
    global handler_init_status
    while not task_queue.empty():
        task = task_queue.get()
        if task[0] == 'INIT':
            handler_init_status = True
            return
        elif task[0] == 'NEW':
            refresh_status(task[1]["PrintTaskID"], str(task[1]["TeamID"]) + str(task[1]["Location"] + str(task[1]["SubmitTime"])))
        elif task[0] == 'DONE':
            task_done_list.append({
                "Print-ID": task[1]["PrintTaskID"],
                "Print-Team": task[1]["TeamID"],
                "Print-Location": task[1]["Location"],
                "Print-Time": task[1]["SubmitTime"]
            })
            init_status()
    if widget_list is not None:
        widget_list["table"].update_rows(task_done_list)
    if handler_init_status is True:
        init_status()

def init_status():
    global widget_list
    if not task_handler.is_alive():
        return
    # widget_list['st_icon'].name='sym_r_check_circle_outline'
    # widget_list['st_icon'].props('color=positive')
    widget_list['st_icon'].set_visibility(False)
    widget_list['st_wait'].set_visibility(True)
    widget_list['st_spin'].set_visibility(False)
    widget_list['st_label'].text='Waiting for tasks...'
    widget_list['st_bdg'].props('color=positive')
    widget_list['st_bdg_icon'].name='sym_r_autorenew'
    widget_list['st_bdg_label'].text='No tasks'
    widget_list['st_item_icon'].name='sym_r_print'
    widget_list['st_item_icon'].props('color=teal-14')
    widget_list['st_item_name'].text='No tasks'
    widget_list['st_item_details'].text='No processing task'
    widget_list["table"].update_rows(task_done_list)

def refresh_status(task_id: int = 0, task_details: str = 'test'):
    global widget_list
    widget_list['st_icon'].set_visibility(False)
    widget_list['st_spin'].set_visibility(True)
    widget_list['st_wait'].set_visibility(False)
    widget_list['st_label'].text='Processing tasks...'
    widget_list['st_bdg'].props('color=positive')
    widget_list['st_bdg_icon'].name='directions_run'
    widget_list['st_bdg_label'].text='Run printing...'
    widget_list['st_item_icon'].name='sym_r_print'
    widget_list['st_item_icon'].props('color=blue-14')
    widget_list['st_item_name'].text=str(task_id)
    widget_list['st_item_name'].props('color=teal-14')
    widget_list['st_item_details'].text=str(task_details)
    widget_list['st_item_details'].props('color=indigo-14')
    widget_list["table"].update_rows(task_done_list)

@ui.page('/')
def main_page():
    global widget_list
    add_basic_layout()
    widget_list = add_main_content(cfg)
    
    
if __name__ in {"__main__", "__mp_main__"}:
    if __name__ == "__main__":
        task_queue = Queue()
        task_handler = TaskProcessor(task_queue, cfg)
        task_handler.start()
    ui.timer(interval=1, callback=update_label)
    ui.run(
        title="Domprinter-Client",
        favicon="./static/favicon.png",
        host=cfg['listen_host'], 
        port=cfg['listen_port'], 
        reload=cfg['auto_reload'],
    )
    
    
