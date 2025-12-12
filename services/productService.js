import { supabase } from './supabase';

// Generic function to check product in any table
export const checkProduct = async (table, query) => {
  const { data, error } = await supabase
    .from(table)
    .select('*')
    .ilike('name', query)
    .single();

  if (error && error.code !== 'PGRST116') throw error;
  return { exists: !!data, data };
};

// Generic function to add product in any table
export const addProduct = async (table, productData) => {
  const { data, error } = await supabase
    .from(table)
    .insert([productData]);

  if (error) throw error;
  return data;
};
