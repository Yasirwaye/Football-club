import React from 'react';
import { Quote } from 'lucide-react';

const Testimonials = () => {
  const testimonials = [
    {
      name: "Tom Bradley",
      role: "U18 Graduate, Now at Manchester City",
      quote: "Eastleigh Academy gave me the foundation I needed. The coaching staff pushed me beyond my limits every single day.",
      image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80"
    },
    {
      name: "Sarah Mitchell",
      role: "Parent of U16 Player",
      quote: "The transformation in my son's confidence and ability has been incredible. The facilities are world-class and the staff genuinely care.",
      image: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80"
    },
    {
      name: "David Okonkwo",
      role: "Senior Squad Captain",
      quote: "I've been here since I was 11. This academy isn't just about football—it's about building character and discipline.",
      image: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80"
    }
  ];

  return (
    <section id="testimonials" className="py-20 bg-gradient-to-b from-[#050810] to-[#0a0e1a]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-display text-4xl md:text-5xl font-bold mb-4">
            What Our <span className="gradient-text">Players Say</span>
          </h2>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, idx) => (
            <div key={idx} className="glass rounded-3xl p-8 card-hover relative">
              <div className="absolute -top-4 left-8">
                <div className="w-8 h-8 bg-cyan-400 rounded-full flex items-center justify-center">
                  <Quote className="w-5 h-5 text-[#0a0e1a]" />
                </div>
              </div>
              <p className="text-gray-300 italic mb-6 mt-4 leading-relaxed">
                "{testimonial.quote}"
              </p>
              <div className="flex items-center space-x-4">
                <img
                  src={testimonial.image}
                  alt={testimonial.name}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div>
                  <div className="font-bold">{testimonial.name}</div>
                  <div className="text-sm text-cyan-400">{testimonial.role}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;