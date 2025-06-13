import React from 'react';
import { ConfigProvider, Layout, theme } from 'antd';
import { darkTheme } from './darkTheme';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Refine } from '@refinedev/core';
import { RefineKbar, RefineKbarProvider } from '@refinedev/kbar';
import routerBindings, {
  NavigateToResource,
  UnsavedChangesNotifier,
} from '@refinedev/react-router-v6';
import dataProvider from '@refinedev/simple-rest';
import { 
  notificationProvider,
  ThemedLayoutV2,
  ErrorComponent,
} from '@refinedev/antd';

// Importar componentes
import Sider from './sider';
import Header from './header';

// Importar páginas existentes
import Dashboard from './dashboard';
import Products from './products';
import Inventory from './inventory';
import Sales from './sales';
import Customers from './customers';
import Reports from './reports';
import Providers from './providers';

// Importar nuevas páginas CRM
import { Companies, Tasks, Contacts } from './src/pages/crm';

// Importar contexto de Odoo
import { OdooProvider } from './OdooContext';

const { Content } = Layout;

const App: React.FC = () => {
  // URL base para la API FastAPI (backend que se conecta a Odoo)
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  return (
    <Router
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <OdooProvider>
        <ConfigProvider theme={darkTheme}>
          <RefineKbarProvider>
            <Refine
              dataProvider={dataProvider(API_URL)}
              notificationProvider={notificationProvider}
              routerProvider={routerBindings}
              resources={[
                {
                  name: "dashboard",
                  list: "/dashboard",
                  meta: {
                    label: "Dashboard",
                    icon: "DashboardOutlined",
                  },
                },
                {
                  name: "products",
                  list: "/products",
                  meta: {
                    label: "Productos",
                    icon: "ShoppingOutlined",
                  },
                },
                {
                  name: "inventory",
                  list: "/inventory",
                  meta: {
                    label: "Inventario",
                    icon: "InboxOutlined",
                  },
                },
                {
                  name: "sales",
                  list: "/sales",
                  meta: {
                    label: "Ventas",
                    icon: "ShoppingCartOutlined",
                  },
                },
                {
                  name: "customers",
                  list: "/customers",
                  meta: {
                    label: "Clientes",
                    icon: "UserOutlined",
                  },
                },
                {
                  name: "reports",
                  list: "/reports",
                  meta: {
                    label: "Informes",
                    icon: "BarChartOutlined",
                  },
                },
                {
                  name: "providers",
                  list: "/providers",
                  meta: {
                    label: "Proveedores",
                    icon: "TeamOutlined",
                  },
                },
                // Nuevas secciones CRM
                {
                  name: "companies",
                  list: "/crm/companies",
                  create: "/crm/companies/create",
                  edit: "/crm/companies/edit/:id",
                  show: "/crm/companies/show/:id",
                  meta: {
                    label: "Empresas",
                    icon: "ShopOutlined",
                    parent: "crm",
                  },
                },
                {
                  name: "tasks",
                  list: "/crm/tasks",
                  create: "/crm/tasks/create",
                  edit: "/crm/tasks/edit/:id",
                  meta: {
                    label: "Tareas",
                    icon: "ProjectOutlined",
                    parent: "crm",
                  },
                },
                {
                  name: "contacts",
                  list: "/crm/contacts",
                  create: "/crm/contacts/create",
                  edit: "/crm/contacts/edit/:id",
                  show: "/crm/contacts/show/:id",
                  meta: {
                    label: "Contactos",
                    icon: "ContactsOutlined",
                    parent: "crm",
                  },
                },
              ]}
              options={{
                syncWithLocation: true,
                warnWhenUnsavedChanges: true,
                projectId: "odoo-dashboard",
                disableTelemetry: true,
              }}
            >
              <ThemedLayoutV2 
                Header={() => <Header collapsed={false} setCollapsed={() => {}} />}
                Sider={Sider}
                Title={() => <div style={{ fontSize: "20px", fontWeight: "bold", color: "#fff" }}>Electrodomésticos ERP</div>}
              >
                <Routes>
                  <Route
                    index
                    element={<NavigateToResource resource="dashboard" />}
                  />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/products" element={<Products />} />
                  <Route path="/inventory" element={<Inventory />} />
                  <Route path="/sales" element={<Sales />} />
                  <Route path="/customers" element={<Customers />} />
                  <Route path="/reports" element={<Reports />} />
                  <Route path="/providers" element={<Providers />} />
                  
                  {/* Rutas CRM */}
                  <Route path="/crm/companies" element={<Companies />} />
                  <Route path="/crm/companies/create" element={<Companies />} />
                  <Route path="/crm/companies/edit/:id" element={<Companies />} />
                  <Route path="/crm/companies/show/:id" element={<Companies />} />
                  <Route path="/crm/tasks" element={<Tasks />} />
                  <Route path="/crm/tasks/create" element={<Tasks />} />
                  <Route path="/crm/tasks/edit/:id" element={<Tasks />} />
                  <Route path="/crm/contacts" element={<Contacts />} />
                  <Route path="/crm/contacts/create" element={<Contacts />} />
                  <Route path="/crm/contacts/edit/:id" element={<Contacts />} />
                  <Route path="/crm/contacts/show/:id" element={<Contacts />} />
                  
                  <Route path="*" element={<ErrorComponent />} />
                </Routes>
              </ThemedLayoutV2>
              <RefineKbar />
              <UnsavedChangesNotifier />
            </Refine>
          </RefineKbarProvider>
        </ConfigProvider>
      </OdooProvider>
    </Router>
  );
};

export default App;
