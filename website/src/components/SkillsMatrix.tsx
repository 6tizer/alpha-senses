import React from 'react';
import { skills } from '../data/skills';
import SkillCard from './SkillCard';

const SkillsMatrix: React.FC = () => {
  return (
    <section id="skills" className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            <span className="bg-gradient-to-r from-alpha-green to-alpha-purple bg-clip-text text-transparent">
              Skills Matrix
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            11 个预置技能，让 Agents 拥有真正的感官能力
          </p>
          <div className="mt-4 inline-flex items-center gap-2 text-sm text-gray-500">
            <span className="w-2 h-2 rounded-full bg-alpha-green animate-pulse" />
            Powered by fal.ai & Moonshot
          </div>
        </div>

        {/* Skills Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {skills.map((skill, index) => (
            <SkillCard key={skill.id} skill={skill} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default SkillsMatrix;
