import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from '../components/Layout';
import { PrivateRoute } from '../components/PrivateRoute';
import {
  Login,
  Register,
  Dashboard,
  DailyPractice,
  WrongQuestions,
  StudyPlans,
  KnowledgeProfile,
  UserProfile
} from '../pages';

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      <Route
        path="/"
        element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="daily-practice" element={<DailyPractice />} />
        <Route path="wrong-questions" element={<WrongQuestions />} />
        <Route path="study-plans" element={<StudyPlans />} />
        <Route path="knowledge-profile" element={<KnowledgeProfile />} />
        <Route path="profile" element={<UserProfile />} />
      </Route>
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}; 