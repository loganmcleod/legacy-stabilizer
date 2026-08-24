package fixtures.nplus1;

import java.util.ArrayList;
import java.util.List;

/**
 * TRUE POSITIVE: N+1 query behavior.
 *
 * findLines(orderId) hits the database once per order in the loop. For N orders
 * this issues 1 (findOrders) + N (findLines) queries. A query-count assertion
 * confirms it; reading the loop only makes it a Candidate.
 */
public class TruePositive {

    private final OrderRepository orderRepository;

    public TruePositive(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public List<OrderView> buildViews(String customerId) {
        List<Order> orders = orderRepository.findOrders(customerId); // 1 query
        List<OrderView> views = new ArrayList<>();
        for (Order order : orders) {
            // One query PER order -> N additional round trips.
            List<OrderLine> lines = orderRepository.findLines(order.getId());
            views.add(new OrderView(order, lines));
        }
        return views;
    }
}
