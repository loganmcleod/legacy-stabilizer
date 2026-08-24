// TRUE POSITIVE: listeners and an interval registered but never released.
//
// The $rootScope.$on deregistration function and the $interval handle are
// discarded, and nothing runs on $destroy. Each time this controller is
// instantiated (e.g. repeated navigation) another listener and timer leak.
// Confirm with a heap snapshot / listener count across repeated navigation.
angular.module('app').controller('LeakyController', function ($scope, $rootScope, $interval) {
  // Return value (the deregistration fn) is thrown away.
  $rootScope.$on('cart:updated', function (event, cart) {
    $scope.itemCount = cart.items.length;
  });

  // Timer handle is thrown away; $interval keeps firing after the view is gone.
  $interval(function () {
    $scope.lastPolled = Date.now();
  }, 5000);

  // No $scope.$on('$destroy', ...) cleanup.
});
