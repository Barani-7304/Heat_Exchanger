
import CoolProp.CoolProp as CP

class Fluid:
    """
    Represents a working fluid with thermophysical properties.
    Uses CoolProp for property evaluation.
    """

    def __init__(self, name, T, P, m_dot=None, v=None):
        """
        Parameters:
        -----------
        name : str
            Fluid name (as recognized by CoolProp, e.g., 'Water', 'Air')
        T : float
            Temperature [K]
        P : float
            Pressure [Pa]
        m_dot : float, optional
            Mass flow rate [kg/s]
        v : float, optional
            Velocity [m/s]
        """
        self.name = name
        self.T = T
        self.P = P
        self.m_dot = m_dot
        self.v = v

    def get_props(self):
        """Return a dictionary of fluid properties at T, P."""
        rho = CP.PropsSI("D", "T", self.T, "P", self.P, self.name)      # density [kg/m³]
        cp = CP.PropsSI("C", "T", self.T, "P", self.P, self.name)       # specific heat [J/kg-K]
        mu = CP.PropsSI("V", "T", self.T, "P", self.P, self.name)       # dynamic viscosity [Pa·s]
        k = CP.PropsSI("L", "T", self.T, "P", self.P, self.name)        # thermal conductivity [W/m-K]
        Pr = CP.PropsSI("Prandtl", "T", self.T, "P", self.P, self.name) # Prandtl number

        return {
            "rho": rho,
            "cp": cp,
            "mu": mu,
            "k": k,
            "Pr": Pr
        }

    def __repr__(self):
        return f"<Fluid {self.name} at {self.T} K, {self.P/1e5:.2f} bar>"
