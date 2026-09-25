#!/usr/bin/env python3
"""Metabolic Free client economics.

Answers four questions:
  1. What is one client worth (LTV, gross profit)?
  2. How much can we pay to acquire one (max CAC) and per lead (max CPL)?
  3. How many clients can the coach hold, and what does full capacity earn?
  4. How long until the free Lumen pays for itself?

Edit ASSUMPTIONS (or pass --key value) with real numbers from
docs/00-questions-for-coach.md. Run:  python3 tools/economics.py
"""
import argparse

ASSUMPTIONS = {
    # Revenue
    "price_per_month": 297.0,         # coaching fee
    "avg_months_retained": 7.0,       # average client lifetime
    "telehealth_attach_rate": 0.30,   # share of clients who add GLP-1 / hormone care
    "telehealth_margin_per_month": 60.0,  # your net per telehealth client-month
    "referrals_per_client": 0.3,      # new clients each client brings over lifetime
    # Costs per client
    "lumen_device_cost": 250.0,       # what one device costs you
    "lumen_sub_per_month": 0.0,       # if you pay the app subscription
    "software_per_client_month": 8.0, # CRM/SMS/etc. allocated
    "payment_fee_pct": 0.03,
    # Funnel
    "lead_to_call": 0.12,
    "show_rate": 0.70,
    "close_rate": 0.30,
    "target_ltv_to_cac": 3.0,
    # Capacity
    "coach_hours_per_week": 20.0,
    "session_minutes": 30.0,
    "admin_minutes_per_session": 10.0,  # notes, Lumen review
    "sessions_per_client_per_month": 2.0,
}


def run(a):
    months = a["avg_months_retained"]
    rev_month = a["price_per_month"] + a["telehealth_attach_rate"] * a["telehealth_margin_per_month"]
    cost_month = (a["lumen_sub_per_month"] + a["software_per_client_month"]
                  + a["price_per_month"] * a["payment_fee_pct"])
    gross_month = rev_month - cost_month
    gp_ltv = gross_month * months - a["lumen_device_cost"]
    # Referrals are free clients: count their value once (not recursively).
    gp_ltv_with_referrals = gp_ltv * (1 + a["referrals_per_client"])

    max_cac = gp_ltv / a["target_ltv_to_cac"]
    lead_to_client = a["lead_to_call"] * a["show_rate"] * a["close_rate"]
    max_cpl = max_cac * lead_to_client

    minutes_per_client_month = (a["session_minutes"] + a["admin_minutes_per_session"]) \
        * a["sessions_per_client_per_month"]
    capacity = int(a["coach_hours_per_week"] * 60 * 52 / 12 // minutes_per_client_month)
    new_clients_needed = capacity / months  # monthly intake to stay full at steady state

    lumen_payback_months = a["lumen_device_cost"] / gross_month if gross_month > 0 else float("inf")

    print("\n== ONE CLIENT ==")
    print(f"Revenue / month ................. ${rev_month:,.0f}")
    print(f"Gross profit / month ............ ${gross_month:,.0f}")
    print(f"Lifetime gross profit (LTV) ..... ${gp_ltv:,.0f}  (after Lumen)")
    print(f"LTV incl. referrals ............. ${gp_ltv_with_referrals:,.0f}")
    print(f"Lumen payback ................... {lumen_payback_months:.1f} months"
          f"  -> {'OK' if lumen_payback_months <= 2 else 'REQUIRE COMMITMENT / PAY-IN-FULL'}")

    print("\n== ACQUISITION LIMITS ==")
    print(f"Lead -> client .................. {lead_to_client:.1%}  (1 client per {1/lead_to_client:.0f} leads)")
    print(f"Max CAC at {a['target_ltv_to_cac']:.0f}:1 ................ ${max_cac:,.0f}")
    print(f"Max cost per lead ............... ${max_cpl:,.2f}  <- Ads agent kill line")

    print("\n== COACH CAPACITY ==")
    print(f"Max active clients .............. {capacity}")
    print(f"Monthly revenue at capacity ..... ${capacity * rev_month:,.0f}")
    print(f"Monthly gross profit at capacity  ${capacity * gross_month:,.0f}")
    print(f"New clients / month to stay full  {new_clients_needed:.1f}")
    print(f"Leads / month needed ............ {new_clients_needed / lead_to_client:.0f}")
    print(f"Ad budget / month at max CPL .... ${new_clients_needed / lead_to_client * max_cpl:,.0f}")
    print()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k, v in ASSUMPTIONS.items():
        p.add_argument(f"--{k}", type=float, default=v)
    run(vars(p.parse_args()))
