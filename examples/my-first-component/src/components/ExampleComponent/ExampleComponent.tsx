import React from 'react';
import { Typography, Grid, Card, CardContent } from '@material-ui/core';
import {
  InfoCard,
  Header,
  Page,
  Content,
} from '@backstage/core-components';

export const ExampleComponent = () => {
  return (
    <Page themeId="tool">
      <Header 
        title="Mi Primer Componente" 
        subtitle="Bienvenido a Roadie.io - Tu primer componente personalizado"
      />
      <Content>
        <Grid container spacing={3} direction="column">
          <Grid item>
            <InfoCard title="¡Bienvenido!">
              <Typography variant="body1" paragraph>
                Este es tu primer componente personalizado en Roadie.io.
                Has completado exitosamente la creación de un plugin básico.
              </Typography>
              <Typography variant="body2">
                Puedes personalizar este contenido según tus necesidades,
                agregar más funcionalidades, conectar con APIs externas,
                y mucho más.
              </Typography>
            </InfoCard>
          </Grid>
          
          <Grid item>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      🎨 Personalización
                    </Typography>
                    <Typography variant="body2">
                      Puedes personalizar los estilos, colores y diseño
                      utilizando Material-UI y los temas de Backstage.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      🔌 Integración
                    </Typography>
                    <Typography variant="body2">
                      Conecta tu componente con APIs, bases de datos,
                      servicios externos y otros plugins de Backstage.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      📊 Datos
                    </Typography>
                    <Typography variant="body2">
                      Muestra datos dinámicos, gráficos, tablas y
                      visualizaciones usando las bibliotecas disponibles.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      🚀 Próximos Pasos
                    </Typography>
                    <Typography variant="body2">
                      Explora la documentación de Backstage y Roadie.io
                      para agregar más funcionalidades a tu componente.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
};
