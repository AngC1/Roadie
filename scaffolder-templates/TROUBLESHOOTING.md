# Solución de Problemas con Templates de Scaffolder

## Error: "Resource not accessible by integration"

Este error ocurre cuando la GitHub App de Roadie no tiene permisos suficientes para crear repositorios.

### Causa
La GitHub App instalada tiene permisos de **lectura** pero no de **escritura/administración** en repositorios.

### Soluciones

#### Opción 1: Actualizar permisos de GitHub App (Recomendado)

1. Ve a GitHub → [Settings → Applications → Installed GitHub Apps](https://github.com/settings/installations)
2. Busca la app de Roadie/Backstage
3. Haz clic en **Configure**
4. En **Repository permissions**, configura:
   - **Administration**: Read & write ✅
   - **Contents**: Read & write ✅
   - **Metadata**: Read-only ✅
   - **Pull requests**: Read & write ✅
5. Guarda y acepta los nuevos permisos

#### Opción 2: Crear repositorio manualmente

Si no puedes cambiar permisos:

1. **Crea el repositorio en GitHub manualmente**:
   ```bash
   # Usando GitHub CLI
   gh repo create AngC1/nombre-proyecto --public --clone
   
   # O desde la web
   https://github.com/new
   ```

2. **Clona el template localmente**:
   ```bash
   git clone https://github.com/AngC1/Roadie.git
   cd Roadie/scaffolder-templates/skeleton/nodejs-api
   ```

3. **Copia los archivos al nuevo repo**:
   ```bash
   cp -r * /ruta/al/nuevo/repo/
   cd /ruta/al/nuevo/repo/
   git add .
   git commit -m "Initial commit from template"
   git push origin main
   ```

4. **Registra en Roadie**:
   - Ve a https://ayesa.roadie.so/catalog-import
   - Pega la URL: `https://github.com/AngC1/nombre-proyecto/blob/main/catalog-info.yaml`
   - Haz clic en **Analyze** y luego **Import**

#### Opción 3: Usar organización de GitHub

Las GitHub Apps tienen más permisos en organizaciones:

1. Crea una organización en GitHub (si no existe)
2. Instala la GitHub App en la organización
3. Al usar templates, selecciona la organización como owner

### Parámetros añadidos a los templates

Los templates ahora incluyen parámetros explícitos para mejor compatibilidad:

- `repoVisibility: public` - Repositorio público por defecto
- `deleteBranchOnMerge: true` - Limpieza automática de ramas
- `allowRebaseMerge: true` - Permite rebase merge
- `allowSquashMerge: true` - Permite squash merge

### Verificación de permisos

Para verificar los permisos actuales de la GitHub App:

```bash
# Usando GitHub CLI
gh api /installation/repositories

# Usando curl con token
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/installation/repositories
```

### Contacto

Si el problema persiste:
- Contacta al administrador de Roadie en Ayesa
- Solicita revisión de permisos de GitHub App
- Considera usar organizaciones en lugar de cuentas personales

## Referencia

- [GitHub Apps Permissions](https://docs.github.com/en/rest/overview/permissions-required-for-github-apps)
- [Backstage Scaffolder Actions](https://backstage.io/docs/features/software-templates/builtin-actions)
- [Roadie Documentation](https://roadie.io/docs/)
