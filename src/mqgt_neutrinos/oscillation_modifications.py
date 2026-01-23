"""Neutrino oscillation modification constraints."""

import math
from typing import Tuple
from mqgtcoreparams.constants import M_HIGGS_GEV, K_ToE


def forward_mapping(kappa_ch: float, v_c: float, m_c: float) -> float:
    """Forward mapping: ToE parameters → neutrino oscillation modifications."""
    theta_hc = compute_theta_hc(kappa_ch, v_c, m_c)
    # Simplified: oscillation probability modifications
    delta_p = (theta_hc ** 2) / K_ToE * 0.1
    return delta_p


def inverse_mapping(delta_p_max: float, m_c: float) -> Tuple[float, float]:
    """Inverse mapping: oscillation limit → bounds."""
    theta_max = math.sqrt(delta_p_max * K_ToE / 0.1)
    m_h_sq = M_HIGGS_GEV ** 2
    m_c_sq = m_c ** 2
    kappa_vc_max = abs(theta_max * (m_h_sq - m_c_sq))
    return theta_max, kappa_vc_max


def compute_theta_hc(kappa_ch: float, v_c: float, m_c: float, m_h: float = M_HIGGS_GEV) -> float:
    """Compute Higgs-portal mixing angle."""
    if abs(v_c) < 1e-10:
        return 0.0
    denominator = m_h ** 2 - m_c ** 2
    if abs(denominator) < 1e-10:
        raise ValueError(f"Resonance region: m_c ≈ m_h")
    return -kappa_ch * v_c / denominator
