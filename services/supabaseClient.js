import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://xzxtbnxjbbtkuviaahob.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6eHRibnhqYmJ0a3V2aWFhaG9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk5MTgxNTgsImV4cCI6MjA3NTQ5NDE1OH0.OWHWkclVQ0d1RbiLrnk-yL5j0SVHSSMn-mxejzIxq5Y';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
