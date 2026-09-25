#!/usr/bin/env python3
"""Metabolic Free client economics.

Answers four questions:
  1. What is one client worth (LTV, gross profit)?
  2. How much can we pay to acquire one (max CAC) and per lead (max CPL)?
  3. How many clients can the coach hold, and what does full capacity earn?
  4. What does this ad budget actually buy?

Edit ASSUMPTIONS (or pass --key value) with real numbers from
docs/00-questions-for-coach.md. Run:  python3 tools/economics.py
"""
import argparse

ASSUMPTIONS = {
    # Revenue
    "price_per_month": 299.0,         # coaching fee (3-month minimum)
    "avg_months_retained": 5.0,       # ESTIMATE: 3 guaranteed by the minimum; replace with real average
    "telehealth_attach_rate": 0.30,   # share of clients who add GLP-1 / hormone care
    "telehealth_margin_per_month": 60.0,  # your net per telehealth client-month
    "referrals_per_client": 0.3,      # new clients each client brings over lifetime
    # Costs per client
    "lumen_device_cost": 199.0,       # what one device costs you
    "lumen_price": 249.0,             # what the client pays for it
    "lumen_attach_rate": 1.0,         # share of clients who buy it (1.0 = part of every enrollment)
    "lumen_sub_per_month": 0.0,       # if you pay the app subscription
    "software_per_client_month": 8.0, # CRM/SMS/etc. allocated
    "payment_fee_pct": 0.03,
    # Funnel
    "lead_to_call": 0.12,
    "show_rate": 0.70,
    "close_rate": 0.30,
    "target_ltv_to_cac": 3.0,
    "ad_budget_per_month": 500.0,
    # Capacity
    "coach_hours_per_week": 25.0,
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
    lumen_net = a["lumen_attach_rate"] * (a["lumen_price"] * (1 - a["payment_fee_pct"]) - a["lumen_device_cost"])
    gp_ltv = gross_month * months + lumen_net
    guaranteed_gp = gross_month * 3 + lumen_net  # the 3-month minimum
    # Referrals are free clients: count their value once (not recursively).
    gp_ltv_with_referrals = gp_ltv * (1 + a["referrals_per_client"])

    max_cac = gp_ltv / a["target_ltv_to_cac"]
    lead_to_client = a["lead_to_call"] * a["show_rate"] * a["close_rate"]
    max_cpl = max_cac * lead_to_client

    minutes_per_client_month = (a["session_minutes"] + a["admin_minutes_per_session"]) \
        * a["sessions_per_client_per_month"]
    capacity = int(a["coach_hours_per_week"] * 60 * 52 / 12 // minutes_per_client_month)
    new_clients_needed = capacity / months  # monthly intake to stay full at steady state

    budget = a["ad_budget_per_month"]
    cpl_target = max_cpl * 0.7  # a healthy account runs below the kill line
    paid_leads = budget / cpl_target
    paid_clients = paid_leads * lead_to_client

    print("\n== ONE CLIENT ==")
    print(f"Revenue / month ................. ${rev_month:,.0f}")
    print(f"Gross profit / month ............ ${gross_month:,.0f}")
    print(f"Lumen net per client ............ ${lumen_net:,.0f}")
    print(f"Guaranteed gross (3-mo minimum) . ${guaranteed_gp:,.0f}")
    print(f"Lifetime gross profit (LTV) ..... ${gp_ltv:,.0f}")
    print(f"LTV incl. referrals ............. ${gp_ltv_with_referrals:,.0f}")

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

    print("\n== THIS BUDGET ==")
    print(f"Ad budget / month ............... ${budget:,.0f}")
    print(f"Leads / month at ${cpl_target:,.2f} CPL ..... {paid_leads:.0f}")
    print(f"Paid clients / month ............ {paid_clients:.1f}")
    print(f"Paid clients / month to fill .... {new_clients_needed:.1f}  (gap is covered by organic, referrals, B2B)")
    print()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k, v in ASSUMPTIONS.items():
        p.add_argument(f"--{k}", type=float, default=v)
    run(vars(p.parse_args()))
