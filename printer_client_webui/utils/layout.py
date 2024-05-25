from nicegui import ui
from pathlib import Path
from typing import Awaitable, Callable, Optional
from utils.cardset import print_monitoring_card
from utils.cardset import current_task_card
# from utils.cardset import add_cpu_card

def add_head_html() -> None:
    ui.add_head_html((Path(__file__).parent.parent / 'static' / 'header.html').read_text())
    ui.add_head_html(f"<style>{(Path(__file__).parent.parent / 'static' / 'style.css').read_text()}</style>")


def add_header(menu: Optional[ui.left_drawer] = None) -> None:
    menu_items = {
        # 'Installation': '/#installation',
        # 'Features': '/#features',
    }
    with ui.header() \
            .classes('items-center duration-200 p-0 px-4 no-wrap') \
            .style('box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        if menu:
            ui.button(on_click=menu.toggle, icon='menu').props('flat color=white round')

        with ui.element('div').classes('row gap-4 items-center no-wrap mr-auto'):
            with ui.element('div').classes('w-8 stroke-white stroke-2 max-[550px]:hidden'):
                ui.icon('print', color='white').classes('text-3xl')
            ui.label('Domprinter-Client').classes('text-2xl')
        
        with ui.row().classes('max-[1050px]:hidden'):
            for title, target in menu_items.items():
                ui.link(title, target).classes(replace='text-lg text-white')

        with ui.row().classes('min-[1051px]:hidden'):
            with ui.button(icon='more_vert').props('flat color=white round'):
                with ui.menu().classes('bg-primary text-white text-lg'):
                    for title, target in menu_items.items():
                        ui.menu_item(title, on_click=lambda target=target: ui.open(target))
                        

def add_basic_layout() -> None:
    add_head_html()
    add_header()
    ui.add_head_html('<style>html {scroll-behavior: auto;}</style>')



def add_main_content(cfg: dict) -> None:
    widgets = {}
    with ui.element('div').classes('flex column w-full flex-center q-px-none q-gutter-y-md'):
        # widgets.update(api_settings_card())
        widgets.update(current_task_card(cfg))
        widgets.update(print_monitoring_card())
    return widgets


