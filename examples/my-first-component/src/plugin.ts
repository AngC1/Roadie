import { createPlugin, createRoutableExtension } from '@backstage/core-plugin-api';

import { rootRouteRef } from './routes';

export const myFirstComponentPlugin = createPlugin({
  id: 'my-first-component',
  routes: {
    root: rootRouteRef,
  },
});

export const MyFirstComponentPage = myFirstComponentPlugin.provide(
  createRoutableExtension({
    name: 'MyFirstComponentPage',
    component: () =>
      import('./components/ExampleComponent').then(m => m.ExampleComponent),
    mountPoint: rootRouteRef,
  }),
);
