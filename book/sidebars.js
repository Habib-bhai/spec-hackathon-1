// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // Main tutorial sidebar
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: Introduction to ROS 2',
      items: [
        'module-1-ros2/week-01-intro',
        'module-1-ros2/week-02-nodes-topics',
        'module-1-ros2/week-03-services',
        'module-1-ros2/week-04-actions',
        'module-1-ros2/week-05-launch',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 2: Robot Simulation',
      items: [
        'module-2-gazebo/week-06-simulation',
        'module-2-gazebo/week-07-urdf',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac',
      items: [
        'module-3-isaac/week-08-nvidia-intro',
        'module-3-isaac/week-09-isaac-sim',
        'module-3-isaac/week-10-reinforcement',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 4: VLA Models',
      items: [
        'module-4-vla/week-11-vision',
        'module-4-vla/week-12-language',
        'module-4-vla/week-13-integration',
      ],
      collapsed: false,
    },
  ],
};

export default sidebars;
