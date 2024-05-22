from nicegui import ui


def add_rwd_div():
    div_box = ui.element('div').classes('flex row w-full flex-center q-px-none')
    return div_box

def api_settings_card():
    card = ui.card().classes('column q-px-md justify-center w-full')
    with add_rwd_div():
        with card:
            with ui.element('div').classes('w-full'):
                with ui.element('div').classes('row items-center q-mx-none q-gutter-x-md q-my-md'):
                    ui.icon('model_training').classes('text-h4')
                    ui.label('API Settings').classes('text-h5 text-weight-bolder')
            with ui.element('div').classes('row w-full items-center q-gutter-x-md q-px-md'):
                pass
            
    return {
        
    }
    
