// TRUE POSITIVE: Module Federation singleton version skew.
//
// The host declares react as a singleton pinned to ^18.2.0, while the remote
// (below) requires ^19.0.0 as a singleton. At runtime one copy wins; the loser's
// components run against the wrong React, producing "invalid hook call" / "two
// copies of React" errors. Confirm with the RESOLVED shared config across host +
// remote and the version actually loaded — a single package.json is not enough.
const { ModuleFederationPlugin } = require('webpack').container;

// ---- host: shell ----
module.exports.host = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'shell',
      remotes: { ordersUi: 'ordersUi@https://cdn.example.com/orders/remoteEntry.js' },
      shared: {
        react: { singleton: true, requiredVersion: '^18.2.0' },
        'react-dom': { singleton: true, requiredVersion: '^18.2.0' },
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
        // Incompatible major with the host's singleton range.
        react: { singleton: true, requiredVersion: '^19.0.0' },
        'react-dom': { singleton: true, requiredVersion: '^19.0.0' },
      },
    }),
  ],
};
