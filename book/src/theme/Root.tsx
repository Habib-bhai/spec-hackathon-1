import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import ChatWidget from '@site/src/components/ChatWidget';

interface RootProps {
  children: React.ReactNode;
}

// Default implementation, that you can customize
export default function Root({children}: RootProps) {
  const {siteConfig} = useDocusaurusContext();
  const apiUrl = (siteConfig.customFields?.apiUrl as string) || 'http://localhost:8000';
  
  return (
    <>
      {children}
      <BrowserOnly fallback={<div>Loading...</div>}>
        {() => <ChatWidget apiUrl={apiUrl} />}
      </BrowserOnly>
    </>
  );
}
