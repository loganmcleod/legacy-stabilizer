package fixtures.nplus1;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * FALSE POSITIVE: a loop that looks like N+1 but is not.
 *
 * All lines are fetched in ONE query and grouped in memory. The loop iterates an
 * in-memory Map — zero queries inside it. A naive "repository/DAO call near a
 * loop" heuristic would flag this; a query count would show 2 total and clear it.
 */
public class FalsePositive {

    private final OrderRepository orderRepository;

    public FalsePositive(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public List<OrderView> buildViews(String customerId) {
        List<Order> orders = orderRepository.findOrders(customerId);        // 1 query
        List<String> ids = orders.stream().map(Order::getId).collect(Collectors.toList());
        Map<String, List<OrderLine>> linesByOrder =
                orderRepository.findLinesForOrders(ids);                    // 1 query, batched

        List<OrderView> views = new ArrayList<>();
        for (Order order : orders) {
            // In-memory lookup only. No database access in the loop.
            List<OrderLine> lines = linesByOrder.getOrDefault(order.getId(), List.of());
            views.add(new OrderView(order, lines));
        }
        return views;
    }
}
