// FALSE POSITIVE: two remotes that share React, but on compatible ranges.
//
// Host and remote both declare react/react-dom as singletons on the SAME major
// range (^19.0.0). One copy is shared cleanly — this is exactly how a singleton
// is meant to work. A naive "two ModuleFederation configs both list react as a
// singleton" heuristic would flag this; it is correct and must not be flagged.
const { ModuleFederationPlugin } = require('webpack').container;

// ---- host: shell ----
module.exports.host = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'shell',
      remotes: { ordersUi: 'ordersUi@https://cdn.example.com/orders/remoteEntry.js' },
      shared: {
        react: { singleton: true, requiredVersion: '^19.0.0' },
        'react-dom': { singleton: true, requiredVersion: '^19.0.0' },
      },
    }),
  ],
};

// ---- remote: orders-ui ----
module.exports.remote = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'ordersUi',
      exposes: { './OrdersPage': './src/OrdersPage' },
      shared: {
        react: { singleton: true, requiredVersion: '^19.0.0' },
        'react-dom': { singleton: true, requiredVersion: '^19.0.0' },
      },
    }),
  ],
};
