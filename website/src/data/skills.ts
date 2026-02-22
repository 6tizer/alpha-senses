export interface Skill {
  id: string;
  name: string;
  description: string;
  model: string;
  icon: string;
}

export const skills: Skill[] = [
  {
    id: 'audio-analyzer',
    name: 'Audio Analyzer',
    description: '将音频转换为文字并分析情绪和生成内容摘要',
    model: 'MiniMax Speech Recognition',
    icon: '🎵',
  },
  {
    id: 'visual-analyzer',
    name: 'Visual Analyzer',
    description: '智能分析图像内容，提取关键信息和洞察',
    model: 'Moonshot Kimi-k2.5',
    icon: '👁️',
  },
  {
    id: 'text-to-speech',
    name: 'Text to Speech',
    description: '将文字转换为自然语音，支持多种中文音色和情绪',
    model: 'fal.ai TTS',
    icon: '🔊',
  },
  {
    id: 'idea-visualizer',
    name: 'Idea Visualizer',
    description: '将文字想法转换为高质量图像，支持多模型对比',
    model: 'fal.ai FLUX',
    icon: '✨',
  },
  {
    id: 'image-styler',
    name: 'Image Styler',
    description: '将图片转换成赛博朋克、动漫、电影感等指定艺术风格',
    model: 'fal.ai Style Transfer',
    icon: '🎨',
  },
  {
    id: 'avatar-gen',
    name: 'Avatar Gen',
    description: '将人物图片转换为动态 Avatar 视频，支持自定义动作参考',
    model: 'fal.ai Avatar',
    icon: '👤',
  },
  {
    id: 'bg-remover',
    name: 'BG Remover',
    description: '智能去除图片背景，保留主体内容',
    model: 'fal.ai Image Processing',
    icon: '✂️',
  },
  {
    id: 'video-analyzer',
    name: 'Video Analyzer',
    description: '使用多模态模型分析视频内容并生成结构化报告',
    model: 'Moonshot Kimi-k2.5',
    icon: '🎬',
  },
  {
    id: 'video-gen',
    name: 'Video Gen',
    description: '通过文字描述或参考图片生成 AI 短视频',
    model: 'fal.ai Video',
    icon: '🎥',
  },
  {
    id: 'voice-clone',
    name: 'Voice Clone',
    description: '克隆声音样本并合成指定文字内容的语音',
    model: 'fal.ai Voice',
    icon: '🎙️',
  },
  {
    id: 'tweet-image-gen',
    name: 'Tweet Image Gen',
    description: '根据推文内容和风格自动生成社交媒体配图',
    model: 'fal.ai + Moonshot',
    icon: '🐦',
  },
];
