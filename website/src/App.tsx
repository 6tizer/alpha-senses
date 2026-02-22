import Hero from './components/Hero';
import PainPoints from './components/PainPoints';
import SkillsMatrix from './components/SkillsMatrix';
import CTAFooter from './components/CTAFooter';

function App() {
  return (
    <div className="min-h-screen bg-deep-space">
      <Hero />
      <PainPoints />
      <SkillsMatrix />
      <CTAFooter />
    </div>
  );
}

export default App;
