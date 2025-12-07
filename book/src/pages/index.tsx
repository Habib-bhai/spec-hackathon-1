import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Learning 🚀
          </Link>
        </div>
      </div>
    </header>
  );
}

type FeatureItem = {
  title: string;
  icon: string;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: '🤖 ROS 2 Fundamentals',
    icon: '🤖',
    description: (
      <>
        Master the Robot Operating System 2 with hands-on examples.
        Learn nodes, topics, services, actions, and launch files.
      </>
    ),
  },
  {
    title: '🎮 Robot Simulation',
    icon: '🎮',
    description: (
      <>
        Simulate robots in Gazebo and NVIDIA Isaac Sim.
        Build URDF models and test in realistic environments.
      </>
    ),
  },
  {
    title: '🧠 AI Integration',
    icon: '🧠',
    description: (
      <>
        Integrate Vision-Language-Action models with robots.
        Enable natural language control and visual understanding.
      </>
    ),
  },
];

function Feature({title, icon, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <div className={styles.featureIcon}>{icon}</div>
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

function HomepageModules(): JSX.Element {
  return (
    <section className={styles.modules}>
      <div className="container">
        <Heading as="h2" className="text--center margin-bottom--lg">
          Learning Modules
        </Heading>
        <div className="row">
          <div className="col col--6">
            <div className={styles.moduleCard}>
              <Heading as="h3">Module 1: Introduction to ROS 2</Heading>
              <p>
                Learn the fundamentals of ROS 2, including nodes, topics,
                services, actions, and launch files.
              </p>
              <Link to="/docs/module-1-ros2/week-01-intro">
                Start Module 1 →
              </Link>
            </div>
          </div>
          <div className="col col--6">
            <div className={styles.moduleCard}>
              <Heading as="h3">Module 2: Robot Simulation</Heading>
              <p>
                Master Gazebo simulation, URDF models, and sensor integration
                for realistic robot testing.
              </p>
              <Link to="/docs/module-2-gazebo/week-06-simulation">
                Start Module 2 →
              </Link>
            </div>
          </div>
          <div className="col col--6">
            <div className={styles.moduleCard}>
              <Heading as="h3">Module 3: NVIDIA Isaac</Heading>
              <p>
                Explore Isaac Sim and Isaac Lab for advanced simulation and
                reinforcement learning.
              </p>
              <Link to="/docs/module-3-isaac/week-08-nvidia-intro">
                Start Module 3 →
              </Link>
            </div>
          </div>
          <div className="col col--6">
            <div className={styles.moduleCard}>
              <Heading as="h3">Module 4: VLA Models</Heading>
              <p>
                Integrate Vision-Language-Action models for intelligent robot
                control with natural language.
              </p>
              <Link to="/docs/module-4-vla/week-11-vision">
                Start Module 4 →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Learn robotics and AI with hands-on projects">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <HomepageModules />
      </main>
    </Layout>
  );
}
