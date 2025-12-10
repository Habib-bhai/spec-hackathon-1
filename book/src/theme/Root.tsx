import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import ChatWidget from '@site/src/components/ChatWidget';

interface RootProps {
  children: React.ReactNode;
}

/**
 * Skip to content link for accessibility
 * Hidden by default, visible on focus for keyboard navigation
 */
function SkipToContent(): JSX.Element {
  return (
    <a 
      href="#__docusaurus" 
      className="skip-to-content"
      tabIndex={0}
    >
      Skip to main content
    </a>
  );
}

// Default implementation, that you can customize
export default function Root({children}: RootProps) {
  const {siteConfig} = useDocusaurusContext();
  const apiUrl = (siteConfig.customFields?.apiUrl as string) || 'http://localhost:8000';
  
  return (
    <>
      <SkipToContent />
      {children}
      <BrowserOnly fallback={<div>Loading...</div>}>
        {() => <ChatWidget apiUrl={apiUrl} />}
      </BrowserOnly>
    </>
  );
}
