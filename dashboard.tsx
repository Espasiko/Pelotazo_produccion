import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Typography, Progress, Space } from 'antd';
import { ShoppingOutlined, InboxOutlined, ShoppingCartOutlined, UserOutlined } from '@ant-design/icons';
import { odooService, DashboardStats, CategoryData } from './src/services/odooService';

const { Title } = Typography;

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    total_products: 0,
    total_sales: 0,
    total_customers: 0,
    pending_orders: 0,
    low_stock_products: 0,
    monthly_revenue: 0,
    top_selling_product: '',
    topCategories: [],
    recent_sales: [],
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Try to login first with default credentials
        const loginSuccess = await odooService.login('admin', 'admin_password_secure');
        if (loginSuccess) {
          const dashboardStats = await odooService.getDashboardStats();
          setStats(dashboardStats);
        } else {
          throw new Error('Authentication failed');
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Fallback to default data if API fails
        setStats({
          total_products: 248,
          total_sales: 156,
          total_customers: 156,
          pending_orders: 12,
          low_stock_products: 15,
          monthly_revenue: 42500,
          top_selling_product: 'Refrigerador Samsung',
          topCategories: [
            { name: 'Electrodomésticos', percentage: 45 },
            { name: 'Electrónicos', percentage: 30 },
            { name: 'Hogar', percentage: 25 },
          ],
          recent_sales: [
            { id: 1, customer_name: 'María García', product_name: 'Refrigerador', total: 899.99, date: '2024-01-15' },
            { id: 2, customer_name: 'Juan Pérez', product_name: 'Lavadora', total: 599.99, date: '2024-01-14' },
          ],
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div className="dashboard-container">
      <Title level={3} style={{ marginBottom: '24px', color: '#fff' }}>Dashboard</Title>
      
      {/* Tarjetas de estadísticas */}
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Statistic
              title="Total Productos"
              value={stats.total_products}
              valueStyle={{ color: '#1890ff' }}
              prefix={<ShoppingOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Statistic
              title="Productos con Stock Bajo"
              value={stats.low_stock_products}
              valueStyle={{ color: '#ff4d4f' }}
              prefix={<InboxOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Statistic
              title="Ventas del Mes"
              value={stats.monthly_revenue}
              valueStyle={{ color: '#52c41a' }}
              prefix={<ShoppingCartOutlined />}
              suffix="€"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Statistic
              title="Clientes Activos"
              value={stats.total_customers}
              valueStyle={{ color: '#722ed1' }}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* Gráficos y datos adicionales */}
      <Row gutter={[16, 16]} style={{ marginTop: '24px' }}>
        <Col xs={24} lg={12}>
          <Card title="Evolución de Ventas" style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            {/* Aquí iría un gráfico de líneas con Chart.js o similar */}
            <div style={{ height: '200px', background: '#141414', borderRadius: '4px', padding: '16px' }}>
              {/* Placeholder para el gráfico */}
              <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography.Text style={{ color: '#888' }}>Gráfico de evolución de ventas</Typography.Text>
              </div>
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="Productos por Categoría" style={{ background: '#1f1f1f', borderRadius: '8px' }}>
            <Space direction="vertical" style={{ width: '100%' }}>
              {stats.topCategories.map((category: CategoryData, index: number) => (
                <div key={index}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography.Text>{category.name}</Typography.Text>
                    <Typography.Text>{category.percentage}%</Typography.Text>
                  </div>
                  <Progress percent={category.percentage} showInfo={false} strokeColor="#1890ff" />
                </div>
              ))}
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
