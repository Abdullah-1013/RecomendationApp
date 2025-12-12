// supabaseService.js
import { createClient } from "@supabase/supabase-js";

// <-- set these env values before running or paste directly (not recommended)
const SUPA_URL = "https://yweqmaqruqnemntvpxel.supabase.co";
const SUPA_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl3ZXFtYXFydXFuZW1udHZweGVsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA3OTQwOTgsImV4cCI6MjA0NjM3MDA5OH0.caT9BazwCZuil5X1d8zVWeBrZINRTPxQiyL4nxBHblA";

export const supabase = createClient(SUPA_URL, SUPA_KEY);

// helper to detect table mapping (frontend side)
export function mapTable(category) {
  // category returned by backend: cars, bikes, air_conditioners, records
  return category; // our Supabase table names match these strings
}
