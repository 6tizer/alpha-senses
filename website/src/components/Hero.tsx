import React from 'react';

const Hero: React.FC = () => {
  const scrollToSkills = () => {
    document.getElementById('skills')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ 
          backgroundImage: 'url(/hero.png)',
        }}
      >
        {/* Overlay for better text readability */}
        <div className="absolute inset-0 bg-gradient-to-t from-deep-space via-deep-space/70 to-deep-space/30" />
      </div>

      {/* Content */}
      <div className="relative z-10 text-center px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
        {/* Logo/Brand */}
        <div className="mb-8">
          <img 
            src="/logo.jpg" 
            alt="Alpha Senses Logo" 
            className="w-20 h-20 rounded-full mx-auto mb-6 border-2 border-alpha-green/50 shadow-lg shadow-alpha-green/20"
          />
        </div>

        {/* Main Title */}
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 tracking-tight">
          <span className="bg-gradient-to-r from-white via-alpha-green to-alpha-purple bg-clip-text text-transparent">
            Alpha Senses
          </span>
        </h1>

        {/* Tagline */}
        <p className="text-2xl sm:text-3xl lg:text-4xl font-light mb-4 text-white/90">
          Agents Think.
        </p>
        <p className="text-2xl sm:text-3xl lg:text-4xl font-light mb-12 text-alpha-green">
          Now They Sense.
        </p>

        {/* Description */}
        <p className="text-lg text-gray-300 max-w-2xl mx-auto mb-12 leading-relaxed">
          为 AI Agents 赋予真正的感官能力。通过 OpenClaw 协议，
          让你的 Agent 能够看、听、说、感知世界。
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <a
            href="https://github.com/AlphaSenses"
            target="_blank"
            rel="noopener noreferrer"
            className="group flex items-center gap-2 px-8 py-4 bg-white/10 hover:bg-white/20 
                       border border-white/20 hover:border-alpha-green/50 rounded-full
                       transition-all duration-300 backdrop-blur-sm"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
            </svg>
            <span className="font-medium">GitHub</span>
          </a>

          <a
            href="https://clawhub.alphasenses.io"
            target="_blank"
            rel="noopener noreferrer"
            className="group flex items-center gap-2 px-8 py-4 bg-alpha-green hover:bg-alpha-green/90 
                       text-deep-space font-semibold rounded-full transition-all duration-300
                       hover:shadow-lg hover:shadow-alpha-green/30 hover:transform hover:scale-105"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span>ClawHub</span>
          </a>

          <button
            onClick={scrollToSkills}
            className="group flex items-center gap-2 px-8 py-4 bg-alpha-purple/20 hover:bg-alpha-purple/30 
                       border border-alpha-purple/50 hover:border-alpha-purple rounded-full
                       transition-all duration-300 backdrop-blur-sm"
          >
            <span className="font-medium text-alpha-purple group-hover:text-white transition-colors">
              Explore Skills
            </span>
            <svg 
              className="w-5 h-5 text-alpha-purple group-hover:text-white transform group-hover:translate-y-1 transition-all" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          </button>
        </div>

        {/* Stats */}
        <div className="mt-20 grid grid-cols-3 gap-8 max-w-md mx-auto">
          <div className="text-center">
            <div className="text-3xl font-bold text-alpha-green">11</div>
            <div className="text-sm text-gray-400 mt-1">Skills</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-alpha-purple">4</div>
            <div className="text-sm text-gray-400 mt-1">Senses</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-white">∞</div>
            <div className="text-sm text-gray-400 mt-1">Possibilities</div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <svg 
          className="w-6 h-6 text-alpha-green" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </div>
    </section>
  );
};

export default Hero;
