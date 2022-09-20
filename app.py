from time import sleep
import streamlit as st

from utils import add_bg_from_local

def init(key, val):
    if key not in st.session_state:
        st.session_state[key] = val

def upd(key, val):
    st.session_state[key] = val

def get(key):
    if key not in st.session_state:
        return None
    return st.session_state[key]
    

init('balance', 10000)
init('page', 'main')

# st.text(get('page'))

def send_change():
    upd('page', 'send')

def receive_change():
    upd('page', 'receive')

def send_change_complete(to_send, name = 'Anna John'):
    init('history', [])
    upd('history', [f"You've sent {name} {to_send} Shillings"] + get('history'))
    upd('balance', get('balance')-to_send)
    upd('page', 'main')
    st.experimental_rerun()

def receive_change_complete(to_send, name = 'Anna John'):
    init('history', [])
    upd('history', [f"{name} sent you {to_send} Shillings"] + get('history'))
    upd('balance', get('balance') + to_send)
    upd('page', 'main')
    st.experimental_rerun()

def send_form(name):
    st.warning(f'Sending change to {name}')
    with st.form(f'Sending change to {name}'):
        to_send = st.number_input("Shillings to send", min_value=0, max_value=get('balance'))
        if st.form_submit_button('Send'):
            send_change_complete(to_send=to_send, name=name)
def send_qr_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")
    st.markdown(f"""### You scanned Anna John's QR code""")
    st.markdown(f'## Confirm sending Anna John 200 Shillings?')
    if st.button('Send'):
        send_change_complete(to_send=200)


def send_phone_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")
    st.markdown('# Contacts:')
    with st.expander('Anna John - 0744444444', False):
        send_form('Anna John')
    with st.expander('Mohamed Bakari - 0712345678', False):
        send_form('Mohamed Bakari')
    st.text('Add contact (Coming soon)')
    
    st.markdown('# People near you:')
    with st.expander('Swahib Bodaboda', False):
        send_form('Swahib Bodaboda')
    with st.expander('John Bajaji', False):
        send_form('John Bajaji')



def receive_qr_page():
    st.markdown('# Anna John is sending you 500 Shillings. Confirm?')
    if st.button('Confirm'):
        receive_change_complete(500)
    # add_bg_from_local('qr.png') 

def receive_form(name):
    st.warning(f'Request change from {name}')
    with st.form(f'Receiveing change from {name}'):
        to_receive = st.number_input("Shillings to receive", min_value=0, max_value=get('balance'))
        if st.form_submit_button('Receive'):
            receive_change_wait(name, to_receive)

def receive_change_wait_page():
    name = get('receive_name')
    to_receive = get('receive_change')
    st.markdown(f'# Waiting for {name} to confirm sending you {to_receive} Shillings...')
    sleep(3)
    st.markdown(f'# You received {to_receive} Shillings from {name}')


def receive_phone_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")
    st.markdown('# Contacts:')
    with st.expander('Anna John - 0744444444', False):
        receive_form('Anna John')
    with st.expander('Mohamed Bakari - 0712345678', False):
        receive_form('Mohamed Bakari')
    st.text('Add contact (Coming soon)')
    st.markdown('# Shops near you:')
    with st.expander('Kawe Pharmacy', False):
        receive_form('Kawe Pharmacy')
    with st.expander('Mangi Shop', False):
        receive_form('Mangi Shop')            
    with st.expander('Kahawa Cafe', False):
        receive_form('Kahawa Cafe')


def main_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")

    col1, buf, col2 = st.columns([2,1,2])

    with col1:
        st.button('Send Change', on_click=send_change)

    with col2:
        st.button('Receive Change', on_click=receive_change)
    
    if (h:= get('history')):
        st.markdown('## History')
        for line in h:
            st.warning(line)
def send_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")
    col1, buf, col2, buf, col3 = st.columns([2,1,2,1,2])
    with col1:
        st.button('Send to Phone Number', on_click=send_phone)
        
    with col2:
        st.button('Scan QR Code (Coming Soon)')#', on_click=send_qr)

    with col3:
        st.button('Touch Phones (Coming Soon)')#, on_click=send_touch)

def receive_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")

    col1, buf, col2, buf, col3 = st.columns([2,1,2,1,2])
    
    with col1:
        st.button('Request from Phone Number', on_click=receive_phone)

    with col2:
        st.button('Show QR Code (Coming Soon)')#', on_click=receive_qr)
    
    with col3:
        st.button('Touch Phones (Coming Soon)')#, on_click=receive_touch)



def send_qr():
    upd('page', 'send_qr')
def send_phone():
    upd('page', 'send_phone')
def send_touch():
    upd('page', 'send_touch')
def receive_qr():
    upd('page', 'receive_qr')
def receive_touch():
    upd('page', 'receive_touch')
def receive_phone():
    upd('page', 'receive_phone')
def receive_change_wait(name, to_receive):
    upd('receive_name', name)
    upd('receive_change', to_receive)
    upd('page', 'receive_change_wait')
    st.experimental_rerun()
for page in ['main',
'send',
'receive',
'send_qr',
'send_phone',
'send_touch',
'receive_qr',
'receive_touch',
'receive_phone',
'receive_change_wait',
]:
    if get('page') == page:
        # st.text(f'should run {page}_page')
        locals()[f'{page}_page']()
# if get('page') == 'send':
#     send_change_page()
# if get('page') == 'receive':
#     receive_change_page()




if get('page') != 'main':
    if st.button('Return Home'):
            
        if get('page') == 'receive_change_wait':
            name = get('receive_name')
            to_receive = get('receive_change')
            receive_change_complete(to_receive, name)
        upd('page', 'main')
        st.experimental_rerun()