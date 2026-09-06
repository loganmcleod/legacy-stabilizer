// TRUE POSITIVE: RxJS subscription with no teardown in an Angular 17 component.
//
// The .subscribe() return value is discarded: no takeUntilDestroyed, no
// takeUntil(destroy$), no async pipe. The stream is an interval, so it keeps
// emitting after the component is destroyed, and each navigation to this route
// leaks another live subscription. This is the modern analogue of the AngularJS
// $destroy leak.
//
// This is a LEAD, not a confirmed defect. Confirm with a heap snapshot or a
// retained-subscription count across repeated navigation — not the code alone.
import { Component } from '@angular/core';
import { interval } from 'rxjs';
import { CartService } from './cart.service';

@Component({
  selector: 'app-cart-badge',
  standalone: true,
  template: `<span>{{ count }}</span>`,
})
export class CartBadgeComponent {
  count = 0;

  constructor(private cart: CartService) {
    // Return value (Subscription) is thrown away; nothing unsubscribes.
    this.cart.itemCount$.subscribe((n) => (this.count = n));

    // Long-lived timer with no teardown — keeps firing after destroy.
    interval(5000).subscribe(() => this.cart.refresh());
  }
}
