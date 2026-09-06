// FALSE POSITIVE: imports that look cross-boundary but are allowed. Do not flag it.
//
// Same feature lib (tags: type:feature, scope:checkout). Both imports satisfy the
// tag rules:
//   - it imports a type:data-access lib within scope:checkout, through its PUBLIC
//     barrel (index.ts), and
//   - it imports a scope:shared util, which every scope may depend on.
// A naive "reaches into another lib" heuristic would flag this; it is legal per the
// depConstraints.
//
// Context needed to clear it: the imports resolve to public barrels and the target
// tags are permitted by the source tag's onlyDependOnLibsWithTags. Confirm with
// nx lint (no error) rather than by eye.

// Public barrel of a data-access lib in the same scope — allowed:
import { CartRepository } from '@shop/checkout/data-access';
// Shared util lib — allowed from any scope:
import { formatMoney } from '@shop/shared/util-format';

export class CartCheckoutService {
  constructor(private carts: CartRepository) {}

  total(): string {
    return formatMoney(this.carts.currentTotal());
  }
}
