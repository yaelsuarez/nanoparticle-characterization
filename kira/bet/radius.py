import sys
import argparse

def BET_radius(surface:float, surface_err:float, density:float):
    """
    Estimate the radius of a nanoparticle based on the measurement of
    BET specific surface area analysis, assuming a spherical morphology
    of the nanoparticle.
    :param density: Density of the material (g/cm³).
    :param surface: BET specific surface area (m²/g).
    :param surface_err: ± Error in measurement of surface (m²/g).
    :return radius: Estimated radius (nm)
    """
    def bet_formula(surface, density):
        return 3 / (density * surface * 1e-3)

    surface_low = surface - surface_err
    surface_high = surface + surface_err
    radius_low = bet_formula(surface_low, density)
    radius_high = bet_formula(surface_high, density)
    radius = (radius_high + radius_low) / 2.0
    radius_err = abs(radius_high - radius)
    return radius, radius_err

def cli_bet_radius(raw_args=sys.argv[1:]):
    """
    CLI to quickly get the estimation in the terminal.
    """
    parser=argparse.ArgumentParser()
    parser.add_argument("surface", 
        help="BET specific surface area (m²/g)", type=float)
    parser.add_argument("surface_err", 
        help="± Error in measurement of surface (m²/g)", type=float)
    parser.add_argument("density",
        help="Density of the material (g/cm³)", type=float)
    args=parser.parse_args(raw_args)
    radius, r_err = BET_radius(
        surface=args.surface,
        surface_err=args.surface_err,
        density=args.density
    )
    diameter = 2.0 * radius
    d_err = 2.0 * r_err
    print(f"radius = {radius:.2f} ± {r_err:.2f} nm")
    print(f"diameter = {diameter:.2f} ± {d_err:.2f} nm")