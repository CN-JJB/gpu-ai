# Dynamic Intelligence — PSU / PCIe Power / Connectors — 2026-08-27

Dynamic/current information; installed PSU/GPU manuals remain authoritative.

## Intel public ATX design guidance

Current public Intel design guide pages expose ATX12V 3.1 guidance and dedicated topics for:
- PCIe add-in-card power excursions;
- PCIe add-in-card and PSU power budgets;
- PSU power excursion;
- PCIe auxiliary power connectors;
- 12V-2x6 sideband signals;
- PSU output protections.

Official:
https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/atx-version-3-0-multi-rail-desktop-platform-power-supply-design-guide/

Do not use this dated summary as a replacement for the exact PSU design/model documentation.

## PCI-SIG 12V-2x6

Published PCI-SIG ECN dated 2023-08-31 states:
- 12V-2x6 is defined in CEM 5.1;
- it replaces 12VHPWR;
- the ECN updates connector type encoding and power measurement consistency.

Official:
https://pcisig.com/PCI%20Express/ECN/Base/12V-2x6ConnectorUpdatestoPCIeBase_6.0

Avoid reducing connector identity to a single universal wattage claim.

## Modular cable compatibility

### Seasonic
Current official knowledge base says modular DC cables are often not compatible across PSU brands and can differ between series/models, and directs users to exact compatibility information.

Official:
https://knowledge.seasonic.com/article/68-cable-compatibility

Current Seasonic quick-start guidance also says to use appropriate Seasonic-provided/compatible cables.

### Corsair
Current official guidance says PSU-side modular cable pinouts are not universal and exact cable family compatibility must be checked.

Official:
https://www.corsair.com/eu/en/explorer/diy-builder/power-supply-units/are-psu-cables-universal/
https://www.corsair.com/ww/en/s/psu-cable-compatibility

## Dynamic rule

When the exact PSU/GPU model is known:

```text
manufacturer manual / compatibility table
>
generic course rule
```

Record exact URL/document revision in the Evidence packet.
