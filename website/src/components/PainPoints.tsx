import React from 'react';

const painPoints = [
  {
    icon: '👁️',
    title: '看不见',
    description: 'Agent 无法理解图像、视频内容，错失视觉信息',
  },
  {
    icon: '👂',
    title: '听不见',
    description: '无法处理音频、语音，无法感知声音世界',
  },
  {
    icon: '🗣️',
    title: '说不出',
    description: '只能返回文字，无法生成语音、视频等多媒体内容',
  },
];

const PainPoints: React.FC = () => {
  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-deep-space-light/50">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            <span className="text-white">Agents 的</span>
            <span className="bg-gradient-to-r from-alpha-green to-alpha-purple bg-clip-text text-transparent">
              感官缺失
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            传统 AI Agents 被困在文本世界，无法真正感知和理解多模态信息
          </p>
        </div>

        {/* Pain Points Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {painPoints.map((point, index) => (
            <div
              key={index}
              className="relative group p-8 rounded-2xl bg-gradient-to-br from-white/5 to-transparent 
                         border border-white/10 hover:border-red-500/30 transition-all duration-300
                         hover:transform hover:-translate-y-2"
            >
              {/* Icon */}
              <div className="text-5xl mb-6 transform group-hover:scale-110 transition-transform duration-300">
                {point.icon}
              </div>

              {/* Content */}
              <h3 className="text-xl font-semibold text-white mb-3 group-hover:text-red-400 transition-colors">
                {point.title}
              </h3>
              <p className="text-gray-400 leading-relaxed">
                {point.description}
              </p>

              {/* Decorative line */}
              <div className="absolute bottom-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-red-500/50 to-transparent 
                              opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            </div>
          ))}
        </div>

        {/* Solution hint */}
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full bg-alpha-green/10 border border-alpha-green/30">
            <span className="text-alpha-green text-xl">✨</span>
            <span className="text-gray-300">
              Alpha Senses 让 Agents 拥有完整的
              <span className="text-alpha-green font-semibold"> 视觉、听觉、表达 </span>
              能力
            </span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PainPoints;
