

def tube_side_calculation(m_cold, D_i, D_o, k_tube, rho=1000, mu=0.83e-3, Cp=4180, k=0.6, n_tubes=52):
    """
    Calculate tube-side fluid velocity, Reynolds number, Nusselt number,
    and convective heat transfer coefficient.
    
    m_cold: mass flow through all tubes (kg/s)
    n_tubes: number of tubes
    """
    # Mass flow per tube
    m_per_tube = m_cold / n_tubes

    # Tube cross-sectional area
    A = 3.14159 * (D_i / 2)**2

    # Fluid velocity
    v = m_per_tube / (rho * A)

    # Reynolds number
    Re = m_per_tube * D_i / (mu * A)

    # Prandtl number
    Pr = Cp * mu / k

    # Nusselt number (Dittus-Boelter)
    Nu = 0.023 * Re**0.8 * Pr**0.4

    # Heat transfer coefficient
    h = Nu * k / D_i

    return {"v": v, "Re": Re, "Nu": Nu, "h": h}
