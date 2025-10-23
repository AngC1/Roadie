# Ejemplos Avanzados de Componentes en Roadie.io

Este documento contiene ejemplos avanzados y patrones comunes para desarrollo de plugins en Roadie.io.

## 📋 Tabla de Contenidos

1. [Componente con Estado](#componente-con-estado)
2. [Integración con APIs](#integración-con-apis)
3. [Componente con Catálogo](#componente-con-catálogo)
4. [Dashboard con Gráficos](#dashboard-con-gráficos)
5. [Formulario Interactivo](#formulario-interactivo)
6. [Componente con Backend](#componente-con-backend)

## 🔄 Componente con Estado

```typescript
import React, { useState } from 'react';
import { Button, TextField, Grid } from '@material-ui/core';
import { InfoCard } from '@backstage/core-components';

export const StatefulComponent = () => {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <InfoCard title="Contador">
          <p>Contador: {count}</p>
          <Button 
            variant="contained" 
            color="primary"
            onClick={() => setCount(count + 1)}
          >
            Incrementar
          </Button>
        </InfoCard>
      </Grid>
      
      <Grid item xs={12}>
        <InfoCard title="Saludo Personalizado">
          <TextField
            label="Tu nombre"
            value={name}
            onChange={(e) => setName(e.target.value)}
            fullWidth
          />
          {name && <p>¡Hola, {name}! 👋</p>}
        </InfoCard>
      </Grid>
    </Grid>
  );
};
```

## 🌐 Integración con APIs

```typescript
import React, { useEffect, useState } from 'react';
import { Progress, InfoCard } from '@backstage/core-components';
import { useApi, configApiRef } from '@backstage/core-plugin-api';

interface User {
  name: string;
  email: string;
  company: string;
}

export const ApiIntegrationComponent = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('https://api.example.com/users');
        const data = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <Progress />;
  }

  if (error) {
    return <InfoCard title="Error">Error al cargar datos: {error.message}</InfoCard>;
  }

  return (
    <InfoCard title="Usuarios">
      <ul>
        {users.map((user, index) => (
          <li key={index}>
            {user.name} - {user.email}
          </li>
        ))}
      </ul>
    </InfoCard>
  );
};
```

## 📚 Componente con Catálogo

```typescript
import React from 'react';
import { useEntity } from '@backstage/plugin-catalog-react';
import { InfoCard } from '@backstage/core-components';
import { Grid, Chip } from '@material-ui/core';

export const CatalogComponent = () => {
  const { entity } = useEntity();

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <InfoCard title="Información del Componente">
          <p><strong>Nombre:</strong> {entity.metadata.name}</p>
          <p><strong>Descripción:</strong> {entity.metadata.description}</p>
          <p><strong>Tipo:</strong> {entity.spec?.type}</p>
          <p><strong>Propietario:</strong> {entity.spec?.owner}</p>
        </InfoCard>
      </Grid>
      
      <Grid item xs={12}>
        <InfoCard title="Etiquetas">
          {entity.metadata.tags?.map((tag) => (
            <Chip key={tag} label={tag} style={{ margin: 4 }} />
          ))}
        </InfoCard>
      </Grid>
    </Grid>
  );
};
```

## 📊 Dashboard con Gráficos

```typescript
import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { InfoCard } from '@backstage/core-components';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export const DashboardComponent = () => {
  const data = {
    labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
    datasets: [
      {
        label: 'Despliegues',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Estadísticas Mensuales',
      },
    },
  };

  return (
    <InfoCard title="Dashboard">
      <Bar data={data} options={options} />
    </InfoCard>
  );
};
```

### Dependencias para Gráficos

```bash
yarn add chart.js react-chartjs-2
```

## 📝 Formulario Interactivo

```typescript
import React, { useState } from 'react';
import {
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
} from '@material-ui/core';
import { InfoCard } from '@backstage/core-components';

interface FormData {
  name: string;
  email: string;
  role: string;
}

export const FormComponent = () => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    role: '',
  });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (field: keyof FormData) => (
    event: React.ChangeEvent<{ value: unknown }>
  ) => {
    setFormData({ ...formData, [field]: event.target.value as string });
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    console.log('Datos enviados:', formData);
    setSubmitted(true);
  };

  return (
    <InfoCard title="Formulario de Registro">
      {!submitted ? (
        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                label="Nombre completo"
                value={formData.name}
                onChange={handleChange('name')}
                required
                fullWidth
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                label="Email"
                type="email"
                value={formData.email}
                onChange={handleChange('email')}
                required
                fullWidth
              />
            </Grid>
            
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Rol</InputLabel>
                <Select
                  value={formData.role}
                  onChange={handleChange('role')}
                  required
                >
                  <MenuItem value="developer">Desarrollador</MenuItem>
                  <MenuItem value="designer">Diseñador</MenuItem>
                  <MenuItem value="manager">Manager</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <Button type="submit" variant="contained" color="primary">
                Enviar
              </Button>
            </Grid>
          </Grid>
        </form>
      ) : (
        <div>
          <p>✅ ¡Formulario enviado exitosamente!</p>
          <Button onClick={() => setSubmitted(false)}>
            Enviar otro
          </Button>
        </div>
      )}
    </InfoCard>
  );
};
```

## 🔧 Componente con Backend

### Frontend (ExampleComponent.tsx)

```typescript
import React, { useEffect, useState } from 'react';
import { useApi } from '@backstage/core-plugin-api';
import { myFirstComponentApiRef } from '../../api';
import { InfoCard, Progress } from '@backstage/core-components';

export const BackendComponent = () => {
  const api = useApi(myFirstComponentApiRef);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getData().then(result => {
      setData(result);
      setLoading(false);
    });
  }, [api]);

  if (loading) {
    return <Progress />;
  }

  return (
    <InfoCard title="Datos del Backend">
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </InfoCard>
  );
};
```

### API Definition (api/types.ts)

```typescript
import { createApiRef } from '@backstage/core-plugin-api';

export interface MyFirstComponentApi {
  getData(): Promise<any>;
}

export const myFirstComponentApiRef = createApiRef<MyFirstComponentApi>({
  id: 'plugin.my-first-component.service',
});
```

### API Implementation (api/MyFirstComponentClient.ts)

```typescript
import { MyFirstComponentApi } from './types';
import { DiscoveryApi, FetchApi } from '@backstage/core-plugin-api';

export class MyFirstComponentClient implements MyFirstComponentApi {
  private readonly discoveryApi: DiscoveryApi;
  private readonly fetchApi: FetchApi;

  constructor(options: {
    discoveryApi: DiscoveryApi;
    fetchApi: FetchApi;
  }) {
    this.discoveryApi = options.discoveryApi;
    this.fetchApi = options.fetchApi;
  }

  async getData(): Promise<any> {
    const baseUrl = await this.discoveryApi.getBaseUrl('my-first-component');
    const response = await this.fetchApi.fetch(`${baseUrl}/data`);
    return response.json();
  }
}
```

### Registrar API en plugin.ts

```typescript
import {
  createApiFactory,
  discoveryApiRef,
  fetchApiRef,
} from '@backstage/core-plugin-api';
import { myFirstComponentApiRef } from './api';
import { MyFirstComponentClient } from './api/MyFirstComponentClient';

export const myFirstComponentPlugin = createPlugin({
  id: 'my-first-component',
  routes: {
    root: rootRouteRef,
  },
  apis: [
    createApiFactory({
      api: myFirstComponentApiRef,
      deps: {
        discoveryApi: discoveryApiRef,
        fetchApi: fetchApiRef,
      },
      factory: ({ discoveryApi, fetchApi }) =>
        new MyFirstComponentClient({ discoveryApi, fetchApi }),
    }),
  ],
});
```

## 🎨 Mejores Prácticas

### 1. Manejo de Errores

```typescript
import { ErrorPanel } from '@backstage/core-components';

try {
  // tu código
} catch (error) {
  return <ErrorPanel error={error} />;
}
```

### 2. Loading States

```typescript
import { Progress } from '@backstage/core-components';

if (loading) {
  return <Progress />;
}
```

### 3. Estados Vacíos

```typescript
import { EmptyState } from '@backstage/core-components';

if (items.length === 0) {
  return (
    <EmptyState
      missing="data"
      title="No hay datos"
      description="No se encontraron elementos"
    />
  );
}
```

## 📦 Dependencias Comunes

```json
{
  "dependencies": {
    "@backstage/core-components": "^0.13.0",
    "@backstage/core-plugin-api": "^1.5.0",
    "@backstage/plugin-catalog-react": "^1.7.0",
    "@material-ui/core": "^4.12.4",
    "@material-ui/icons": "^4.11.3",
    "@material-ui/lab": "^4.0.0-alpha.61",
    "react": "^17.0.2",
    "react-router-dom": "^6.3.0",
    "react-use": "^17.4.0"
  }
}
```

## 🚀 Recursos Adicionales

- [Backstage Plugin Development](https://backstage.io/docs/plugins/)
- [Roadie Plugin Catalog](https://roadie.io/backstage/plugins/)
- [Material-UI Documentation](https://v4.mui.com/)
- [React Hooks](https://reactjs.org/docs/hooks-intro.html)

¡Feliz desarrollo! 🎉
