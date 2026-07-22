#!/usr/bin/env python3
"""CLI for mqgt-neutrinos."""

import argparse
import csv
from pathlib import Path
from mqgt_neutrinos.oscillation_modifications import inverse_mapping
from mqgtapischema.validate_csv import BOUNDS_CSV_SCHEMA


def generate_bounds(delta_p_limit: float, m_c_range: tuple, output_path: str):
    """Generate bounds CSV."""
    m_c_min, m_c_max, n_points = m_c_range
    
    import math
    m_c_values = [10**(math.log10(m_c_min) + i * (math.log10(m_c_max) - math.log10(m_c_min)) / (n_points - 1))
                  for i in range(n_points)]
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=BOUNDS_CSV_SCHEMA["required_columns"])
        writer.writeheader()
        
        for m_c in m_c_values:
            theta_max, kappa_vc_max = inverse_mapping(delta_p_limit, m_c)
            lambda_m = 1.973e-13 / m_c if m_c > 0 else 0
            
            writer.writerow({
                'm_c_GeV': m_c,
                'lambda_m': lambda_m,
                'theta_max': theta_max,
                'kappa_vc_max_GeV': kappa_vc_max,
                'domain_min': m_c_min,
                'domain_max': m_c_max,
                'channel_name': 'neutrinos'
            })
    
    print(f"Generated {len(m_c_values)} bounds, saved to: {output_path}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Generate neutrino constraint bounds')
    parser.add_argument('--delta-p-limit', type=float, default=0.01, help='Oscillation modification limit')
    parser.add_argument('--m-c-min', type=float, default=1e-6, help='Minimum m_c (GeV)')
    parser.add_argument('--m-c-max', type=float, default=1e3, help='Maximum m_c (GeV)')
    parser.add_argument('--n-points', type=int, default=100, help='Number of points')
    parser.add_argument('--output', default='results/neutrino_bounds.csv', help='Output CSV')
    
    args = parser.parse_args()
    
    generate_bounds(
        args.delta_p_limit,
        (args.m_c_min, args.m_c_max, args.n_points),
        args.output
    )


if __name__ == '__main__':
    main()
