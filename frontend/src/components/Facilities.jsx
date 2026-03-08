import React from 'react';
import { ChevronRight } from 'lucide-react';

const Facilities = () => {
  const facilities = [
    {
      title: "Full-Size FIFA Pitch",
      description: "Professional-grade natural turf with floodlighting and drainage systems",
      image: "https://images.unsplash.com/photo-1577223625816-7546f13df25d?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
    },
    {
      title: "Performance Gym",
      description: "Elite strength and conditioning equipment with dedicated sports science lab",
      image: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
    },
    {
      title: "Tactical Classroom",
      description: "Video analysis suite with interactive whiteboards and stadium seating",
      image: "https://images.unsplash.com/photo-1509062522246-3755977927d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
    }
  ];

  return (
    <section id="facilities" className="py-20 bg-gradient-to-b from-[#0a0e1a] to-[#050810]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-display text-4xl md:text-5xl font-bold mb-4">
            World-Class <span className="gradient-text">Facilities</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Train in an environment designed for elite performance
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {facilities.map((facility, idx) => (
            <div key={idx} className="group relative rounded-3xl overflow-hidden aspect-[4/5] card-hover">
              <img
                src={facility.image}
                alt={facility.title}
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#0a0e1a] via-[#0a0e1a]/50 to-transparent opacity-90"></div>
              <div className="absolute bottom-0 left-0 right-0 p-6">
                <h3 className="font-display text-2xl font-bold mb-2">{facility.title}</h3>
                <p className="text-gray-300 text-sm">{facility.description}</p>
              </div>
              <div className="absolute top-4 right-4 w-12 h-12 glass rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <ChevronRight className="w-6 h-6" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Facilities;