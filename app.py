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

def send_money():
    upd('page', 'send')

def receive_money():
    upd('page', 'receive')

def send_money_complete(to_send, name = 'Bogdan'):
    init('history', [])
    upd('history', [f"You've sent {name} {to_send} Shillings"] + get('history'))
    upd('balance', get('balance')-to_send)
    upd('page', 'main')
    st.experimental_rerun()

def receive_money_complete(to_send, name = 'Bogdan'):
    init('history', [])
    upd('history', [f"{name} sent you {to_send} Shillings"] + get('history'))
    upd('balance', get('balance') + to_send)
    upd('page', 'main')
    st.experimental_rerun()

def send_form(name):
    st.warning(f'Sending money to {name}')
    with st.form(f'Sending money to {name}'):
        to_send = st.number_input("Shillings to send", min_value=0, max_value=get('balance'))
        if st.form_submit_button('Send'):
            send_money_complete(to_send=to_send, name=name)
def send_qr_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")
    st.markdown(f"""### You scanned Bogdan's QR code""")
    st.markdown(f'## Confirm sending Bogdan 200 Shillings?')
    if st.button('Send'):
        send_money_complete(to_send=200)


def send_phone_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")
    with st.expander('Bogdan - 0744444444', False):
        send_form('Bogdan')
    with st.expander('Mwombeki - 0712345678', False):
        send_form('Mwombeki')
    st.text('Add contact (Comming soon)')

def receive_qr_page():
    st.markdown('# Bogdan is sending you 500 Shillings. Confirm?')
    if st.button('Confirm'):
        receive_money_complete(500)
    # add_bg_from_local('qr.png') 

def main_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")

    col1, buf, col2 = st.columns([2,1,2])

    with col1:
        st.button('Send Money', on_click=send_money)

    with col2:
        st.button('Receive Money', on_click=receive_money)
    
    if (h:= get('history')):
        st.markdown('## History')
        for line in h:
            st.warning(line)
def send_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")
    col1, buf, col2, buf, col3 = st.columns([2,1,2,1,2])
    with col1:
        st.button('Scan QR Code', on_click=send_qr)

    with col2:
        st.button('Send to Phone Number', on_click=send_phone)

    with col3:
        st.button('Touch Phones (Comming Soon)')#, on_click=send_touch)

def receive_page():
    st.markdown(f"""# Balance: {st.session_state.balance}""")

    col1, buf, col2 = st.columns([2,1,2])

    with col1:
        st.button('Show QR Code', on_click=receive_qr)

    with col2:
        st.button('Touch Phones (Comming Soon)')#, on_click=receive_touch)



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

for page in ['main',
'send',
'receive',
'send_qr',
'send_phone',
'send_touch',
'receive_qr',
'receive_touch',
]:
    if get('page') == page:
        # st.text(f'should run {page}_page')
        locals()[f'{page}_page']()
# if get('page') == 'send':
#     send_money_page()
# if get('page') == 'receive':
#     receive_money_page()





if st.button('Return Home'):
    upd('page', 'main')
    st.experimental_rerun()