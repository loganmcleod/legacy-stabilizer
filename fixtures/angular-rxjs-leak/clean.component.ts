// FALSE POSITIVE: the same streams, correctly torn down. Do not flag it.
//
// itemCount$ is rendered through the async pipe (Angular unsubscribes on destroy),
// and the interval subscription is scoped with takeUntilDestroyed, which completes
// when the component is destroyed. A naive ".subscribe present" heuristic would
// flag this; it is correct code.
//
// Context needed to clear it: async pipe on the template stream, takeUntilDestroyed
// on the imperative subscription. Both teardowns are present.
import { Component, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { interval } from 'rxjs';
import { AsyncPipe } from '@angular/common';
import { CartService } from './cart.service';

@Component({
  selector: 'app-cart-badge',
  standalone: true,
  imports: [AsyncPipe],
  template: `<span>{{ count$ | async }}</span>`,
})
export class CartBadgeComponent {
  private cart = inject(CartService);
  count$ = this.cart.itemCount$; // async pipe unsubscribes on destroy

  constructor() {
    interval(5000)
      .pipe(takeUntilDestroyed()) // completes when the component is destroyed
      .subscribe(() => this.cart.refresh());
  }
}
