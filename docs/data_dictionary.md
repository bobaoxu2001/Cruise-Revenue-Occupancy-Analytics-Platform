# Data Dictionary

Core raw entities:
- guests: loyalty, geography, acquisition channel, and age band.
- ships: fleet, class, cabin count, and passenger capacity.
- cabins: ship-level cabin inventory, category, deck, and capacity.
- itineraries: region, ports, duration, and pricing multiplier.
- sailings: ship-itinerary departures and returns.
- reservations: booking lifecycle, passengers, booking value, status, and campaign attribution.
- payments: deposit, final payment, refund, and cancellation penalty events.
- marketing_campaigns: campaign spend and targeting.
- aop_targets: monthly revenue, occupancy, and booking targets.
- onboard_spend: optional service spend for completed reservations.

Governed marts:
- mart_executive_scorecard: month-region-ship class KPIs vs AOP.
- mart_revenue_management: sailing-level occupancy gaps and revenue.
- mart_finance_revenue: recognized, deferred, refund, and penalty measures.
- mart_marketing_performance: campaign contribution and ROAS.
