// TRUE POSITIVE: an import that crosses NX enforce-module-boundaries tags.
//
// This file lives in libs/checkout/feature-cart (tags: type:feature, scope:checkout).
// It reaches into another scope's INTERNAL path AND up into the app layer:
//   - deep import bypasses libs/billing's public index.ts barrel, and
//   - scope:checkout imports scope:billing, which the tag rules forbid.
// Both are exactly what @nx/enforce-module-boundaries is meant to catch.
//
// This is a LEAD, not a confirmed defect. Corroborate with the lint rule output
// (nx lint) or the dep graph (nx graph) — not by eye. The real tag rules live in
// eslint config / project.json, which this fixture only summarizes below.

// Deep import into another lib, past its barrel:
import { InvoiceCalculator } from '../../billing/data-access/src/lib/invoice-calculator';
// Import up into the application layer from a feature lib:
import { AppShellStore } from '../../../apps/shop/src/app/app-shell.store';

export class CartCheckoutService {
  constructor(
    private invoices: InvoiceCalculator, // scope:billing internal — forbidden
    private shell: AppShellStore,         // type:app from a type:feature — forbidden
  ) {}
}

/*
Assumed tag config (for the assessor to verify against the real workspace):

  // libs/checkout/feature-cart/project.json  -> tags: ["type:feature","scope:checkout"]
  // libs/billing/data-access/project.json     -> tags: ["type:data-access","scope:billing"]
  // apps/shop/project.json                    -> tags: ["type:app","scope:shop"]

  // .eslintrc depConstraints (excerpt):
  //   { sourceTag: "scope:checkout", onlyDependOnLibsWithTags: ["scope:checkout","scope:shared"] }
  //   { sourceTag: "type:feature",   onlyDependOnLibsWithTags: ["type:data-access","type:ui","type:util"] }
*/
