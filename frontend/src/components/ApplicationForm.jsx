import React, { useState } from 'react';
import { Send, CheckCircle } from 'lucide-react';
import { applicationAPI } from '../services/api';

const ApplicationForm = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    dob: '',
    position: '',
    previousClub: '',
    email: '',
    phone: '',
    message: ''
  });
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      await applicationAPI.create({
        first_name: formData.firstName,
        last_name: formData.lastName,
        date_of_birth: formData.dob,
        position: formData.position,
        previous_club: formData.previousClub,
        email: formData.email,
        phone: formData.phone,
        message: formData.message
      });

      setSubmitted(true);
      setFormData({
        firstName: '',
        lastName: '',
        dob: '',
        position: '',
        previousClub: '',
        email: '',
        phone: '',
        message: ''
      });
    } catch (err) {
      setError(err.message || 'Failed to submit application. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <section id="apply" className="py-20 relative">
      <div className="absolute inset-0 opacity-5"></div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-12">
          <h2 className="font-display text-4xl md:text-5xl font-bold mb-4">
            Apply to Join <span className="gradient-text">Eastleigh FC</span>
          </h2>
          <p className="text-gray-400">
            Take the first step towards your professional football career
          </p>
        </div>

        <div className="glass rounded-3xl p-8 md:p-12">
          {submitted ? (
            <div className="text-center py-12 animate-fade-in">
              <div className="w-20 h-20 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <CheckCircle className="w-10 h-10 text-green-400" />
              </div>
              <h3 className="font-display text-2xl font-bold mb-2">Application Received!</h3>
              <p className="text-gray-400">Our scouting team will review your application and contact you within 5 working days.</p>
              <button 
                onClick={() => setSubmitted(false)}
                className="mt-6 text-cyan-400 hover:text-cyan-300 underline"
              >
                Submit another application
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-4 text-red-400 text-center">
                  {error}
                </div>
              )}
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">First Name *</label>
                  <input
                    type="text"
                    name="firstName"
                    required
                    value={formData.firstName}
                    onChange={handleChange}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors"
                    placeholder="John"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Last Name *</label>
                  <input
                    type="text"
                    name="lastName"
                    required
                    value={formData.lastName}
                    onChange={handleChange}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors"
                    placeholder="Doe"
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">Date of Birth *</label>
                  <input
                    type="date"
                    name="dob"
                    required
                    value={formData.dob}
                    onChange={handleChange}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Preferred Position *</label>
                  <select
                    name="position"
                    required
                    value={formData.position}
                    onChange={handleChange}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors"
                  >
                    <option value="">Select Position</option>
                    <option value="GK">Goalkeeper</option>
                    <option value="DEF">Defender</option>
                    <option value="MID">Midfielder</option>
                    <option value="FWD">Forward</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Previous Club (if any)</label>
                <input
                  type="text"
                  name="previousClub"
                  value={formData.previousClub}
                  onChange={handleChange}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors"
                  placeholder="e.g. Southampton Youth"
                />
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">Email *</label>
                  <input
                    type="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors"
                    placeholder="john@example.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Phone Number</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors"
                    placeholder="+254 73456 7890"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Why do you want to join Eastleigh FC Academy?</label>
                <textarea
                  name="message"
                  rows="4"
                  value={formData.message}
                  onChange={handleChange}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors resize-none"
                  placeholder="Tell us about your football journey, ambitions, and why you chose Eastleigh..."
                ></textarea>
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full bg-gradient-to-r from-cyan-400 to-blue-500 text-[#0a0e1a] font-bold py-4 rounded-xl hover:shadow-lg hover:shadow-cyan-500/30 transition-all transform hover:scale-[1.02] flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span>{submitting ? 'Submitting...' : 'Submit Application'}</span>
                <Send className="w-5 h-5" />
              </button>
            </form>
          )}
        </div>
      </div>
    </section>
  );
};

export default ApplicationForm;