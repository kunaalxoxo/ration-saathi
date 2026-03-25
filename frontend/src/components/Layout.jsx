import React from 'react';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gov-ash">
      <Sidebar />
      <Navbar />
      <main className="pl-[280px] pt-20 min-h-screen transition-all duration-300">
        <div className="p-10 max-w-[1600px] mx-auto animate-fade-in-up">
          {children}
        </div>
      </main>
      
      {/* Background Decor */}
      <div className="fixed top-0 left-[280px] right-0 h-[500px] bg-gradient-to-b from-brand-50/50 to-transparent -z-10 pointer-events-none"></div>
    </div>
  );
};

export default Layout;
