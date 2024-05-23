from nicegui import ui


def add_rwd_div():
    div_box = ui.element('div').classes('flex row w-full flex-center q-px-none')
    return div_box

def api_settings_card():
    
    def handle_click():
        localhost_value = localhost.value
        port_value = port.value
        username_value = username.value
        password_value = password.value

        if not localhost_value or not port_value or not username_value or not password_value:
            ui.notify('Please fill in all fields.', color='negative', position='top')
        else:
            ui.notify('Data sent successfully!', color='positive', position='top')
    
    card = ui.card().classes('column q-px-md justify-center w-full')
    with add_rwd_div():
        with card:
            with ui.element('div').classes('w-full'):
                with ui.element('div').classes('row items-center q-mx-none q-gutter-x-md q-my-md'):
                    ui.icon('model_training').classes('text-h4')
                    ui.label('API Settings').classes('text-h5 text-weight-bolder')
            with ui.element('div').classes('row w-full items-center q-gutter-x-md q-px-md justify-center'):
                localhost = ui.input(label='localhost').classes('row text-h6 q-px-md input-lg')
                port = ui.input(label='port').classes('row text-h6 input-lg')
                username = ui.input(label='username').classes('row text-h6 input-lg')
                password = ui.input(label='password').classes('row text-h6 input-lg')
                change_button = ui.button('Change', color='amber-10').classes('col-1 q-ml-lg')
                change_button.on('click', handle_click)
                
    return {
        "print_localhost": localhost,
        "print_host": port,
        "print_username": username,
        "print_password": password
    }

def print_monitoring_card():
    card = ui.card().classes('column q-px-md justify-center w-full')
    with add_rwd_div():
        with card:
            with ui.element('div').classes('w-full'):
                with ui.element('div').classes('row items-center q-mx-none q-gutter-x-md q-my-md'):
                    ui.icon('model_training').classes('text-h4')
                    ui.label('Print Monitoring').classes('text-h5 text-weight-bolder')
            with ui.element('div').classes('row w-full items-center q-gutter-x-md q-px-md'):
                print_columns = [
                            {'name': 'Print-ID', 'label': 'Print-ID', 'field': 'Print-ID', 'required': True, 'align': 'center'},
                            {'name': 'Print-Team', 'label': 'Print-Team', 'field': 'Print-Team', 'align': 'center'},
                            {'name': 'Print-Location', 'label': 'Print-Location', 'field': 'Print-Location', 'align': 'center'},
                            {'name': 'Print-Time', 'label': 'Print-time', 'field': 'Print-Time', 'align': 'center'},
                        ]
                rows = [ ]
                table = ui.table(columns=print_columns, rows=rows, row_key='name').classes('align-center mx-auto')
                table.style('width: 100%; border-collapse: collapse;')

    return {
        "rows": rows
    }
    
