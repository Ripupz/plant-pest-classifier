import { useState } from 'react';
import { HomePage } from './components/HomePage';
import { ClassificationPage } from './components/ClassificationPage';

export default function App() {
  const [currentPage, setCurrentPage] = useState<'home' | 'classify'>('home');

  return (
    <div className="min-h-screen bg-linear-to-br from-emerald-50 to-teal-100">
      {currentPage === 'home' && <HomePage onNavigate={() => setCurrentPage('classify')} />}
      {currentPage === 'classify' && <ClassificationPage onNavigate={() => setCurrentPage('home')} />}
    </div>
  );
}
