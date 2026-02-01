import { createClient } from '@supabase/supabase-js';
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL || '',
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
    );

    const { data, error } = await supabase.from('predictions').select('*');
    
    if (error) throw error;
    return NextResponse.json(data || []);
  } catch (err: any) {
    console.error("ERREUR SERVEUR :", err.message);
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}