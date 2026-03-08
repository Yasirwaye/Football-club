import React from 'react';
import { Target, Activity, Dumbbell, Users, ChevronRight } from 'lucide-react';

const Training = () => {
  const programs = [
    {
      icon: <Target className="w-8 h-8" />,
      title: "Technical Skills",
      description: "Ball mastery, passing precision, and shooting technique developed through repetitive drills and small-sided games.",
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: <Activity className="w-8 h-8" />,
      title: "Tactical Awareness",
      description: "Game intelligence, positional play, and decision-making training using video analysis and scenario-based sessions.",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: <Dumbbell className="w-8 h-8" />,
      title: "Physical Conditioning",
      description: "Age-appropriate strength, speed, agility, and endurance programs designed by sports scientists.",
      color: "from-orange-500 to-red-500"
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Sports Science",
      description: "Nutrition planning, injury prevention, recovery protocols, and mental performance coaching.",
      color: "from-green-500 to-emerald-500"
    }
  ];

  return (
    <section id="training" className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-display text-4xl md:text-5xl font-bold mb-4">
            Training & <span className="gradient-text">Development</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Our comprehensive curriculum covers every aspect of modern football development
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {programs.map((program, idx) => (
            <div
              key={idx}
              className="glass rounded-3xl p-8 card-hover group cursor-pointer"
            >
              <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${program.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                {program.icon}
              </div>
              <h3 className="font-display text-2xl font-bold mb-3">{program.title}</h3>
              <p className="text-gray-400 leading-relaxed">{program.description}</p>
              <div className="mt-6 flex items-center text-cyan-400 font-semibold group-hover:translate-x-2 transition-transform">
                <span>Learn More</span>
                <ChevronRight className="w-5 h-5" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Training;