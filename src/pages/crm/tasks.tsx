import React, { useState } from 'react';
import {
  List,
  useTable,
  EditButton,
  DeleteButton,
  CreateButton,
  FilterDropdown,
} from '@refinedev/antd';
import {
  Table,
  Card,
  Space,
  Button,
  Input,
  Select,
  Tag,
  Avatar,
  Typography,
  Row,
  Col,
  Dropdown,
  Menu,
  Badge,
  Tooltip,
  Progress,
  DatePicker,
  Form,
  Modal,
  message,
} from 'antd';
import {
  SearchOutlined,
  ProjectOutlined,
  CalendarOutlined,
  UserOutlined,
  FlagOutlined,
  AppstoreOutlined,
  UnorderedListOutlined,
} from '@ant-design/icons';
import { useGo, getDefaultFilter } from '@refinedev/core';

const { Title, Text } = Typography;
const { Option } = Select;

interface Task {
  id: number;
  name: string;
  description?: string;
  stage: 'todo' | 'in_progress' | 'review' | 'done';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  assigned_user?: {
    id: number;
    name: string;
    avatar?: string;
  };
  company?: {
    id: number;
    name: string;
  };
  date_deadline?: string;
  progress?: number;
  create_date: string;
}

const priorityColors = {
  low: 'green',
  medium: 'blue',
  high: 'orange',
  urgent: 'red',
};

const stageColors = {
  todo: 'default',
  in_progress: 'processing',
  review: 'warning',
  done: 'success',
};

const stageLabels = {
  todo: 'Por Hacer',
  in_progress: 'En Progreso',
  review: 'En Revisión',
  done: 'Completado',
};

const Tasks: React.FC = () => {
  const go = useGo();
  const [viewMode, setViewMode] = useState<'table' | 'kanban'>('table');

  const { tableProps, filters, searchFormProps } = useTable<Task>({
    resource: 'tasks',
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
          field: 'create_date',
          order: 'desc',
        },
      ],
    },
  });

  const renderKanbanView = () => {
    const stages = ['todo', 'in_progress', 'review', 'done'];
    const tasks = tableProps.dataSource || [];
    
    return (
      <Row gutter={[16, 16]}>
        {stages.map((stage) => {
          const stageTasks = tasks.filter((task: Task) => task.stage === stage);
          
          return (
            <Col key={stage} xs={24} sm={12} lg={6}>
              <Card
                title={
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span>{stageLabels[stage as keyof typeof stageLabels]}</span>
                    <Tag color={stageColors[stage as keyof typeof stageColors]}>
                      {stageTasks.length}
                    </Tag>
                  </div>
                }
                size="small"
                style={{ height: '600px', overflow: 'auto' }}
              >
                <Space direction="vertical" style={{ width: '100%' }} size="small">
                  {stageTasks.map((task: Task) => (
                    <Card
                      key={task.id}
                      size="small"
                      hoverable
                      style={{ cursor: 'pointer' }}
                      onClick={() => go({ to: `/crm/tasks/edit/${task.id}` })}
                    >
                      <div style={{ marginBottom: '8px' }}>
                        <Text strong>{task.name}</Text>
                      </div>
                      
                      {task.description && (
                        <div style={{ marginBottom: '8px' }}>
                          <Text type="secondary" style={{ fontSize: '12px' }}>
                            {task.description.substring(0, 100)}...
                          </Text>
                        </div>
                      )}
                      
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Tag color={priorityColors[task.priority as keyof typeof priorityColors]}>
                          {task.priority}
                        </Tag>
                        
                        {task.assigned_user && (
                          <Tooltip title={task.assigned_user.name}>
                            <Avatar size="small" icon={<UserOutlined />} />
                          </Tooltip>
                        )}
                      </div>
                      
                      {task.progress !== undefined && (
                        <div style={{ marginTop: '8px' }}>
                          <Progress percent={task.progress} size="small" />
                        </div>
                      )}
                    </Card>
                  ))}
                </Space>
              </Card>
            </Col>
          );
        })}
      </Row>
    );
  };

  const renderTableView = () => (
    <Table
      {...tableProps}
      rowKey="id"
      scroll={{ x: 1200 }}
      pagination={{
        ...tableProps.pagination,
        showSizeChanger: true,
        showQuickJumper: true,
        showTotal: (total, range) =>
          `${range[0]}-${range[1]} de ${total} tareas`,
      }}
    >
      <Table.Column
        dataIndex="name"
        title="Tarea"
        filterDropdown={(props) => (
          <FilterDropdown {...props}>
            <Input
              placeholder="Buscar tarea..."
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
        dataIndex="stage"
        title="Estado"
        render={(value: string) => (
          <Tag color={stageColors[value as keyof typeof stageColors]}>
            {stageLabels[value as keyof typeof stageLabels]}
          </Tag>
        )}
        filters={[
          { text: 'Por Hacer', value: 'todo' },
          { text: 'En Progreso', value: 'in_progress' },
          { text: 'En Revisión', value: 'review' },
          { text: 'Completado', value: 'done' },
        ]}
      />
      
      <Table.Column
        dataIndex="priority"
        title="Prioridad"
        render={(value: string) => (
          <Tag color={priorityColors[value as keyof typeof priorityColors]}>
            <FlagOutlined /> {value.toUpperCase()}
          </Tag>
        )}
        filters={[
          { text: 'Baja', value: 'low' },
          { text: 'Media', value: 'medium' },
          { text: 'Alta', value: 'high' },
          { text: 'Urgente', value: 'urgent' },
        ]}
      />
      
      <Table.Column
        dataIndex="assigned_user"
        title="Asignado a"
        render={(user: any) => 
          user ? (
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <Avatar size="small" icon={<UserOutlined />} style={{ marginRight: '8px' }} />
              {user.name}
            </div>
          ) : '-'
        }
      />
      
      <Table.Column
        dataIndex="company"
        title="Empresa"
        render={(company: any) => company?.name || '-'}
      />
      
      <Table.Column
        dataIndex="date_deadline"
        title="Fecha Límite"
        render={(value: string) => 
          value ? (
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <CalendarOutlined style={{ marginRight: '4px' }} />
              {new Date(value).toLocaleDateString('es-ES')}
            </div>
          ) : '-'
        }
      />
      
      <Table.Column
        dataIndex="progress"
        title="Progreso"
        render={(value: number) => 
          value !== undefined ? <Progress percent={value} size="small" /> : '-'
        }
      />
      
      <Table.Column
        title="Acciones"
        dataIndex="actions"
        fixed="right"
        width={150}
        render={(_, record: Task) => (
          <Space>
            <EditButton
              hideText
              size="small"
              recordItemId={record.id}
              onClick={() => go({ to: `/crm/tasks/edit/${record.id}` })}
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
  );

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <ProjectOutlined style={{ fontSize: '24px', marginRight: '12px', color: '#1890ff' }} />
            <Title level={2} style={{ margin: 0 }}>Gestión de Tareas</Title>
          </div>
          
          <Space>
            <Space.Compact>
              <Button
                type={viewMode === 'table' ? 'primary' : 'default'}
                icon={<UnorderedListOutlined />}
                onClick={() => setViewMode('table')}
              >
                Lista
              </Button>
              <Button
                type={viewMode === 'kanban' ? 'primary' : 'default'}
                icon={<AppstoreOutlined />}
                onClick={() => setViewMode('kanban')}
              >
                Kanban
              </Button>
            </Space.Compact>
            
            <CreateButton onClick={() => go({ to: '/crm/tasks/create' })}>
              Nueva Tarea
            </CreateButton>
          </Space>
        </div>
        
        <List>
          {viewMode === 'table' ? renderTableView() : renderKanbanView()}
        </List>
      </Card>
    </div>
  );
};

export default Tasks;