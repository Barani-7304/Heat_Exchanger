# core/geometry.py
import numpy as np

def heat_exchanger_balance(m_hot, cp_hot, Th_in=None, Th_out=None,
                           m_cold=None, cp_cold=None, Tc_in=None, Tc_out=None):
    """
    Solve basic heat exchanger energy balance.
    Any one of the four temperatures can be unknown (None).
    Returns: q (heat transfer), all four temperatures.
    """
    temps = {"Th_in": Th_in, "Th_out": Th_out, "Tc_in": Tc_in, "Tc_out": Tc_out}
    unknowns = [k for k, v in temps.items() if v is None]

    if len(unknowns) == 0:
        # All temperatures known, just calculate q
        q_hot = m_hot * cp_hot * (Th_in - Th_out)
        q_cold = m_cold * cp_cold * (Tc_out - Tc_in)
        q = (q_hot + q_cold) / 2.0
    elif len(unknowns) == 1:
        # Only one unknown temperature
        unknown = unknowns[0]
        if unknown in ["Th_in", "Th_out"]:
            # Hot side unknown
            if Th_in is None:
                q = m_cold * cp_cold * (Tc_out - Tc_in)
                Th_in = Th_out + q / (m_hot * cp_hot)
            else:  # Th_out is None
                q = m_cold * cp_cold * (Tc_out - Tc_in)
                Th_out = int(Th_in - q / (m_hot * cp_hot))
        else:
            # Cold side unknown
            if Tc_in is None:
                q = m_hot * cp_hot * (Th_in - Th_out)
                Tc_in = Tc_out - q / (m_cold * cp_cold)
            else:  # Tc_out is None
                q = m_hot * cp_hot * (Th_in - Th_out)
                Tc_out = int(Tc_in + q / (m_cold * cp_cold))
    else:
        raise ValueError("Too many unknowns: only one temperature can be missing.")

    return {
        "q": q,
        "Th_in": Th_in, "Th_out": Th_out,
        "Tc_in": Tc_in, "Tc_out": Tc_out
    }


def log_mean_temp_difference(Th_in, Th_out, Tc_in, Tc_out):
    """Calculate log mean temperature difference (LMTD)."""
    dT1 = Th_in - Tc_out
    dT2 = Th_out - Tc_in
    if dT1 == dT2:  # avoid log(1)=0
        return dT1
    else:
        return int((dT1 - dT2) / (np.log(dT1 / dT2)))
