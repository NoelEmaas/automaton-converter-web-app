import streamlit as st 
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode, ColumnsAutoSizeMode
import pandas as pd


st.set_page_config(layout="wide")

# Session variables
st.session_state.setdefault('show_generated_table', False)
st.session_state.setdefault('input_symbols', '')
st.session_state.setdefault('states', '')
st.session_state.setdefault('start_state', '')
st.session_state.setdefault('final_states', '')
st.session_state.setdefault('show_table', False)
st.session_state.setdefault('table_data', pd.DataFrame())

expand_output_section = False

st.markdown(
    f"""
    <style>
        .appview-container {{
            margin: auto;
            max-width: 1200px;
            padding-top: 0;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }}
        .element-container:has(.full-btn) + div button {{
            width: 100%;
        }}
        element-container:has(.blue-btn) + div button {{
            background-color: #4B64FF;
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title('Automaton Converter')
st.write('Convert εNFA to NFA or NFA to DFA seamlessly with this user-friendly automaton converter app.')

st.markdown(
    """
    <div style="margin-top: -20px; margin-bottom: 0px;">
        <hr>
    </div>
    """,
    unsafe_allow_html = True
)


def generate_transition_table(input_symbols, states, start_state, final_states):
    input_symbols = input_symbols.split()
    states = states.split()

    table_data = []

    for state in states:
        if state == start_state:
            row = {' ': '*  ' + state}
        if state in final_states:
            row = {' ': '-> ' + state}
        if state != start_state and state not in final_states:
            row = {' ': '   ' + state}
        for symbol in input_symbols:
            row[symbol] = ' '
        table_data.append(row)

    columns = [' '] + input_symbols
    df = pd.DataFrame(columns = columns, data = table_data)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=False)
    gb.configure_default_column(editable=True, sorteable=False)
    gb.configure_column(" ", editable=False, cellStyle={"textAlign": "center", "BackgroundColor": "grey"})
    gb.configure_auto_height(True)
    grid_options = gb.build()

    grid_data = AgGrid(
        df,
        gridOptions = grid_options,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
        fit_columns_on_grid_load=True,
        width = '100%',
    )

    st.write(grid_data['data'])


def validate_input(input_symbols, states, start_state):
    if input_symbols == '':
        st.error("Input symbols cannot be empty.")
        return False
    if states == '':
        st.error("States cannot be empty.")
        return False
    if start_state == '':
        st.error("Start state cannot be empty.")
        return False
    return True


with st.expander("Automaton Data", expanded = True):
    input_symbols = st.text_input(label = "Enter Input Symbols (Separated by Spaces, copy ε for epsilon input):", placeholder = "e.g. a b c d ε")
    states = st.text_input(label = "Enter States (Separated by Spaces):", placeholder = "e.g. q1 q2 q3 q4")
    start_state = st.selectbox(
        label = 'Select Start State',
        options = states.split(),
    )
    final_states = st.multiselect(
        label = "Select Final States",
        options = states.split(),
    )

    st.markdown('<span class="full-btn .blue-btn"></span>', unsafe_allow_html=True)
    if st.button(label = "Generate Table") and validate_input(input_symbols, states, start_state):
        st.session_state.show_generated_table = True
        st.session_state.input_symbols = input_symbols
        st.session_state.states = states
        st.session_state.start_state = start_state
        st.session_state.final_states = final_states
    
    if st.session_state.show_generated_table:
        generate_transition_table(
            st.session_state.input_symbols, 
            st.session_state.states, 
            st.session_state.start_state, 
            st.session_state.final_states
        )

st.markdown('<span class="full-btn"></span>', unsafe_allow_html=True)
if st.button(label = "Convert to NFA"):
    expand_output_section = True

with st.expander("Transition Table Output", expanded = expand_output_section):
    st.write("Output here")