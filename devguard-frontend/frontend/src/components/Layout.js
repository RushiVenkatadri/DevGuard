// src/components/Layout.js

import React from 'react';

const Layout = ({ children }) => {
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-1/5 bg-gray-800 text-white p-4">
        <h2 className="text-xl font-bold">DevGuard</h2>
        <ul className="mt-8">
          <li className="mb-4"><a href="/" className="text-white">Dashboard</a></li>
          <li className="mb-4"><a href="/scan" className="text-white">Scan Projects</a></li>
          <li className="mb-4"><a href="/scan-api" className="text-white">Scan APIs</a></li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6 bg-gray-100">
        {children}
      </div>
    </div>
  );
};

export default Layout;
