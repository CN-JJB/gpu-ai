# Expected — Experiment 65

There is no universal real numeric result.

With unmodified Experiment 63 CSV:
- client/system occupancy can be derived;
- service-start/active occupancy cannot;
- active KV must remain UNKNOWN.

With trustworthy service-start timestamps:
- verify L_system = L_active + L_queue within trace arithmetic;
- report mean and peak separately.

Do not choose slots solely from ceil(L_system) or ceil(L_active).
