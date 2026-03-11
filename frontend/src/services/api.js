import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = process.env.REACT_APP_SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
  console.error('Supabase credentials not configured. Check environment variables.');
}

const supabase = createClient(SUPABASE_URL || '', SUPABASE_ANON_KEY || '');

// Squad APIs
export const squadAPI = {
  getAll: async () => {
    const { data, error } = await supabase
      .from('squads')
      .select(`
        *,
        players:players(id, first_name, last_name)
      `)
      .order('name');
    if (error) throw new Error(error.message);
    return data || [];
  },
  getById: async (id) => {
    const { data, error } = await supabase
      .from('squads')
      .select('*')
      .eq('id', id)
      .single();
    if (error) throw new Error(error.message);
    return data;
  },
  create: async (data) => {
    const { data: result, error } = await supabase
      .from('squads')
      .insert([data])
      .select();
    if (error) throw new Error(error.message);
    return result[0];
  },
  update: async (id, data) => {
    const { data: result, error } = await supabase
      .from('squads')
      .update(data)
      .eq('id', id)
      .select();
    if (error) throw new Error(error.message);
    return result[0];
  },
  delete: async (id) => {
    const { error } = await supabase
      .from('squads')
      .delete()
      .eq('id', id);
    if (error) throw new Error(error.message);
  },
};

// Player APIs
export const playerAPI = {
  getAll: async (params = {}) => {
    let query = supabase.from('players').select('*');
    if (params.squad_id) {
      query = query.eq('squad_id', params.squad_id);
    }
    if (params.position) {
      query = query.eq('position', params.position);
    }
    const { data, error } = await query;
    if (error) throw new Error(error.message);
    return data || [];
  },
  getById: async (id) => {
    const { data, error } = await supabase
      .from('players')
      .select('*')
      .eq('id', id)
      .single();
    if (error) throw new Error(error.message);
    return data;
  },
  create: async (data) => {
    const payload = {
      first_name: data.first_name,
      last_name: data.last_name,
      age: data.age || null,
      position: data.position,
      squad_id: data.squad_id,
      quote: data.quote || null,
      stats: {
        goals: data.stats_goals || 0,
        assists: data.stats_assists || 0,
        matches: data.stats_matches || 0,
      },
    };
    const { data: result, error } = await supabase
      .from('players')
      .insert([payload])
      .select();
    if (error) throw new Error(error.message);
    return result[0];
  },
  update: async (id, data) => {
    const payload = {
      first_name: data.first_name,
      last_name: data.last_name,
      age: data.age || null,
      position: data.position,
      squad_id: data.squad_id,
      quote: data.quote || null,
      stats: {
        goals: data.stats_goals || 0,
        assists: data.stats_assists || 0,
        matches: data.stats_matches || 0,
      },
    };
    const { data: result, error } = await supabase
      .from('players')
      .update(payload)
      .eq('id', id)
      .select();
    if (error) throw new Error(error.message);
    return result[0];
  },
  delete: async (id) => {
    const { error } = await supabase
      .from('players')
      .delete()
      .eq('id', id);
    if (error) throw new Error(error.message);
  },
  moveToSquad: async (id, squadId) => {
    const { data: result, error } = await supabase
      .from('players')
      .update({ squad_id: squadId })
      .eq('id', id)
      .select();
    if (error) throw new Error(error.message);
    return result[0];
  },
};

// Application APIs
export const applicationAPI = {
  getAll: async (status) => {
    let query = supabase.from('applications').select('*').order('created_at', { ascending: false });
    if (status) {
      query = query.eq('status', status);
    }
    const { data, error } = await query;
    if (error) throw new Error(error.message);
    return data || [];
  },
  create: async (data) => {
    const { data: result, error } = await supabase
      .from('applications')
      .insert([data])
      .select();
    if (error) throw new Error(error.message);
    return result[0];
  },
  updateStatus: async (id, status) => {
    const { data: result, error } = await supabase
      .from('applications')
      .update({ status })
      .eq('id', id)
      .select();
    if (error) throw new Error(error.message);
    return result[0];
  },
  delete: async (id) => {
    const { error } = await supabase
      .from('applications')
      .delete()
      .eq('id', id);
    if (error) throw new Error(error.message);
  },
};

// Initialize database - no longer needed with Supabase
export const initDatabase = async () => {
  console.log('Database already initialized on Supabase');
  return { success: true };
};

// Health check
export const healthCheck = async () => {
  try {
    const { data, error } = await supabase.from('squads').select('count');
    if (error) throw error;
    return { status: 'ok' };
  } catch (error) {
    throw new Error('Database health check failed: ' + error.message);
  }
};

const apiClient = { squadAPI, playerAPI, applicationAPI, healthCheck, initDatabase };

export default apiClient;