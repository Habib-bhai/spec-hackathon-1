// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI Textbook',
  tagline: 'Learn robotics and AI with hands-on projects',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: process.env.SITE_URL || 'https://yourusername.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: process.env.BASE_URL || '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: process.env.GIT_USER || 'yourusername', // Usually your GitHub org/user name.
  projectName: 'physical-ai-textbook', // Usually your repo name.

  onBrokenLinks: 'warn',
  
  // Markdown configuration
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  // Internationalization (i18n) configuration
  // Supports: English, French, Arabic (RTL), Urdu (RTL)
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'fr', 'ar', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
        htmlLang: 'en-US',
        calendar: 'gregory',
      },
      fr: {
        label: 'Français',
        direction: 'ltr',
        htmlLang: 'fr-FR',
        calendar: 'gregory',
      },
      ar: {
        label: 'العربية',
        direction: 'rtl',
        htmlLang: 'ar-SA',
        calendar: 'gregory',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
        htmlLang: 'ur-PK',
        calendar: 'gregory',
      },
    },
  },

  // Custom fields for runtime access
  customFields: {
    apiUrl: process.env.API_URL || 'http://localhost:8000',
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Enable breadcrumbs for better navigation
          breadcrumbs: true,
          // Show last update time
          showLastUpdateTime: true,
          // Remove this to remove the "edit this page" links.
          editUrl: undefined,
        },
        blog: false, // Disable blog feature
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Social card image
      image: 'img/docusaurus-social-card.jpg',
      
      // Color mode configuration
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      
      // Table of contents configuration
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 4,
      },
      
      // Docs configuration
      docs: {
        sidebar: {
          hideable: true,
          autoCollapseCategories: true,
        },
      },
      
      navbar: {
        title: 'Physical AI Textbook',
        hideOnScroll: false,
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/yourusername/physical-ai-textbook',
            label: 'GitHub',
            position: 'right',
          },
          // Language selector dropdown
          {
            type: 'localeDropdown',
            position: 'right',
            dropdownItemsAfter: [
              {
                type: 'html',
                value: '<hr style="margin: 0.3rem 0;">',
              },
              {
                href: 'https://github.com/yourusername/physical-ai-textbook/issues',
                label: 'Help translate',
              },
            ],
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Learn',
            items: [
              {
                label: 'Getting Started',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/yourusername/physical-ai-textbook',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'json', 'yaml', 'cpp', 'cmake'],
        defaultLanguage: 'python',
        magicComments: [
          {
            className: 'theme-code-block-highlighted-line',
            line: 'highlight-next-line',
            block: {start: 'highlight-start', end: 'highlight-end'},
          },
          {
            className: 'code-block-error-line',
            line: 'error-next-line',
          },
        ],
      },
      // Announcement bar (optional - can be enabled for important notices)
      // announcementBar: {
      //   id: 'i18n_support',
      //   content: '🌍 Now available in French, Arabic, and Urdu!',
      //   backgroundColor: '#2563eb',
      //   textColor: '#ffffff',
      //   isCloseable: true,
      // },
    }),
};

export default config;
