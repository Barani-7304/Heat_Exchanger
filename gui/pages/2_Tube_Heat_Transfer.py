import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.tube import tube_side_heat_transfer

st.title("Tube-Side Heat Transfer Coefficient Calculator")

st.sidebar.header("Tube Parameters")
D_i = st.sidebar.number_input("Tube inner diameter (m)", 0.005, 0.1, 0.01)
D_o = st.sidebar.number_input("Tube outer diameter (m)", 0.006, 0.1, 0.012)
k_tube = st.sidebar.number_input("Tube thermal conductivity (W/m.K)", 10, 400, 50)

# Get tube-side mass flow from Page 1
m_cold = st.session_state.get("m_cold", 1.0)  # default 1.0 if not set

st.write(f"Using tube-side mass flow rate: {m_cold:.2f} kg/s")

if st.button("Calculate Tube-Side Heat Transfer Coefficient"):
    results = tube_side_heat_transfer(m_cold, D_i, D_o, k_tube)
    st.subheader("Results")
    st.write(f"Tube-side fluid velocity: {results['v']:.3f} m/s")
    st.write(f"Reynolds number: {results['Re']:.0f}")
    st.write(f"Nusselt number: {results['Nu']:.2f}")
    st.write(f"Tube-side convective heat transfer coefficient h = {results['h']:.2f} W/m².K")
