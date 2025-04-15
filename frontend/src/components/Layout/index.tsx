import React from 'react';
import { Layout as AntLayout, Menu } from 'antd';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  BookOutlined,
  WarningOutlined,
  CalendarOutlined,
  ProfileOutlined,
  UserOutlined,
  LogoutOutlined
} from '@ant-design/icons';
import { useAuth } from '../../hooks/useAuth';
import './style.css';

const { Header, Sider, Content } = AntLayout;

export const Layout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: '仪表盘'
    },
    {
      key: '/daily-practice',
      icon: <BookOutlined />,
      label: '每日练习'
    },
    {
      key: '/wrong-questions',
      icon: <WarningOutlined />,
      label: '错题本'
    },
    {
      key: '/study-plans',
      icon: <CalendarOutlined />,
      label: '学习计划'
    },
    {
      key: '/knowledge-profile',
      icon: <ProfileOutlined />,
      label: '知识图谱'
    },
    {
      key: '/profile',
      icon: <UserOutlined />,
      label: '个人中心'
    }
  ];

  const handleMenuClick = (key: string) => {
    navigate(key);
  };

  return (
    <AntLayout className="layout">
      <Sider width={200} className="sider">
        <div className="logo">StudySync</div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => handleMenuClick(key)}
        />
        <div className="logout" onClick={logout}>
          <LogoutOutlined /> 退出登录
        </div>
      </Sider>
      <AntLayout>
        <Header className="header">
          <h1>StudySync - 智能学习助手</h1>
        </Header>
        <Content className="content">
          <Outlet />
        </Content>
      </AntLayout>
    </AntLayout>
  );
}; 