import type { Skill } from '../data/skills';

interface SkillCardProps {
  skill: Skill;
  index: number;
}

const SkillCard: React.FC<SkillCardProps> = ({ skill, index }) => {
  return (
    <div
      className="group relative bg-deep-space-light border border-white/10 rounded-xl p-6 
                 hover:border-alpha-green/50 transition-all duration-300 
                 hover:transform hover:-translate-y-1 hover:shadow-lg hover:shadow-alpha-green/10"
      style={{
        animationDelay: `${index * 50}ms`,
      }}
    >
      {/* Glow effect */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-alpha-green/5 to-alpha-purple/5 
                      opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      {/* Content */}
      <div className="relative z-10">
        {/* Icon and Name */}
        <div className="flex items-center gap-3 mb-3">
          <span className="text-3xl" role="img" aria-label={skill.name}>
            {skill.icon}
          </span>
          <h3 className="text-lg font-semibold text-white group-hover:text-alpha-green transition-colors">
            {skill.name}
          </h3>
        </div>
        
        {/* Description */}
        <p className="text-gray-400 text-sm mb-4 leading-relaxed">
          {skill.description}
        </p>
        
        {/* Model Badge */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-alpha-purple bg-alpha-purple/10 px-2 py-1 rounded-full">
            {skill.model}
          </span>
        </div>
      </div>
      
      {/* Corner accent */}
      <div className="absolute top-0 right-0 w-16 h-16 overflow-hidden rounded-tr-xl">
        <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-alpha-green/10 to-transparent 
                        transform rotate-45 translate-x-16 -translate-y-16 group-hover:from-alpha-green/20 
                        transition-colors duration-300" />
      </div>
    </div>
  );
};

export default SkillCard;
