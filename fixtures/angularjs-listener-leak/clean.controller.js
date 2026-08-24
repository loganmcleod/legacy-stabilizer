// FALSE POSITIVE: the same listener and interval, correctly released.
//
// The $rootScope.$on deregistration fn and the $interval promise are captured and
// cancelled on $destroy. A naive "$on / $interval present" heuristic would flag
// this; it is correct code and must not be flagged.
angular.module('app').controller('CleanController', function ($scope, $rootScope, $interval) {
  var deregister = $rootScope.$on('cart:updated', function (event, cart) {
    $scope.itemCount = cart.items.length;
  });

  var poll = $interval(function () {
    $scope.lastPolled = Date.now();
  }, 5000);

  $scope.$on('$destroy', function () {
    deregister();          // remove the rootScope listener
    $interval.cancel(poll); // stop the timer
  });
});
