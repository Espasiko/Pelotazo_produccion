import React from 'react';
import {
  List,
  useTable,
  EditButton,
  DeleteButton,
  CreateButton,
  FilterDropdown,
} from '@refinedev/antd';
import {
  Card,
  Table,
  Space,
  Input,
  Select,
  Tag,
  Typography,
  Avatar,
  Tooltip,
  Button,
} from 'antd';
import {
  SearchOutlined,
  UserOutlined,
  PhoneOutlined,
  MailOutlined,
  HomeOutlined,
  TeamOutlined,
  StarOutlined,
  StarFilled,
} from '@ant-design/icons';
import { useGo, getDefaultFilter } from '@refinedev/core';

const { Title, Text } = Typography;
const { Option } = Select;

interface Contact {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  mobile?: string;
  job_title?: string;
  company?: {
    id: number;
    name: string;
  };
  street?: string;
  city?: string;
  country?: string;
  is_company: boolean;
  category_id?: {
    id: number;
    name: string;
    color: number;
  }[];
  supplier_rank: number;
  customer_rank: number;
  is_favorite?: boolean;
  create_date: string;
}

const getContactTypeTag = (contact: Contact) => {
  const types = [];
  
  if (contact.customer_rank > 0) {
    types.push(<Tag key="customer" color="blue">Cliente</Tag>);
  }
  
  if (contact.supplier_rank > 0) {
    types.push(<Tag key="supplier" color="green">Proveedor</Tag>);
  }
  
  if (contact.is_company) {
    types.push(<Tag key="company" color="purple">Empresa</Tag>);
  } else {
    types.push(<Tag key="person" color="orange">Persona</Tag>);
  }
  
  return types;
};

const Contacts: React.FC = () => {
  const go = useGo();

  const { tableProps, filters, searchFormProps } = useTable<Contact>({
    resource: 'contacts',
    onSearch: (values: any) => {
      return [
        {
          field: 'name',
          operator: 'contains',
          value: values.name,
        },
        {
          field: 'email',
          operator: 'contains',
          value: values.email,
        },
      ];
    },
    sorters: {
      initial: [
        {
          field: 'name',
          order: 'asc',
        },
      ],
    },
  });

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <TeamOutlined style={{ fontSize: '24px', marginRight: '12px', color: '#1890ff' }} />
            <Title level={2} style={{ margin: 0 }}>Gestión de Contactos</Title>
          </div>
          
          <CreateButton onClick={() => go({ to: '/crm/contacts/create' })}>
            Nuevo Contacto
          </CreateButton>
        </div>
        
        <List>
          <Table
            {...tableProps}
            rowKey="id"
            scroll={{ x: 1400 }}
            pagination={{
              ...tableProps.pagination,
              showSizeChanger: true,
              showQuickJumper: true,
              showTotal: (total, range) =>
                `${range[0]}-${range[1]} de ${total} contactos`,
            }}
          >
            <Table.Column
              dataIndex="name"
              title="Nombre"
              filterDropdown={(props) => (
                <FilterDropdown {...props}>
                  <Input
                    placeholder="Buscar nombre..."
                    prefix={<SearchOutlined />}
                  />
                </FilterDropdown>
              )}
              defaultFilteredValue={getDefaultFilter('name', filters, 'contains')}
              render={(value: string, record: Contact) => (
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar 
                    size="small" 
                    icon={record.is_company ? <HomeOutlined /> : <UserOutlined />}
                    style={{ marginRight: '8px' }}
                  />
                  <div>
                    <div style={{ fontWeight: 'bold', color: '#1890ff', display: 'flex', alignItems: 'center' }}>
                      {value}
                      {record.is_favorite && (
                        <StarFilled style={{ color: '#faad14', marginLeft: '4px', fontSize: '12px' }} />
                      )}
                    </div>
                    {record.job_title && (
                      <Text type="secondary" style={{ fontSize: '12px' }}>
                        {record.job_title}
                      </Text>
                    )}
                  </div>
                </div>
              )}
            />
            
            <Table.Column
              dataIndex="email"
              title="Email"
              filterDropdown={(props) => (
                <FilterDropdown {...props}>
                  <Input
                    placeholder="Buscar email..."
                    prefix={<MailOutlined />}
                  />
                </FilterDropdown>
              )}
              defaultFilteredValue={getDefaultFilter('email', filters, 'contains')}
              render={(value: string) => 
                value ? (
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <MailOutlined style={{ marginRight: '4px', color: '#1890ff' }} />
                    <a href={`mailto:${value}`}>{value}</a>
                  </div>
                ) : '-'
              }
            />
            
            <Table.Column
              dataIndex="phone"
              title="Teléfono"
              render={(value: string, record: Contact) => {
                const phone = value || record.mobile;
                return phone ? (
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <PhoneOutlined style={{ marginRight: '4px', color: '#52c41a' }} />
                    <a href={`tel:${phone}`}>{phone}</a>
                  </div>
                ) : '-';
              }}
            />
            
            <Table.Column
              dataIndex="company"
              title="Empresa"
              render={(company: any, record: Contact) => {
                if (record.is_company) {
                  return (
                    <Tag color="purple">
                      <HomeOutlined /> Es Empresa
                    </Tag>
                  );
                }
                return company?.name || '-';
              }}
            />
            
            <Table.Column
              title="Ubicación"
              render={(_, record: Contact) => {
                const location = [];
                if (record.city) location.push(record.city);
                if (record.country) location.push(record.country);
                
                return location.length > 0 ? (
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <HomeOutlined style={{ marginRight: '4px', color: '#722ed1' }} />
                    {location.join(', ')}
                  </div>
                ) : '-';
              }}
            />
            
            <Table.Column
              title="Tipo"
              render={(_, record: Contact) => (
                <Space wrap>
                  {getContactTypeTag(record)}
                </Space>
              )}
              filters={[
                { text: 'Cliente', value: 'customer' },
                { text: 'Proveedor', value: 'supplier' },
                { text: 'Empresa', value: 'company' },
                { text: 'Persona', value: 'person' },
              ]}
            />
            
            <Table.Column
              dataIndex="category_id"
              title="Categorías"
              render={(categories: any[]) => {
                if (!categories || categories.length === 0) return '-';
                
                return (
                  <Space wrap>
                    {categories.slice(0, 2).map((category) => (
                      <Tag 
                        key={category.id} 
                        color={`hsl(${(category.color || 0) * 36}, 70%, 50%)`}
                        style={{ fontSize: '11px' }}
                      >
                        {category.name}
                      </Tag>
                    ))}
                    {categories.length > 2 && (
                      <Tooltip title={categories.slice(2).map(c => c.name).join(', ')}>
                        <Tag style={{ fontSize: '11px' }}>+{categories.length - 2}</Tag>
                      </Tooltip>
                    )}
                  </Space>
                );
              }}
            />
            
            <Table.Column
              dataIndex="create_date"
              title="Fecha Creación"
              render={(value: string) => (
                <Text type="secondary">
                  {new Date(value).toLocaleDateString('es-ES')}
                </Text>
              )}
              sorter
            />
            
            <Table.Column
              title="Acciones"
              dataIndex="actions"
              fixed="right"
              width={150}
              render={(_, record: Contact) => (
                <Space>
                  <Tooltip title="Ver detalles">
                    <Button
                      type="link"
                      size="small"
                      icon={<UserOutlined />}
                      onClick={() => go({ to: `/crm/contacts/show/${record.id}` })}
                    />
                  </Tooltip>
                  
                  <EditButton
                    hideText
                    size="small"
                    recordItemId={record.id}
                    onClick={() => go({ to: `/crm/contacts/edit/${record.id}` })}
                  />
                  
                  <DeleteButton
                    hideText
                    size="small"
                    recordItemId={record.id}
                  />
                </Space>
              )}
            />
          </Table>
        </List>
      </Card>
    </div>
  );
};

export default Contacts;