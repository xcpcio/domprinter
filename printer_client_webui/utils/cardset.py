from nicegui import ui


def add_rwd_div():
    div_box = ui.element('div').classes('flex row w-full flex-center q-px-none')
    return div_box
    
def current_task_card(cfg: dict):
    with add_rwd_div():
        with ui.card().classes('column q-px-md justify-center w-full'):
             with ui.element('div').classes('w-full'):
                with ui.element('div').classes('row items-center q-mx-none q-gutter-x-md q-my-md'):
                    st_icon = ui.icon('sym_r_error', color='negative').classes('col-1 text-h1')
                    st_spin = ui.spinner('rings').classes('col-1 text-h1').props('color=orange-9')
                    st_wait = ui.spinner('gears').classes('col-1 text-h3').props('color=orange-9')
                    st_spin.set_visibility(False)
                    st_wait.set_visibility(False)
                    with ui.element('div').classes('col q-gutter-y-sm'):
                        with ui.element('div').classes('column q-gutter-y-md'):
                            st_label = ui.label('No status, check backend logs for more details.').classes('row text-h5 text-weight-bolder')
                            with ui.element('div').classes('row'):
                                with ui.element('div').classes('row q-gutter-x-sm'):
                                    # with ui.element('div').classes('col'):
                                    with ui.badge(color='negative').classes('row text-body1 text-weight-bolder') as st_bdg:
                                        st_bdg_icon = ui.icon('info').classes('text-body1 q-mr-sm')
                                        st_bdg_label = ui.label('Backend is not connected.').classes('text-body1')
                                    with ui.badge(color='amber-9'):
                                        ui.icon('sym_r_dns').classes('text-body1 q-mr-sm')
                                        host_ip = ui.label(cfg['service_host']).classes('text-body1')    
                                    # with ui.element('div').classes('col'):
                                    with ui.badge(color='deep-purple-13'):
                                        ui.icon('sym_r_login').classes('text-body1 q-mr-sm')
                                        host_port = ui.label(cfg['service_port']).classes('text-body1')
                                    # with ui.element('div').classes('col'):
                                    with ui.badge(color='deep-orange-13'):
                                        ui.icon('sym_r_account_circle').classes('text-body1 q-mr-sm')
                                        host_auth = ui.label(cfg['auth_name']).classes('text-body1')
                            with ui.element('q-item').classes('row w-full bg-grey-2 col').props('clickable v-ripple'):
                                with ui.element('div').classes('flex col-auto items-center'):
                                    print_icon = ui.icon('sym_r_print_disabled', color="red-6").classes('text-h4')
                                with ui.element('div').classes('col q-gutter-y-sm'):
                                    with ui.element('div').classes('flex row items-center w-full q-gutter-x-md q-px-md'):
                                        ui.label('Task ID: ')
                                        task_name = ui.badge('UNKNOWN', color='yellow-9')
                                    with ui.element('div').classes('flex row items-center w-full q-gutter-x-md q-px-md'):
                                        ui.label('Details: ')
                                        task_details = ui.badge('UNCONNECTED', color='red-9')
    
    return {
        "st_icon": st_icon,
        "st_spin": st_spin,
        "st_wait": st_wait,
        "st_label": st_label,
        "st_bdg": st_bdg,
        "st_bdg_icon": st_bdg_icon,
        "st_bdg_label": st_bdg_label,
        "st_item_icon": print_icon,
        "st_item_name": task_name,
        "st_item_details": task_details
    }
    
def print_monitoring_card():
    with add_rwd_div():
        with ui.card().classes('column q-px-md justify-center w-full'):
            with ui.element('div').classes('w-full'):
                with ui.element('div').classes('row items-center q-mx-none q-gutter-x-md q-my-md'):
                    ui.icon('sym_r_task').classes('text-h4')
                    ui.label('Task history').classes('text-h5 text-weight-bolder')
                with ui.element('div').classes('row w-full items-center'):
                    print_columns = [
                                {'name': 'Print-ID', 'label': 'Print-ID', 'field': 'Print-ID', 'required': True, 'align': 'center'},
                                {'name': 'Print-Team', 'label': 'Print-Team', 'field': 'Print-Team', 'align': 'center'},
                                {'name': 'Print-Location', 'label': 'Print-Location', 'field': 'Print-Location', 'align': 'center'},
                                {'name': 'Print-Time', 'label': 'Print-Time', 'field': 'Print-Time', 'align': 'center'},
                            ]
                    rows = [ ]
                    table = ui.table(columns=print_columns, rows=rows, row_key='name').classes('align-center mx-auto').style('width: 100%; border-collapse: collapse;').props('flat bordered')

    return {
        "table": table
    }
    
