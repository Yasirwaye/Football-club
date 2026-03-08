import React, { useState } from 'react';
import { Play } from 'lucide-react';

const Highlights = () => {
  const [isPlaying, setIsPlaying] = useState(false);

  return (
    <section id="highlights" className="py-20 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-display text-4xl md:text-5xl font-bold mb-4">
            Academy <span className="gradient-text">Highlights</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Witness the intensity, skill, and passion that defines Eastleigh FC Academy
          </p>
        </div>

        <div className="relative max-w-5xl mx-auto">
          <div className="relative rounded-3xl overflow-hidden shadow-2xl shadow-blue-500/20 aspect-video bg-gray-900">
            {!isPlaying ? (
              <>
                <img
                  src="https://images.unsplash.com/photo-1560272564-c83b66b1ad12?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80"
                  alt="Video Thumbnail"
                  className="w-full h-full object-cover opacity-60"
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <button
                    onClick={() => setIsPlaying(true)}
                    className="w-24 h-24 bg-cyan-400/20 backdrop-blur-sm rounded-full flex items-center justify-center hover:scale-110 transition-transform group"
                  >
                    <div className="w-20 h-20 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full flex items-center justify-center shadow-lg shadow-cyan-500/50 group-hover:shadow-cyan-500/80 transition-shadow">
                      <Play className="w-8 h-8 text-[#0a0e1a] ml-1" />
                    </div>
                  </button>
                </div>
                <div className="absolute bottom-6 left-6">
                  <div className="glass px-4 py-2 rounded-full text-sm font-medium">
                    2023/24 Season Montage
                  </div>
                </div>
              </>
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-black">
                <div className="text-center">
                  <div className="animate-pulse text-cyan-400 mb-4">Video Player Active</div>
                  <p className="text-gray-400">In production: Video streaming integration</p>
                  <button
                    onClick={() => setIsPlaying(false)}
                    className="mt-4 text-sm underline text-gray-500 hover:text-white"
                  >
                    Close Player
                  </button>
                </div>
              </div>
            )}
          </div>

          <div className="grid grid-cols-3 gap-4 mt-6">
            {[
              { label: 'Training Drills', value: '120+' },
              { label: 'Match Footage', value: '85+' },
              { label: 'Player Stories', value: '40+' },
            ].map((stat, idx) => (
              <div key={idx} className="glass rounded-2xl p-4 text-center">
                <div className="font-display text-2xl font-bold text-cyan-400">{stat.value}</div>
                <div className="text-sm text-gray-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Highlights;