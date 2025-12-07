/// <reference types="react" />
/// <reference types="react-dom" />

// CSS Modules
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.module.scss' {
  const classes: { [key: string]: string };
  export default classes;
}

// Docusaurus modules
declare module '@docusaurus/Link' {
  import type { ComponentProps } from 'react';
  export interface Props extends ComponentProps<'a'> {
    readonly to: string;
  }
  export default function Link(props: Props): JSX.Element;
}

declare module '@docusaurus/useDocusaurusContext' {
  export interface DocusaurusContext {
    siteConfig: {
      title: string;
      tagline: string;
      url: string;
      baseUrl: string;
      customFields?: Record<string, unknown>;
      [key: string]: unknown;
    };
    [key: string]: unknown;
  }
  export default function useDocusaurusContext(): DocusaurusContext;
}

declare module '@docusaurus/BrowserOnly' {
  import type { ComponentType, ReactElement } from 'react';
  export interface Props {
    children?: () => JSX.Element;
    fallback?: ReactElement;
  }
  const BrowserOnly: ComponentType<Props>;
  export default BrowserOnly;
}

declare module '@theme/Layout' {
  import type { ReactNode } from 'react';
  export interface Props {
    children: ReactNode;
    title?: string;
    description?: string;
  }
  export default function Layout(props: Props): JSX.Element;
}

declare module '@theme/Heading' {
  import type { ComponentProps } from 'react';
  export interface Props extends ComponentProps<'h1'> {
    as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
  }
  export default function Heading(props: Props): JSX.Element;
}

declare module '@site/src/components/ChatWidget' {
  export interface ChatWidgetProps {
    apiUrl?: string;
    chapterSlug?: string;
  }
  export default function ChatWidget(props: ChatWidgetProps): JSX.Element;
}

declare module '@site/src/pages/index.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}
