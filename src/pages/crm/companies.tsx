import React from 'react';
import {
  List,
  useTable,
  EditButton,
  ShowButton,
  DeleteButton,
  CreateButton,
  FilterDropdown,
} from '@refinedev/antd';
import { Table, Space, Input, Card, Typography, Tag } from 'antd';
import { SearchOutlined, ShopOutlined } from '@ant-design/icons';
import { useGo, getDefaultFilter } from '@refinedev/core';

const { Title } = Typography;

interface Company {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  website?: string;
  industry?: string;
  city?: string;
  country?: string;
  is_company: boolean;
  customer_rank: number;
  supplier_rank: number;
}

const Companies: React.FC = () => {
  const go = useGo();

  const { tableProps, filters, searchFormProps } = useTable<Company>({
    resource: 'companies',
    onSearch: (values: any) => {
      return [
        {
          field: 'name',
          operator: 'contains',
          value: values.name,
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
    filters: {
      initial: [
        {
          field: 'is_company',
          operator: 'eq',
          value: true,
        },
      ],
    },
  });

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '24px' }}>
          <ShopOutlined style={{ fontSize: '24px', marginRight: '12px', color: '#1890ff' }} />
          <Title level={2} style={{ margin: 0 }}>Gestión de Empresas</Title>
        </div>
        
        <List
          headerButtons={[
            <CreateButton key="create" onClick={() => go({ to: '/crm/companies/create' })}>
              Nueva Empresa
            </CreateButton>,
          ]}
        >
          <Table
            {...tableProps}
            rowKey="id"
            scroll={{ x: 1200 }}
            pagination={{
              ...tableProps.pagination,
              showSizeChanger: true,
              showQuickJumper: true,
              showTotal: (total, range) =>
                `${range[0]}-${range[1]} de ${total} empresas`,
            }}
          >
            <Table.Column
              dataIndex="name"
              title="Nombre de la Empresa"
              filterDropdown={(props) => (
                <FilterDropdown {...props}>
                  <Input
                    placeholder="Buscar empresa..."
                    prefix={<SearchOutlined />}
                  />
                </FilterDropdown>
              )}
              defaultFilteredValue={getDefaultFilter('name', filters, 'contains')}
              render={(value: string) => (
                <div style={{ fontWeight: 'bold', color: '#1890ff' }}>
                  {value}
                </div>
              )}
            />
            
            <Table.Column
              dataIndex="email"
              title="Email"
              render={(value: string) => value || '-'}
            />
            
            <Table.Column
              dataIndex="phone"
              title="Teléfono"
              render={(value: string) => value || '-'}
            />
            
            <Table.Column
              dataIndex="city"
              title="Ciudad"
              render={(value: string) => value || '-'}
            />
            
            <Table.Column
              dataIndex="industry"
              title="Sector"
              render={(value: string) => 
                value ? <Tag color="blue">{value}</Tag> : '-'
              }
            />
            
            <Table.Column
              dataIndex="customer_rank"
              title="Tipo"
              render={(value: number, record: Company) => {
                const tags = [];
                if (record.customer_rank > 0) {
                  tags.push(<Tag key="customer" color="green">Cliente</Tag>);
                }
                if (record.supplier_rank > 0) {
                  tags.push(<Tag key="supplier" color="orange">Proveedor</Tag>);
                }
                return tags.length > 0 ? tags : <Tag color="default">Empresa</Tag>;
              }}
            />
            
            <Table.Column
              title="Acciones"
              dataIndex="actions"
              fixed="right"
              width={200}
              render={(_, record: Company) => (
                <Space>
                  <ShowButton
                    hideText
                    size="small"
                    recordItemId={record.id}
                    onClick={() => go({ to: `/crm/companies/show/${record.id}` })}
                  />
                  <EditButton
                    hideText
                    size="small"
                    recordItemId={record.id}
                    onClick={() => go({ to: `/crm/companies/edit/${record.id}` })}
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

export default Companies;